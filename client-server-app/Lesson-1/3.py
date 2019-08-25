"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

if __name__ == "__main__":
    for word in (b"attribute", b"type"):
        print("value = %s, len = %s, type = %s" % (word, len(word), type(word)))

    """
    for word in (b"attribute", b"класс", b"функция", b"type"):
    SyntaxError: bytes can only contain ASCII literal characters.

    b"класс", b"функция" — нельзя записать как бинарную строку через b""
    """
