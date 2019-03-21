USE `employees`;

DROP TRIGGER IF EXISTS `first_entrance_salary`;
DELETE FROM `employees`
WHERE
    `employees`.`emp_no` = 10000;
DELETE FROM `salaries`
WHERE
    `salaries`.`emp_no` = 10000;

delimiter //
CREATE TRIGGER `first_entrance_salary`
AFTER INSERT
ON `employees` FOR EACH ROW
BEGIN
	INSERT INTO `salaries` (`emp_no`, `salary`, `from_date`, `to_date`)
		VALUES (NEW.`emp_no`, 50000, CURDATE(), CURDATE());
END;//
delimiter ;

SHOW TRIGGERS;
SELECT sleep(3);
INSERT INTO `employees` (`emp_no`, `birth_date`, `first_name`, `last_name`, `gender`, `hire_date`)
	VALUES (10000, '1970-01-01', 'Robotic', 'Automation', 'M', CURDATE());

SELECT
    *
FROM
    `employees`
        LEFT JOIN
    `salaries` ON `employees`.`emp_no` = `salaries`.`emp_no`
WHERE
    `employees`.`emp_no` = 10000;
