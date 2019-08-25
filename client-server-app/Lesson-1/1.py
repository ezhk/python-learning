# -*- coding: utf-8 -*-

"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
"""

if __name__ == "__main__":
    words = ("разработка", "сокеты", "декоратор")
    for word in words:
        print("value = %s, type = %s" % (word, type(word)))

    words_utf = ('\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                 '\u0441\u043e\u043a\u0435\u0442\u044b',
                 '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')
    for word in words_utf:
        print("value = %s, type = %s" % (word, type(word)))

    """
    Python 3.7:
    value = разработка, type = <class 'str'>
    value = сокеты, type = <class 'str'>
    value = декоратор, type = <class 'str'>
    value = разработка, type = <class 'str'>
    value = сокеты, type = <class 'str'>
    value = декоратор, type = <class 'str'>

    Python 2.7:
    value = разработка, type = <type 'str'>
    value = сокеты, type = <type 'str'>
    value = декоратор, type = <type 'str'>
    value = \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430, type = <type 'str'>
    value = \u0441\u043e\u043a\u0435\u0442\u044b, type = <type 'str'>
    value = \u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440, type = <type 'str'>
    """
