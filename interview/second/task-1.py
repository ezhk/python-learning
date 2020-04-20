#!/usr/bin/env python

"""
Проверить механизм наследования в Python.

Для этого создать два класса. Первый — родительский (ItemDiscount),
должен содержать статическую информацию о товаре: название и цену.

Второй — дочерний (ItemDiscountReport),
должен содержать функцию (get_parent_data), отвечающую
за отображение информации о товаре в одной строке.

Проверить работу программы.
"""


class ItemDiscount:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class ItemDiscountReport(ItemDiscount):
    def get_parent_data(self):
        return f"item: {self.name}, price: {self.price}"


if __name__ == "__main__":
    item = ItemDiscount("стол", 15000)
    try:
        print(item.get_parent_data())
    except AttributeError as err:
        print(f"method get_parent_data error: {err}, {type(item)}")

    item_report = ItemDiscountReport("стул", 5000)
    print(item_report.get_parent_data())
