"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

if __name__ == "__main__":
    for word in ("разработка", "администрирование", "protocol", "standard"):
        encoded = word.encode('utf-8')
        decoded = encoded.decode('utf-8')
        print("encoded = %s, decoded = %s" % (encoded, decoded))

    """
    encoded = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0', decoded = разработка
    encoded = b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', decoded = администрирование
    encoded = b'protocol', decoded = protocol
    encoded = b'standard', decoded = standard
    """
