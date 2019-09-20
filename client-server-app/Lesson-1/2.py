"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

if __name__ == "__main__":
    for word in (b"class", b"function", b"method"):
        print("value = %s, len = %s, type = %s" % (word, len(word), type(word)))

    """
    value = b'class', len = 5, type = <class 'bytes'>
    value = b'function', len = 8, type = <class 'bytes'>
    value = b'method', len = 6, type = <class 'bytes'>
    """
