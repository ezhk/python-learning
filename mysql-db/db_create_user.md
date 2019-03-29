# Create user and check grants

mysql> CREATE USER 'test-user-homework'@'%' IDENTIFIED BY 'test-password';

    Query OK, 0 rows affected (0.01 sec)

mysql> GRANT SELECT, UPDATE, INSERT ON `geodata`.* TO 'test-user-homework'@'%';

    Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH PRIVILEGES;

    Query OK, 0 rows affected (0.00 sec)

$ mysql -utest-user-homework -p

    Enter password:

mysql> show databases;

    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | geodata            |
    +--------------------+
    2 rows in set (0.01 sec)

mysql> USE geodata;

    Database changed

mysql> SHOW TABLES;

    +---------------------+
    | Tables_in_geodata   |
    +---------------------+
    | _cities             |
    | _countries          |
    | _regions            |
    | cities              |
    | cities_view         |
    | moscow_region       |
    | moscow_regions_view |
    +---------------------+
    7 rows in set (0.00 sec)

mysql> SELECT * FROM _regions LIMIT 5;

    +-------+------------+------------------------+
    | id    | country_id | title                  |
    +-------+------------+------------------------+
    |   875 |        137 | Imo State              |
    |  2188 |         80 | Pune                   |
    |  2763 |         97 | Chongqing Municipality |
    | 13330 |        137 | Ogun State             |
    | 20573 |        130 | Dornod Aymag           |
    +-------+------------+------------------------+
    5 rows in set (0.00 sec)


# Modify grants

mysql> SHOW GRANTS FOR 'test-user-homework'@'%';

    +-------------------------------------------------------------------------+
    | Grants for test-user-homework@%                                         |
    +-------------------------------------------------------------------------+
    | GRANT USAGE ON *.* TO 'test-user-homework'@'%'                          |
    | GRANT SELECT, INSERT, UPDATE ON `geodata`.* TO 'test-user-homework'@'%' |
    +-------------------------------------------------------------------------+

mysql> REVOKE INSERT ON `geodata`.* FROM 'test-user-homework'@'%';

    Query OK, 0 rows affected (0.02 sec)

mysql> FLUSH PRIVILEGES;

    Query OK, 0 rows affected (0.01 sec)

mysql> SHOW GRANTS FOR 'test-user-homework'@'%';

    +-----------------------------------------------------------------+
    | Grants for test-user-homework@%                                 |
    +-----------------------------------------------------------------+
    | GRANT USAGE ON *.* TO 'test-user-homework'@'%'                  |
    | GRANT SELECT, UPDATE ON `geodata`.* TO 'test-user-homework'@'%' |
    +-----------------------------------------------------------------+
    2 rows in set (0.00 sec)
