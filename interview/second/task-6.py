#!/usr/bin/env python

"""
6. Проверить на практике возможности полиморфизма.

Необходимо разделить дочерний класс ItemDiscountReport на два класса.

Инициализировать классы необязательно.

Внутри каждого поместить функцию get_info,
которая в первом классе будет отвечать за вывод названия товара,
а вторая — его цены.

Далее реализовать выполнение каждой из функции тремя способами.
"""


class ItemDiscount:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    def __str__(self):
        return f"Price for {self.name}: {self.price}"


class ItemDiscountReportName(ItemDiscount):
    def get_info(self):
        return f"Name {self.name}"


class ItemDiscountReportPrice(ItemDiscount):
    def get_info(self):
        return f"Price {self.price}"


if __name__ == "__main__":
    item_name = ItemDiscountReportName("стул", 5000)
    print(item_name.get_info())

    item_price = ItemDiscountReportPrice("стол", 15000)
    print(item_price.get_info())
