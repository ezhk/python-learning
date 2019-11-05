# Docker

- Запустить контейнер с nginx

```
$ sudo docker run -d --name nginx-test -p 8080:80 nginx:latest
    Unable to find image 'nginx:latest' locally
    latest: Pulling from library/nginx
    8d691f585fa8: Pull complete
    5b07f4e08ad0: Pull complete
    abc291867bca: Pull complete
    Digest: sha256:922c815aa4df050d4df476e92daed4231f466acc8ee90e0e774951b0fd7195a4
    Status: Downloaded newer image for nginx:latest
    ff8092176e66faa25db45a8020cebe8d0991d9af0b9a79c07ea2739b060aefe3
``` 
 
- Запустить контейнер с MySQL, убедиться , что контейнер с MySQL стартует и вы можете пропасть в БД

```
$ sudo docker run -d --name mysql-test -e MYSQL_ROOT_PASSWORD=password -p 33306:3306 mysql:latest
    Unable to find image 'mysql:latest' locally
    latest: Pulling from library/mysql
    80369df48736: Pull complete
    e8f52315cb10: Pull complete
    cf2189b391fc: Pull complete
    cc98f645c682: Pull complete
    27a27ac83f74: Pull complete
    fa1f04453414: Pull complete
    d45bf7d22d33: Pull complete
    3dbac26e409c: Pull complete
    9017140fb8c1: Pull complete
    b76dda2673ae: Pull complete
    bea9eb46d12a: Pull complete
    e1f050a38d0f: Pull complete
    Digest: sha256:7345ce4ce6f0c1771d01fa333b8edb2c606ca59d385f69575f8e3e2ec6695eee
    Status: Downloaded newer image for mysql:latest
    67385289a5750b03d639656e2da52f12d7fe8bb41a5c60edb36511d9dbf3fabd

$ mysql -uroot -h 127.0.0.1 -P 33306 -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 8
    Server version: 8.0.18 MySQL Community Server - GPL

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | sys                |
    +--------------------+
    4 rows in set (0.00 sec)
```

- Убедиться, что оба контейнера доступны снаружи виртуальной машины

```
$ sudo docker ps
    CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                PORTS                                NAMES
    67385289a575        mysql:latest                  "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes          33060/tcp, 0.0.0.0:33306->3306/tcp   mysql-test
    ff8092176e66        nginx:latest                  "nginx -g 'daemon of…"   3 minutes ago       Up 3 minutes          0.0.0.0:8080->80/tcp                 nginx-test


$ curl localhost:8080
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>

/*
 * Доступ по порту 33306 на localhost указан выше,
 * здесь опишу как попасть в контейнер через exec.
 */

$ sudo docker exec -ti 67385289a575 mysql -uroot -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 10
    Server version: 8.0.18 MySQL Community Server - GPL

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
```
