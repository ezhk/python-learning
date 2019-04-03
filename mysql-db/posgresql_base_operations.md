# Install and create user

    # apt-get install postgresql-11
    # su - postgres
    $ createuser --interactive --pwprompt
        Enter name of role to add: root
        Enter password for new role:
        Enter it again:
        Shall the new role be a superuser? (y/n) y

    $ psql
    psql (11.2 (Ubuntu 11.2-1.pgdg18.04+1))

    postgres=# \du
     postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
     root      | Superuser, Create role, Create DB                          | {}

Добавим пользователю прав на репликацию:

    postgres=# ALTER USER root WITH Replication;
    ALTER ROLE
    postgres=# \du
     postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
     root      | Superuser, Create role, Create DB, Replication             | {}

# Create and switch into schema

    postgres=# CREATE SCHEMA test;
    CREATE SCHEMA
    postgres=# SET search_path TO test;
    SET

# Custom data types and table
В postresql нет по умолчанию ENUM, но ничто не мешает нам его создать

    postgres=# CREATE TYPE gender_type AS ENUM ('M', 'F');
    CREATE TYPE

    postgres=# CREATE TABLE auth_data (
        id serial,
        username user_params NOT NULL,
        last_login timestamp default NOW()
    );
    CREATE TABLE

    postgres=# \d+
                                 List of relations
     Schema |       Name       |   Type   |  Owner   |    Size    | Description 
    --------+------------------+----------+----------+------------+-------------
     test   | auth_data        | table    | postgres | 16 kB      | 
     test   | auth_data_id_seq | sequence | postgres | 8192 bytes | 
    (2 rows)

# Insert and show data

    postgres=# INSERT INTO auth_data (username) VALUES (ROW('Test-user', 'Test-surname', 'M', 18));
    INSERT 0 1
    postgres=# SELECT * FROM auth_data;
      1 | (Test-user,Test-surname,M,18) | 2019-04-03 10:38:00.727525

# User auth and PgAdmin
Чтобы работать с пользователем, необходимо поправить main/pg_hba.conf:

    host    all             root            127.0.0.1/32            md5
    host    all             root            ::1/128                 md5

Проверяем, что нас пускает по паролю

    $ psql -h 127.0.0.1 --username=root -d postgres
    Password for user root:
    psql (11.2 (Ubuntu 11.2-1.pgdg18.04+1))
    SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
    Type "help" for help.

Устанавливаем админку

    $ sudo apt-get install pgadmin4

Profit.
