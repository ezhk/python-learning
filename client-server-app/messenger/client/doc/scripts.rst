Scripts
=======

client.py
---------

Основная часть клиентского пакета — запускает GUI и
в потоке забускает обратку сообщений. 

Справка по использованию:

::

    Usage: client.py [-h] [-a ADDRESS] [-p PORT] [-u USERNAME] [-P PASSWORD]

    Messenger application.

    optional arguments:
    -h, --help            show this help message and exit
    -a ADDRESS, --address ADDRESS
    -p PORT, --port PORT
    -u USERNAME, --username USERNAME
    -P PASSWORD, --password PASSWORD

Как запускается клиентская часть:

- если не использовались ключи, то вы увидите диалоговое окно в вводом логина и пароля
- затем создается thread, работающий с сервером и параллельно запускается окно чатов
- в основном обраточике (треде), происходит сначала шифрование канала:

    - сервер при соединении отправляет свой публичный ключи
    - клиент генерирует случайную последовательность (которая в дальнейшем является сессионым ключом)
    - клиент шифрует открытым ключом сессионный и отправляет на сервер

- затем клиент шлет presence сообщение и запрашивает список контактов

В дальнешем при получении сообщение в случае активности текущего чата загружается вся последняя история чата.

multiple-client.py
------------------

Не более чем обвязка с Popen, которая позволяет удобно запускать несколько клиентов и их останавливать.

Опции:

- **r** (run) — запустить ещё один клиентский процесс
- **c** (close all processes) — закрывает все клиенские процессы
- **s** (show clients) — показывает список клиентов в служебном виде
- **q** (quit) — выход из программы, но сначала надо закрыть все процессы