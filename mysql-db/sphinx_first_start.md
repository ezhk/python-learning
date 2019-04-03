# Install Sphinx
Предполагаем, что MySQL уже установлен.

    $ sudo apt-get install sphinxsearch

Правим запуск sphinx в /etc/default/sphinxsearch и запускаем:

    $ sudo cp /etc/sphinxsearch/sphinx.conf.sample /etc/sphinxsearch/sphinx.conf
    $ sudo /etc/init.d/sphinxsearch restart

Перед перезапуском стоит проверить пользователя MySQL.

# Create index and search

    $ sudo mysql -u root
    mysql> CREATE DATABASE test;
    mysql> SOURCE /etc/sphinxsearch/example.sql;
    Query OK, 0 rows affected, 1 warning (0.03 sec)

    Query OK, 0 rows affected (0.13 sec)

    Query OK, 4 rows affected (0.02 sec)
    Records: 4  Duplicates: 0  Warnings: 0

    Query OK, 0 rows affected, 1 warning (0.01 sec)

    Query OK, 0 rows affected (0.01 sec)

    Query OK, 10 rows affected (0.00 sec)
    Records: 10  Duplicates: 0  Warnings: 0

    mysql> use test;
    mysql> select * from  documents;
    +----+----------+-----------+---------------------+-----------------+---------------------------------------------------------------------------+
    | id | group_id | group_id2 | date_added          | title           | content                                                                   |
    +----+----------+-----------+---------------------+-----------------+---------------------------------------------------------------------------+
    |  1 |        1 |         5 | 2019-04-03 11:13:30 | test one        | this is my test document number one. also checking search within phrases. |
    |  2 |        1 |         6 | 2019-04-03 11:13:30 | test two        | this is my test document number two                                       |
    |  3 |        2 |         7 | 2019-04-03 11:13:30 | another doc     | this is another group                                                     |
    |  4 |        2 |         8 | 2019-04-03 11:13:30 | doc number four | this is to test groups                                                    |
    +----+----------+-----------+---------------------+-----------------+---------------------------------------------------------------------------+
    4 rows in set (0.00 sec)

Создаем поисковый индекс:

    $ sudo indexer --all
    Sphinx 2.2.11-id64-release (95ae9a6)
    Copyright (c) 2001-2016, Andrew Aksyonoff
    Copyright (c) 2008-2016, Sphinx Technologies Inc (http://sphinxsearch.com)

    using config file '/etc/sphinxsearch/sphinx.conf'...
    indexing index 'test1'...
    collected 4 docs, 0.0 MB
    sorted 0.0 Mhits, 100.0% done
    total 4 docs, 193 bytes
    total 0.023 sec, 8129 bytes/sec, 168.49 docs/sec
    indexing index 'test1stemmed'...
    collected 4 docs, 0.0 MB
    sorted 0.0 Mhits, 100.0% done
    total 4 docs, 193 bytes
    total 0.001 sec, 152689 bytes/sec, 3164.55 docs/sec
    skipping non-plain index 'dist1'...
    skipping non-plain index 'rt'...
    total 8 reads, 0.000 sec, 0.1 kb/call avg, 0.0 msec/call avg
    total 24 writes, 0.000 sec, 0.1 kb/call avg, 0.0 msec/call avg

Попробуем что-то поискать:

    $ sudo mysql -h127.0.0.1 -P9306
    mysql> SELECT * FROM test1 WHERE MATCH('@content document');
    +------+----------+------------+
    | id   | group_id | date_added |
    +------+----------+------------+
    |    1 |        1 | 1554279210 |
    |    2 |        1 | 1554279210 |
    +------+----------+------------+
    2 rows in set (0.00 sec)

    mysql> SELECT * FROM test1 WHERE MATCH('@content world');
    Empty set (0.00 sec)

    mysql> SELECT * FROM test1 WHERE MATCH('@content one');
    +------+----------+------------+
    | id   | group_id | date_added |
    +------+----------+------------+
    |    1 |        1 | 1554279210 |
    +------+----------+------------+
    1 row in set (0.00 sec)

Работает.
