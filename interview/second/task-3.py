#!/usr/bin/env python

"""
3. Усовершенствовать родительский класс таким образом,
чтобы получить доступ к защищенным переменным.
"""


class ItemDiscount:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price


class ItemDiscountReport(ItemDiscount):
    def get_parent_data(self):
        return f"item: {self.name}, price: {self.price}"


if __name__ == "__main__":
    item = ItemDiscountReport("стол", 15000)
    print(item.get_parent_data())
