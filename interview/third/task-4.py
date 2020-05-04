#!/usr/bin/env python3

"""
4. Написать программу, в которой реализовать две функции.

В первой должен создаваться простой текстовый файл.
Если файл с таким именем уже существует, выводим соответствующее сообщение.

Необходимо открыть файл и подготовить два списка: с текстовой и числовой информацией.
Например:
[91, 42, 47, 64, 60, 23, 82, 78, 22, 15]
и
['zmsebjvdgi', 'ychpwljtzn', 'zqywoopbwf', 'nkxdnnqyhe', 'eqpbrjwjdp',
'sllbegvgmh', 'kzrmrozeco', 'jbppumpypu', 'jjsmronkvm', 'qtnspcleqd']

Для создания списков использовать генераторы. Применить к спискам функцию zip().
Результат выполнения этой функции должен должен быть обработан и записан в файл таким образом,
чтобы каждая строка файла содержала текстовое и числовое значение.
Например:
91 zmsebjvdgi

42 ychpwljtzn

...

Первая функция должна возвращать ссылку на файловый дескриптор

После вызова первой функции возвращаемый файловый дескриптор нужно передавать во вторую функцию
Во второй функции необходимо реализовать открытие файла и простой построчный вывод содержимого.

$ ./task-4.py
Filename testresult-4.txt already exists
91 zmsebjvdgi
42 ychpwljtzn
47 zqywoopbwf
64 nkxdnnqyhe
60 eqpbrjwjdp
23 sllbegvgmh
82 kzrmrozeco
78 jbppumpypu
22 jjsmronkvm
15 qtnspcleqd
"""

import os


def generate_lines(r_list, l_list):
    for num, string in zip(r_list, l_list):
        yield f"{num} {string}\n"


def save_data(filename, r_list, l_list):
    if os.path.isfile(filename):
        print(f"Filename {filename} already exists")

    fh = open(filename, "w+")
    for line in generate_lines(r_list, l_list):
        fh.write(line)
    return fh


def print_file(fh):
    fh.seek(0)
    for line in fh:
        print(line, end="")
    fh.close()


if __name__ == "__main__":
    RIGHT_LIST = [91, 42, 47, 64, 60, 23, 82, 78, 22, 15]
    LEFT_LIST = [
        "zmsebjvdgi",
        "ychpwljtzn",
        "zqywoopbwf",
        "nkxdnnqyhe",
        "eqpbrjwjdp",
        "sllbegvgmh",
        "kzrmrozeco",
        "jbppumpypu",
        "jjsmronkvm",
        "qtnspcleqd",
    ]

    fhandle = save_data("testresult-4.txt", RIGHT_LIST, LEFT_LIST)
    print_file(fhandle)
