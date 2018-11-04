from distutils.core import setup

setup(
    name="Loïc Lisp",
    version="0.1.0",
    author="Loïc CARR",
    author_email="loic.carr@gmail.com",
    packages=["llisp"],
    description="My simple Lisp interpreter",
    entry_points={"console_scripts": ["llisplang = llisp.main:main"]},
)
