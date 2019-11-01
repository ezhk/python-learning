#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="JSON-messenger-client",
    description="JSON instant messenger, learning project",
    author="Andrey Kiselev",
    author_email="kiselevandrew@yandex.ru",
    version="0.1a2",
    packages=find_packages(),
    scripts=["client.py", "multiple-client.py"],
    install_requires=["pycryptodome==3.9.0", "PyQt5==5.13.1"],
    setup_requires=["wheel", "twine"],
)
