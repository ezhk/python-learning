USE `geodata`;

DROP VIEW IF EXISTS `cities_view`;
CREATE VIEW `cities_view` AS
    SELECT
        `_cities`.`title` AS `city`,
        `_regions`.`title` AS `region`,
        `_countries`.`title` AS `country`
    FROM
        `_cities`
            INNER JOIN
        `_countries` ON `_cities`.`country_id` = `_countries`.`id`
            LEFT JOIN
        `_regions` ON `_cities`.`region_id` = `_regions`.`id`;

DROP VIEW IF EXISTS `moscow_regions_view`;
CREATE VIEW `moscow_regions_view` AS
    SELECT
        `_cities`.`title` AS `city`,
        `_regions`.`title` AS `region`,
        `_countries`.`title` AS `country`
    FROM
        `_cities`
            INNER JOIN
        `_countries` ON `_cities`.`country_id` = `_countries`.`id`
            LEFT JOIN
        `_regions` ON `_cities`.`region_id` = `_regions`.`id`
    WHERE
        `_countries`.`title` = 'Россия'
            AND `_regions`.`title` LIKE 'Московская%';

---
--- Warning, it's heavy request
--- try LIMIT for view presentation
---
SELECT * FROM `cities_view`
UNION
SELECT * FROM `moscow_regions_view`;
