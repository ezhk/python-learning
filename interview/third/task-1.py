#!/usr/bin/env python3

"""
1. Написать программу, которая будет содержать функцию
для получения имени файла из полного пути до него.

При вызове функции в качестве аргумента должен передаваться путь до файла.
В функции необходимо реализовать «выделение» из этого пути имени файла (без расширения).

Пример:
функция принмает следующую строку - '../mainapp/views.py'

Результат:
views

$ ./task-1.py
filename without extension: testfilename
"""

import os


def get_filename(filepath):
    filename = os.path.basename(filepath)
    fname, _ = os.path.splitext(filename)

    return fname


if __name__ == "__main__":
    print(
        "filename without extension:",
        get_filename("./testpath/testfilename.md"),
    )
