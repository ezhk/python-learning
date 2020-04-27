#!/usr/bin/env python3

"""
5. Усовершенствовать первую функцию из предыдущего примера.

Необходимо просканировать текстовый файл, созданный на предыдущем задании
и реализовать создание и запись нового текстового файла

В новый текстовый файл обеспечить запись строк вида:

zmsebjvdgi zmsebjvdgi
ychpwljtzn ychpwljtzn
...

Т.е. извлекаются строки из первого текстового файла
а в новый они записываются в виде, где вместо числа ставится строка

Здесь необходимо использовать регулярные выражения.

$ ./task-5.py
zmsebjvdgi zmsebjvdgi
ychpwljtzn ychpwljtzn
zqywoopbwf zqywoopbwf
nkxdnnqyhe nkxdnnqyhe
eqpbrjwjdp eqpbrjwjdp
sllbegvgmh sllbegvgmh
kzrmrozeco kzrmrozeco
jbppumpypu jbppumpypu
jjsmronkvm jjsmronkvm
qtnspcleqd qtnspcleqd
"""


import re


def read_fname(filename):
    with open(filename, "r") as fh:
        for line in fh:
            yield line


def process_fname(old_file, new_file):
    with open(new_file, "w+") as fh:
        for line in read_fname(old_file):
            # split will be better here
            new_line = re.sub(r"^(\d+)\s+(.+)", "\\2 \\2", line)
            fh.write(new_line)
            print(new_line, end="")


if __name__ == "__main__":
    process_fname("testresult-4.txt", "testresult-5.txt")
