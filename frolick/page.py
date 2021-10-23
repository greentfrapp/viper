from concurrent.futures.thread import ThreadPoolExecutor
import contextlib
import importlib
import inspect
import sys
import time
import threading

from typing import Any

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


class ImportFromStringError(Exception):
    pass


def import_from_string(import_str: Any) -> Any:
    if not isinstance(import_str, str):
        return import_str

    module_str, _, attrs_str = import_str.partition(":")
    if not module_str or not attrs_str:
        message = (
            'Import string "{import_str}" must be in format "<module>:<attribute>".'
        )
        raise ImportFromStringError(message.format(import_str=import_str))

    try:
        module = importlib.import_module(module_str)
    except ImportError as exc:
        if exc.name != module_str:
            raise exc from None
        message = 'Could not import module "{module_str}".'
        raise ImportFromStringError(message.format(module_str=module_str))

    module = importlib.reload(module)
    instance = module
    try:
        for attr_str in attrs_str.split("."):
            instance = getattr(instance, attr_str)
    except AttributeError:
        message = 'Attribute "{attrs_str}" not found in module "{module_str}".'
        raise ImportFromStringError(
            message.format(attrs_str=attrs_str, module_str=module_str)
        )

    return instance


class Server(uvicorn.Server):
    def __init__(self, config):
        super().__init__(config)
        self.keep_running = True

    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        self.keep_running = True
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(0.1)
            yield
            while self.keep_running:
                time.sleep(0.1)
        finally:
            self.should_exit = True
            thread.join()


class Watcher:
    def __init__(self):
        """
        Takes a list of variables and watches for changes by monitoring
        setting and getting functions
        """
        pass


class Page:
    def __init__(self):
        self.app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
        self.templates = Jinja2Templates(directory="frolick/frontend/dist")
        self.content = []
        self.buttons = []
        self._title = "My Frolick App"
        self.host = "0.0.0.0"
        self.port = "8000"

        self.server = None
        
        self._script = sys.argv[0]

        self.vars = {}

    def title(self, title):
        self._title = title

    def write(self, title="", content=""):
        self.content.append({
            "title": title,
            "content": content,
        })

    def button(self, label, callback):
        self.buttons.append({
            'label': label,
            'callback': callback,
        })

    def _reload_server(self, app):
        app = import_from_string(app)
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="warning")
        self.server = Server(config=config)
        with self.server.run_in_thread():
            while self.server.keep_running:
                pass

    def _start_watcher(self):
        handler = FileSystemEventHandler()
        app = self
        def fn(*args, **kwargs):
            app.server.keep_running = False
            app.running = False
        handler.on_modified = fn
        observer = Observer()
        observer.schedule(handler, self._script, recursive=True)
        observer.start()
        self.running = True
        try:
            while self.running:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()

    def init_server(self):
        @self.app.get('/', response_class=HTMLResponse)
        async def root(request: Request):
            return self.templates.TemplateResponse("index.html", {'request': request})
        @self.app.get('/ping')
        async def ping(request: Request):
            return {'hello': 'world'}
        @self.app.get('/vars')
        async def get_vars(request: Request):
            return self.vars
        @self.app.get('/title')
        async def get_title(request: Request):
            return {'title': self._title}
        @self.app.get('/content')
        async def get_content(request: Request):
            return {'content': self.content}
        @self.app.get('/show')
        async def get_show(request: Request):
            return list(self.vars.keys())
        @self.app.get('/buttons')
        async def get_buttons(request: Request):
            return [{"label": b['label'], "callback": b['callback'].__name__} for b in self.buttons]
        for i in self.buttons:
            self.app.get(f'/{i["callback"].__name__}')(i["callback"])
        self.app.mount("/", StaticFiles(directory="frolick/frontend/dist"), name="")

    def _get_var_name(self):
        # NOTE this is brittle
        f_back = inspect.currentframe().f_back
        var_name = [var_name for var_name, var_val in f_back.f_locals.items() if var_val is self][0]
        while var_name in ['self', '_app']:
            f_back = f_back.f_back
            var_name = [var_name for var_name, var_val in f_back.f_locals.items() if var_val is self][0]
        return var_name

    def _get_module(self):
        # NOTE this is brittle
        script_name = sys.argv[0]
        var_name = self._get_var_name()
        return f'{script_name.split(".")[0]}:{var_name}.app'

    def launch(self, reload=False):
        print(f"Frolick is running on http://{self.host}:{self.port} (Press CTRL+C to quit)")
        if reload:
            print("Note that for reload=True, launch() should be called within the if __name__ == '__main__' scope")
            self._module_name = self._get_module()
            try:
                while True:
                    with ThreadPoolExecutor() as executor:
                        self.server_future = executor.submit(self._reload_server, self._module_name)
                        watcher_future = executor.submit(self._start_watcher)
                    watcher_future.result()
            except KeyboardInterrupt:
                print('\nExiting...')
                self.server.keep_running = False
                self.running = False
        else:
            uvicorn.run(self.app, host=self.host, port=self.port, log_level='warning')
