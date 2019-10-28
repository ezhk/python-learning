- Написать регулярное выражение, которое проверяет валидный IP-адрес. Например, 192.168.1.1 подойдет, а 256.300.1.1 — нет.

    ```
    (?:(?P<octet>25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}(?P<lastOctet>25[0-5]|2[0-4]\d|1?\d{1,2})
    ```

- Написать регулярное выражение, которое проверяет, является ли указанный файлом нужного типа (на выбор .com,.exe или .jpg,.png,.gif и т.д.). Написать регулярное выражение для проверки, ведет ли ссылка URL на некоторый файл, и это действительно ссылка на картинку (например, http://site.com/folder/1.png), а не на любой файл.

    ```
    .+\.png$
    ```

- Написать регулярное выражение, которое проверяет, является выведенное значение «белым» IP-адресом (5.255.255.5 подойдет, а 172.16.0.1 — нет).

    ```
    ^(?!127\.|10\.|192\.168\.|(?P<CGN>100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))|172\.(?:1[6-9]|2\d|3[01]))(?P<whiteIP>.*)
    ```

- Написать регулярное выражение, которое проверяет, что файл в URL (например, https://site.ru/folder/download/test.docx) не обладает неким расширением (например .exe не пройдет, или .sh — не пройдет. Выбор списка исключенных расширений за вами).

    ```
    ^(?!(?=.*\.(exe|sh)$))
    ```