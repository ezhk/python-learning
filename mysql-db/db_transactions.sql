--------------------------------
--- CHECK TRANSACTIONS LOGIC ---
--------------------------------

--- first terminal
SET AUTOCOMMIT = 0;
UPDATE `salaries` SET `salary` = 987654321 WHERE `emp_no` = 10001 AND `to_date` > CURDATE();
START TRANSACTION;

--- second terminal
SET AUTOCOMMIT = 0;
START TRANSACTION;
SELECT SUM(`salaries`.salary) AS 'summary_salary', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` ORDER BY `dept_emp`.`dept_no`;
+----------------+---------+
| summary_salary | dept_no |
+----------------+---------+
|     1188233434 | d001    |
|      977049936 | d002    |
|      824464664 | d003    |
|     3616319369 | d004    |
|     5140814413 | d005    |
|      951919236 | d006    |
|     3349845802 | d007    |
|     1048650423 | d008    |
|     1182134209 | d009    |
+----------------+---------+
9 rows in set (1.00 sec)

--- first terminal
UPDATE `salaries` SET `salary` = 50000 WHERE `emp_no` = 10001 AND `to_date` > CURDATE();
COMMIT;

--- second terminal
SELECT SUM(`salaries`.salary) AS 'summary_salary', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` ORDER BY `dept_emp`.`dept_no`;
+----------------+---------+
| summary_salary | dept_no |
+----------------+---------+
|     1188233434 | d001    |
|      977049936 | d002    |
|      824464664 | d003    |
|     3616319369 | d004    |
|     5140814413 | d005    |
|      951919236 | d006    |
|     3349845802 | d007    |
|     1048650423 | d008    |
|     1182134209 | d009    |
+----------------+---------+
9 rows in set (1.00 sec)
--- VALUE DEPT 005 doesn't change: 5140814413
COMMIT;
SELECT SUM(`salaries`.salary) AS 'summary_salary', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` ORDER BY `dept_emp`.`dept_no`;
+----------------+---------+
| summary_salary | dept_no |
+----------------+---------+
|     1188233434 | d001    |
|      977049936 | d002    |
|      824464664 | d003    |
|     3616319369 | d004    |
|     4153210092 | d005    |
|      951919236 | d006    |
|     3349845802 | d007    |
|     1048650423 | d008    |
|     1182134209 | d009    |
+----------------+---------+
9 rows in set (1.00 sec)
--- VALUE DEPT 005 has changed: 4153210092



----------------------------------
--- GET BONUSES TO DEPARTMENTS ---
----------------------------------

mysql> SELECT SUM(`salaries`.salary) AS 'summary_salary', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` ORDER BY `dept_emp`.`dept_no`;
+----------------+---------+
| summary_salary | dept_no |
+----------------+---------+
|     1188233434 | d001    |
|      977049936 | d002    |
|      824464664 | d003    |
|     3616319369 | d004    |
|     4153210092 | d005    |
|      951919236 | d006    |
|     3349845802 | d007    |
|     1048650423 | d008    |
|     1182134209 | d009    |
+----------------+---------+
9 rows in set (1.06 sec)

START TRANSACTION;
CREATE TABLE IF NOT EXISTS `dept_bonus` (`id` INT AUTO_INCREMENT, `value` INT, `dept_no` VARCHAR(4), `date` DATETIME DEFAULT NOW(), PRIMARY KEY(`id`));
SET @avg_salary = (SELECT SUM(`salaries`.salary) AS 'summary_salary' FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE()) / (SELECT COUNT(*) FROM `departments`);

SELECT @avg_salary;
+----------------------+
| @avg_salary          |
+----------------------+
| 1921314129.444444444 |
+----------------------+
1 row in set (0.00 sec)

SELECT SUM(`salaries`.salary) - @avg_salary AS 'bonus', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` HAVING `bonus` > 0;
+-------------------------------------------+---------+
| bonus                                     | dept_no |
+-------------------------------------------+---------+
| 1695005239.555555556000000000000000000000 | d004    |
| 2231895962.555555556000000000000000000000 | d005    |
| 1428531672.555555556000000000000000000000 | d007    |
+-------------------------------------------+---------+
3 rows in set (1.00 sec)

--- Insert department bonus

ALTER TABLE `dept_bonus` MODIFY `value` DOUBLE;
Query OK, 0 rows affected (0.08 sec)
Records: 0  Duplicates: 0  Warnings: 0

INSERT INTO `dept_bonus` (`value`, `dept_no`) (SELECT SUM(`salaries`.salary) - @avg_salary AS 'bonus', `dept_emp`.`dept_no` FROM `salaries` INNER JOIN `dept_emp` ON `dept_emp`.`emp_no` = `salaries`.`emp_no` WHERE `salaries`.to_date > CURDATE() AND `dept_emp`.`to_date` > CURDATE() GROUP BY `dept_emp`.`dept_no` HAVING `bonus` > 0);
Query OK, 3 rows affected (1.68 sec)
Records: 3  Duplicates: 0  Warnings: 0

SELECT * FROM `dept_bonus`;
+----+--------------------+---------+---------------------+
| id | value              | dept_no | date                |
+----+--------------------+---------+---------------------+
|  3 | 1695005239.5555556 | d004    | 2019-03-24 22:38:19 |
|  4 | 2231895962.5555553 | d005    | 2019-03-24 22:38:19 |
|  5 | 1428531672.5555556 | d007    | 2019-03-24 22:38:19 |
+----+--------------------+---------+---------------------+
3 rows in set (0.00 sec)

COMMIT;
