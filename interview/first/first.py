#!/usr/bin/env python
"""
Домашнее задание к первому уроку по курсу
«подготовка к собеседованию Python-разработчика».
"""

from decimal import Decimal
from hashlib import sha256
import os
import time

from tabulate import tabulate


def multiplication_table(x_lines=10, y_lines=10):
    """
    Написать функцию, реализующую вывод таблицы умножения размерностью A x B.
    Первый и второй множитель должны задаваться в виде аргументов функции.
    Значения каждой строки таблицы должны быть представлены списком, который формируется в цикле.
    После этого осуществляется вызов внешней lambda-функции,
        которая формирует на основе списка строку.
    Полученная строка выводится в главной функции.
    Элементы строки (элементы таблицы умножения) должны разделяться табуляцией.
    """

    lines = []
    for y_pos in range(1, y_lines + 1):
        lines.append([x_pos * y_pos for x_pos in range(1, x_lines + 1)])
    return tabulate(lines)


def print_directory_contents(source_dir):
    """
    Функция принимает имя каталога и распечатывает его содержимое
    в виде «путь и имя файла», а также любые другие
    файлы во вложенных каталогах.

    Эта функция подобна os.walk. Использовать функцию os.walk
    нельзя. Данная задача показывает ваше умение работать с
    вложенными структурами.
    """

    for fname in os.listdir(source_dir):
        fpath = os.path.join(source_dir, fname)
        if os.path.isfile(fpath):
            print(fpath)
        elif os.path.isdir(fpath):
            print_directory_contents(fpath)
        else:
            # symlink?
            pass


def rand_generator(start=-50, stop=50, count=10):
    """
    3. Разработать генератор случайных чисел.
    В функцию передавать начальное и конечное число генерации
        (нуль необходимо исключить).
    Заполнить этими данными список и словарь.
    Ключи словаря должны создаваться по шаблону: “elem_<номер_элемента>”.
    Вывести содержимое созданных списка и словаря.

    Пример:
    (
    [18, 22, 21, 23, 18, 21, 19, 16, 18, 8],
    {'elem_18': 18, 'elem_22': 22, 'elem_21': 21,
     'elem_23': 23, 'elem_19': 19, 'elem_16': 16, 'elem_8': 8}
    )
    """

    rand_list = []
    rand_dict = {}
    available_range = stop - start

    while count:
        init_rand = str(time.time()).encode()
        init_hash_sum = sha256(init_rand).hexdigest()
        pseudo_rand = int(init_hash_sum, 16)
        rand_val = start + (pseudo_rand % available_range)

        # skip zero values
        if rand_val == 0:
            continue

        rand_list.append(rand_val)
        rand_dict.setdefault(f"elem_{rand_val}", rand_val)
        count -= 1

    print(rand_list)
    print(rand_dict)


def calc_deposit(amount, month_duration, month_change=0):
    """
    4 и 5. Написать программу «Банковский депозит».
    Она должна состоять из функции и ее вызова с аргументами.
    Клиент банка делает депозит на определенный срок.
    В зависимости от суммы и срока вклада определяется процентная ставка:
        1000–10000 руб (6 месяцев — 5 % годовых, год — 6 % годовых, 2 года — 5 % годовых).
        10000–100000 руб (6 месяцев — 6 % годовых, год — 7 % годовых, 2 года – 6.5 % годовых).
        100000–1000000 руб (6 месяцев — 7 % годовых, год — 8 % годовых, 2 года — 7.5 % годовых).
    Необходимо написать функцию, в которую будут передаваться параметры: сумма вклада и срок вклада.
    Каждый из трех банковских продуктов должен быть представлен в виде словаря с ключами
        (begin_sum, end_sum, 6, 12, 24).
    Ключам соответствуют значения начала и конца диапазона суммы вклада
        и значения процентной ставки для каждого срока.
    В функции необходимо проверять принадлежность суммы вклада к одному из диапазонов
        и выполнять расчет по нужной процентной ставке.
    Функция возвращает сумму вклада на конец срока.

    Также добавлена функциональность с ежемесячным пополнением счета.
    """

    INTEREST_RATE = {
        (1000, 10000, 6, 12, 24): (5, 6, 5),
        (10000, 100000, 6, 12, 24): (6, 7, 6.5),
        (100000, 1000000, 6, 12, 24): (7, 8, 7.5),
    }
    MONTH_IN_YEAR = 12

    def _monthly_capitalization_calc(amount, rate, duration):
        return amount * (1 + rate / (100 * 12)) ** duration

    def _year_capitalization_calc(amount, rate, duration):
        year_ratio = max(1, duration // MONTH_IN_YEAR)
        effective_ratio = Decimal(1 + rate / 100) ** year_ratio - 1
        monthly_effective_ratio = effective_ratio / (
            year_ratio * MONTH_IN_YEAR
        )
        return amount + amount * duration * monthly_effective_ratio

    def _deposit_with_percents(amount, rate, duration, change=0):
        amount = Decimal(amount)
        rate = Decimal(rate)

        amount = _monthly_capitalization_calc(amount, rate, duration)
        if not change:
            return amount

        for month in range(1, duration):
            amount += _monthly_capitalization_calc(
                change, rate, duration - month
            )

        return amount

    current_year_rate = None
    for product, rate in INTEREST_RATE.items():
        product = list(product)
        rate = list(rate)

        begin_sum = product.pop(0)
        end_sum = product.pop(0)
        if begin_sum <= amount < end_sum:
            while product:
                duration = product.pop()
                current_rate = rate.pop()

                if month_duration // duration > 0:
                    current_year_rate = current_rate
                    break
        if current_year_rate:
            break
    if current_year_rate is None:
        return None

    return format(
        _deposit_with_percents(
            amount, current_year_rate, month_duration, month_change
        ),
        ".4f",
    )


if __name__ == "__main__":
    print("---\nMultiplication table")
    print(multiplication_table(10, 5))

    print("---\nDirectory list")
    print_directory_contents(".")

    print("---\nRandom generator")
    rand_generator(0, 10)

    print("---\nDeposit")
    print(f"10_000 in 2 years: {calc_deposit(10000, 24)}")
    print(f"15_000 in a half year: {calc_deposit(15000, 6)}")
    print(f"150_000 in 10 years: {calc_deposit(150000, 120)}")

    print("---\nDeposit with monthly replenishment")
    print(
        "10_000 in 2 years, monthly payment 100: "
        f"{calc_deposit(10000, 24, 100)}"
    )
    print(
        "15_000 in 3 years, monthly payment 1000: "
        f"{calc_deposit(15000, 36, 1000)}"
    )
    print(
        "150_000 in 10 years, monthly payment 5000: "
        f"{calc_deposit(150000, 120, 5000)}"
    )
