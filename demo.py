from frolick.page import Page
import uvicorn

class MyPage(Page):
    def __init__(self):
        super().__init__()
        self.vars = {
            'x': 1,
            'y': 2,
        }

    def my_function(self):
        self.vars['x'] += 2
        return {'x': self.vars['x']}

    def another_function(self):
        self.vars['y'] += 1
        return {'y': self.vars['y']}

    def reset(self):
        self.vars['x'] = 1
        self.vars['y'] = 2
        return {
            'x': self.vars['x'],
            'y': self.vars['y'],
        }


p = MyPage()
p.title('Cool Appliances')
p.write(title='This is a success')
p.write(title='Card 2', content='This is another success')
p.write(content='Three time\'s the charm')
p.button('Click Moi!', p.my_function)
p.button('Change y', p.another_function)
p.button('Reset', p.reset)
p.init_server()

if __name__ == "__main__":
    p.launch(reload=True)
