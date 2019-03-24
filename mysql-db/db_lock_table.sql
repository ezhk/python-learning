--- first terminal
LOCK TABLE `_cities` READ;

--- second terminal
DELETE FROM `_cities` WHERE `title` = 'Buenos Aires';
--- no output

--- first terminal
UNLOCK TABLES;

--- second terminal
Query OK, 149 rows affected (2.51 sec)

