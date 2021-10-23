from setuptools import setup, find_packages

version = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="frolick",
    packages=find_packages(exclude=[]),
    version=version,
    description=(
        "Frolick. "
        "Build your frontend with Python."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The Frolick Authors",
    author_email="limsweekiat@gmail.com",
    url="https://github.com/greentfrapp/frolick",
    license="Apache License 2.0",
    keywords=[
        "frontend",
        "webdev",
    ],
    install_requires=[
        "fastapi",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
