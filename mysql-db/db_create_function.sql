USE `employees`;

---
--- Function returns only one value, instead Procedure
--- F hasn't precompiled execution plan
--- F can be used into SQL queries (in P possible to use variables as output param)
---

DROP FUNCTION IF EXISTS `get_dept_manager_id_by_name`;

CREATE FUNCTION `get_dept_manager_id_by_name` (firstname VARCHAR(14), lastname VARCHAR(16))
RETURNS INT
DETERMINISTIC
READS SQL DATA
RETURN (
	SELECT
		`dept_manager`.`emp_no`
	FROM
		`dept_manager`
			INNER JOIN
		`employees` ON `dept_manager`.`emp_no` = `employees`.`emp_no`
	WHERE
		`employees`.`first_name` = firstname
			AND `employees`.`last_name` = lastname
);

SELECT `get_dept_manager_id_by_name`('Isamu', 'Legleitner');
