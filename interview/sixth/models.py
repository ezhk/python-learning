#!/usr/bin/env python3

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types import choice, email, phone_number

Base = declarative_base()

"""
Вспомогательные таблицы.

Категории товаров.
    Написать запрос создания таблицы categories (с проверкой ее существования). 
    Таблица должна содержать два поля: category_name (категория), category_description (описание).
    Все поля должны быть не пустыми.
    Поле category должно быть первичным ключом.
Единицы измерения товаров.
    Написать запрос создания таблицы units с проверкой ее существования.
    Таблица должна содержать одно поле — unit (единица измерения).
    Оно должно быть не пустым и выступать первичным ключом.
Должности.
    Написать запрос создания таблицы positions (с проверкой ее существования).
    Таблица должна содержать одно поле — position (должность).
    Оно должно быть не пустым и выступать первичным ключом. 
"""


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(Text(8192), nullable=False)


class Units(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(String(128), nullable=False)


class Positions(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    position = Column(String(128), nullable=False)


class Ownerships(Base):
    __tablename__ = "ownerships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ownership = Column(String(128), nullable=False)


"""
Основные таблицы.

Товары.
    Написать запрос создания таблицы goods с проверкой ее существования.
    Таблица должна содержать четыре поля:
        good_id (номер товара — первичный ключ),
        good_name (название товара),
        good_unit (единица измерения товара — внешний ключ на таблицу units),
        good_cat (категория товара — внешний ключ на таблицу categories).
Сотрудники.
    Написать запрос создания таблицы employees с проверкой ее существования.
    Таблица должна содержать три поля:
        employee_id (номер сотрудника — первичный ключ),
        employee_fio (ФИО сотрудника),
        employee_position (должность сотрудника — внешний ключ на таблицу positions).
Поставщики.
    Написать запрос создания таблицы vendors с проверкой ее существования.
    Таблица должна содержать шесть полей:
        vendor_id (номер поставщика — первичный ключ),
        vendor_name (название поставщика),
        vendor_ownerchipform (форма собственности поставщика),
        vendor_address (адрес поставщика),
        vendor_phone (телефон поставщика),
        vendor_email (email поставщика).
"""


class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, index=True)
    unit = Column(Integer, ForeignKey("units.id"))
    category = Column(Integer, ForeignKey("categories.id"))


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(256), nullable=False, index=True)
    position = Column(Integer, ForeignKey("positions.id"))


class Vendors(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, index=True)
    ownership_form = Column(Integer, ForeignKey("ownerships.id"))
    address = Column(String(512), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(128), nullable=False)
