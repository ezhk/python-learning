#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="JSON-messenger-server",
    description="JSON instant messenger server",
    author="Andrey Kiselev",
    author_email="kiselevandrew@yandex.ru",
    version="0.1a1",
    packages=find_packages(),
    scripts=["server.py"],
    package_data={"": "settings.ini"},
    include_package_data=True,
    install_requires=[
        "pycryptodome==3.9.0",
        "PyQt5==5.13.1",
        "SQLAlchemy==1.3.8",
    ],
    setup_requires=["wheel"],
)
