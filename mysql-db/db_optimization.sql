EXPLAIN SELECT SUM(`salaries`.salary) - @avg_salary AS 'bonus', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` HAVING `bonus` > 0;
+----+-------------+----------+------------+------+------------------------+---------+---------+---------------------------+--------+----------+----------------------------------------------+
| id | select_type | table    | partitions | type | possible_keys          | key     | key_len | ref                       | rows   | filtered | Extra                                        |
+----+-------------+----------+------------+------+------------------------+---------+---------+---------------------------+--------+----------+----------------------------------------------+
|  1 | SIMPLE      | dept_emp | NULL       | ALL  | PRIMARY,emp_no,dept_no | NULL    | NULL    | NULL                      | 331570 |    33.33 | Using where; Using temporary; Using filesort |
|  1 | SIMPLE      | salaries | NULL       | ref  | PRIMARY,emp_no         | PRIMARY | 4       | employees.dept_emp.emp_no |      9 |    33.33 | Using where                                  |
+----+-------------+----------+------------+------+------------------------+---------+---------+---------------------------+--------+----------+----------------------------------------------+
2 rows in set, 1 warning (0.00 sec)


ALTER TABLE `dept_emp` ADD INDEX (`to_date`);
Query OK, 0 rows affected (0.31 sec)
Records: 0  Duplicates: 0  Warnings: 0


EXPLAIN SELECT SUM(`salaries`.salary) - @avg_salary AS 'bonus', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` HAVING `bonus` > 0;
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+-----------------------------------------------------------+
| id | select_type | table    | partitions | type  | possible_keys                  | key     | key_len | ref                       | rows   | filtered | Extra                                                     |
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+-----------------------------------------------------------+
|  1 | SIMPLE      | dept_emp | NULL       | range | PRIMARY,emp_no,dept_no,to_date | to_date | 3       | NULL                      | 165785 |   100.00 | Using where; Using index; Using temporary; Using filesort |
|  1 | SIMPLE      | salaries | NULL       | ref   | PRIMARY,emp_no                 | PRIMARY | 4       | employees.dept_emp.emp_no |      9 |    33.33 | Using where                                               |
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+-----------------------------------------------------------+
2 rows in set, 1 warning (0.00 sec)

--- HAVE GOT BOOST FOR dept_emp,TRY TO SPEED UP salary

ALTER TABLE `salaries` ADD INDEX (`to_date`);
Query OK, 0 rows affected (3.12 sec)
Records: 0  Duplicates: 0  Warnings: 0

EXPLAIN SELECT SUM(`salaries`.salary) - @avg_salary AS 'bonus', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.`to_date` > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` HAVING `bonus` > 0;
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+-----------------------------------------------------------+
| id | select_type | table    | partitions | type  | possible_keys                  | key     | key_len | ref                       | rows   | filtered | Extra                                                     |
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+-----------------------------------------------------------+
|  1 | SIMPLE      | dept_emp | NULL       | range | PRIMARY,emp_no,dept_no,to_date | to_date | 3       | NULL                      | 165785 |   100.00 | Using where; Using index; Using temporary; Using filesort |
|  1 | SIMPLE      | salaries | NULL       | ref   | PRIMARY,emp_no,to_date         | PRIMARY | 4       | employees.dept_emp.emp_no |      9 |    17.05 | Using where                                               |
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+-----------------------------------------------------------+
2 rows in set, 1 warning (0.00 sec)

--- USE FORCE INDEX ---
EXPLAIN SELECT SUM(`salaries`.salary) - @avg_salary AS 'bonus', `dept_emp`.`dept_no` FROM `salaries` FORCE INDEX (`to_date`) INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.`to_date` > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` HAVING `bonus` > 0;
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+--------------------------------------------------------+
| id | select_type | table    | partitions | type  | possible_keys                  | key     | key_len | ref                       | rows   | filtered | Extra                                                  |
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+--------------------------------------------------------+
|  1 | SIMPLE      | salaries | NULL       | range | to_date                        | to_date | 3       | NULL                      | 483860 |   100.00 | Using index condition; Using temporary; Using filesort |
|  1 | SIMPLE      | dept_emp | NULL       | ref   | PRIMARY,emp_no,dept_no,to_date | PRIMARY | 4       | employees.salaries.emp_no |      1 |    50.00 | Using where                                            |
+----+-------------+----------+------------+-------+--------------------------------+---------+---------+---------------------------+--------+----------+--------------------------------------------------------+
2 rows in set, 1 warning (0.00 sec)
