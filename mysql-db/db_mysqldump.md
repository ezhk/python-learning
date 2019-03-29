# Dump database

    # mysqldump --single-transaction --triggers --routines  --set-gtid-purged=OFF -uroot employees >employees.sql
    # mysql -uroot -e'CREATE DATABASE `employees-new`; USE `employees-new`; SHOW TABLES;'

# Retore database 

    # cat employees.sql | mysql -uroot -D employees-new
    # mysql -uroot -e'USE `employees-new`; SHOW TABLES;'
    +-------------------------+
    | Tables_in_employees-new |
    +-------------------------+
    | departments             |
    | dept_bonus              |
    | dept_emp                |
    | dept_manager            |
    | employees               |
    | salaries                |
    | titles                  |
    +-------------------------+
