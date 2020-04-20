#!/usr/bin/env python

"""
2. Инкапсулировать оба параметра (название и цену)
товара родительского класса.
Убедиться, что при сохранении текущей логики работы программы
будет сгенерирована ошибка выполнения.
"""


class ItemDiscount:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price


class ItemDiscountReport(ItemDiscount):
    def get_parent_data(self):
        return f"item: {self.__name}, price: {self.__price}"


if __name__ == "__main__":
    item = ItemDiscountReport("стол", 15000)
    try:
        print(item.get_parent_data())
    except AttributeError as err:
        print(f"method get_parent_data error: {err}, {type(item)}")
