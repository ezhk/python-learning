DROP TABLE IF EXISTS `_cities`;
DROP TABLE IF EXISTS `_regions`;
DROP TABLE IF EXISTS `_countries`;


CREATE TABLE IF NOT EXISTS `_countries` (
	`id`	INT		NOT NULL AUTO_INCREMENT,
	`title`	VARCHAR(150)	NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `title_idx` (`title`)
);

CREATE TABLE IF NOT EXISTS `_regions` (
	`id`		INT		NOT NULL AUTO_INCREMENT,
	`country_id`	INT		NOT NULL,
	`title`		VARCHAR(150)	NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `title_idx` (`title`),
	CONSTRAINT `regions_country_fk`
		FOREIGN KEY (`country_id`)
		REFERENCES `_countries` (`id`)
			ON DELETE CASCADE
			ON UPDATE CASCADE
		
);

CREATE TABLE IF NOT EXISTS `_cities` (
	`id`		INT		NOT NULL AUTO_INCREMENT,
	`country_id`	INT		NOT NULL,
	`important`	TINYINT(1)	NOT NULL,
	`region_id`	INT		NOT NULL,
	`title`		VARCHAR(150)	NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `title_idx` (`title`),
	CONSTRAINT `cities_country_fk`
		FOREIGN KEY (`country_id`)
		REFERENCES `_countries` (`id`)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
	CONSTRAINT `cities_region_fk`
		FOREIGN KEY (`region_id`)
		REFERENCES `_regions` (`id`)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

