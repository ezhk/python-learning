"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

import sys

if __name__ == "__main__":
    print(f"Кодировка по умолчанию: {sys.getdefaultencoding()}")

    """
    Работа с файлом в обычном режиме намного проще — там
    при записи и чтении возможны только строки, поэтому
    попробуем поработать в бинарном режиме.
    """
    with open('test_file.txt', 'wb') as fh:
        for string in ("сетевое программирование", "сокет", "декоратор"):
            fh.write(string.encode(sys.getdefaultencoding()))
            fh.write(b"\n")

    """
    Проверим наши строки с правильной кодировкой — UTF8 и неправильной — UTF16.
    """
    with open('test_file.txt', 'rb') as fh:
        print(fh)
        for line in fh:
            print(f"UTF-8 {line.decode('utf-8')}"
                  f"UTF-16 {line.decode('utf-16', 'replace')}")

    """
    И откроем файл с указанной кодировкой.
    """
    with open('test_file.txt', 'r', encoding='utf-8') as fh:
        print(fh)
        for line in fh:
            print(f"UTF-8 encoded file: {line}", end='')

    """
    Кодировка по умолчанию: utf-8
    <_io.BufferedReader name='test_file.txt'>
    UTF-8 сетевое программирование
    UTF-16 臑뗐苑뗐닐뻐뗐퀠톿킀킾톳킀킰킼킼톸킀킾킲킰킽킸વ
    UTF-8 сокет
    UTF-16 臑뻐뫐뗐苑�
    UTF-8 декоратор
    UTF-16 듐뗐뫐뻐胑냐苑뻐胑�
    <_io.TextIOWrapper name='test_file.txt' mode='r' encoding='utf-8'>
    UTF-8 encoded file: сетевое программирование
    UTF-8 encoded file: сокет
    UTF-8 encoded file: декоратор

    Сожержимое test_file.txt:
        сетевое программирование
        сокет
        декоратор
    """
