-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: countries_and_cities
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cities`
--


DROP TABLE IF EXISTS `_cities`;
DROP TABLE IF EXISTS `_regions`;
DROP TABLE IF EXISTS `_countries`;


DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(256) NOT NULL,
  `id_country` int(11) NOT NULL,
  `id_region` int(11) NOT NULL,
  `id_district` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_idx` (`city_name`,`id_region`,`id_country`),
  KEY `fk_countries_idx` (`id_country`),
  KEY `fk_regions_idx` (`id_region`),
  KEY `fk_districts_idx` (`id_district`),
  CONSTRAINT `fk_countries` FOREIGN KEY (`id_country`) REFERENCES `coutries` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_districts` FOREIGN KEY (`id_district`) REFERENCES `districts` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_regions` FOREIGN KEY (`id_region`) REFERENCES `regions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
/*
INSERT INTO `cities` VALUES (1,'Moscow',1,1,NULL),(2,'Dmitrov',1,1,1);
*/
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coutries`
--

DROP TABLE IF EXISTS `coutries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coutries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `country_UNIQUE` (`country`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coutries`
--

LOCK TABLES `coutries` WRITE;
/*!40000 ALTER TABLE `coutries` DISABLE KEYS */;
/*
INSERT INTO `coutries` VALUES (1,'Russia');
*/
/*!40000 ALTER TABLE `coutries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `districts`
--

DROP TABLE IF EXISTS `districts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `districts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `district` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `district_UNIQUE` (`district`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `districts`
--

LOCK TABLES `districts` WRITE;
/*!40000 ALTER TABLE `districts` DISABLE KEYS */;
/*
INSERT INTO `districts` VALUES (1,'Dmitrovsky');
*/
/*!40000 ALTER TABLE `districts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regions`
--

DROP TABLE IF EXISTS `regions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `region_UNIQUE` (`region`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regions`
--

LOCK TABLES `regions` WRITE;
/*!40000 ALTER TABLE `regions` DISABLE KEYS */;
/*
INSERT INTO `regions` VALUES (1,'Moscow');
*/
/*!40000 ALTER TABLE `regions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-20 17:00:36


/*
	==================
	ALTERS STARTS HERE
	==================
*/


ALTER TABLE `cities`
	RENAME `_cities`,
	DROP KEY		`city_idx`,
	CHANGE COLUMN `city_name`	`title`		VARCHAR(150) NOT NULL,
	ADD INDEX `title_idx` (`title`),
	DROP FOREIGN KEY	`fk_countries`,
	DROP FOREIGN KEY	`fk_regions`,
	DROP FOREIGN KEY	`fk_districts`,
	CHANGE COLUMN `id_region`	`region_id`	INT NOT NULL,
	CHANGE COLUMN `id_country`	`country_id`	INT NOT NULL,
	DROP COLUMN `id_district`,
	ADD COLUMN `important`	TINYINT(1) NOT NULL
;

DROP TABLES `districts`;

ALTER TABLE `coutries`
	RENAME `_countries`,
	DROP KEY `country_UNIQUE`,
	MODIFY COLUMN `id` INT NOT NULL AUTO_INCREMENT,
	CHANGE COLUMN `country` `title`	VARCHAR(150) NOT NULL,
	ADD INDEX `title_idx` (`title`)
;

ALTER TABLE `regions`
	RENAME `_regions`,
	DROP KEY `region_UNIQUE`,
	CHANGE COLUMN `region` `title`	VARCHAR(150)	NOT NULL,
	ADD COLUMN `country_id` 	INT		NOT NULL,
	ADD INDEX `title_idx` (`title`),
	ADD CONSTRAINT `fk_regions_countries`
		FOREIGN KEY (`country_id`)
		REFERENCES `_countries` (`id`)
		ON DELETE CASCADE
		ON UPDATE CASCADE
;

ALTER TABLE `_cities`
	ADD CONSTRAINT `fk_cities_countries`
		FOREIGN KEY (`country_id`)
		REFERENCES `_countries` (`id`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	ADD CONSTRAINT `fk_cities_regions`
		FOREIGN KEY (`region_id`)
		REFERENCES `_regions` (`id`)
		ON DELETE CASCADE
		ON UPDATE CASCADE
;

