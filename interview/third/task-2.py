#!/usr/bin/env python3

"""
2. Написать программу, которая запрашивает у пользователя ввод числа.
На введенное число она отвечает сообщением, целое оно или дробное.
Если дробное — необходимо далее выполнить сравнение чисел до и после запятой.

$ ./task-2.py
Введите число: 12.21
Число 12.21 — дробное, целая и дробная части отличаются
"""

import math


def try_numeric(value):
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return None


def is_float_equal(value):
    int_part, fract_part = str(value).split(".", 1)
    return int_part == fract_part


if __name__ == "__main__":
    value = input("Введите число: ")
    value = try_numeric(value)

    if value is None:
        print("Вы ввели не число")

    elif isinstance(value, int):
        print(f"Число {value} — целое")

    else:
        print(f"Число {value} — дробное, ", end="")
        if is_float_equal(value):
            print("целая и дробная части совпадают")
        else:
            print("целая и дробная части отличаются")
