-- MySQL dump 10.13  Distrib 5.5.40, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: final
-- ------------------------------------------------------
-- Server version	5.5.40-0ubuntu0.14.04.1

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
-- Table structure for table `Evidence`
--

DROP TABLE IF EXISTS `Evidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Evidence` (
  `AI_Evidence` int(11) NOT NULL AUTO_INCREMENT,
  `EvidenceCode` varchar(45) DEFAULT NULL,
  `FK_Protein_GO` int(11) DEFAULT NULL,
  `OnDate` date DEFAULT NULL,
  PRIMARY KEY (`AI_Evidence`),
  KEY `fk_Evidence_Describes1_idx` (`FK_Protein_GO`),
  CONSTRAINT `fk_Evidence_Describes1` FOREIGN KEY (`FK_Protein_GO`) REFERENCES `Protein_GO` (`AI_Protein_GO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GO`
--

DROP TABLE IF EXISTS `GO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GO` (
  `AI_GO` int(11) NOT NULL AUTO_INCREMENT,
  `GO_id` varchar(45) DEFAULT NULL,
  `GO_Term` varchar(200) DEFAULT NULL,
  `GO_Domain` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`AI_GO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Protein`
--

DROP TABLE IF EXISTS `Protein`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Protein` (
  `AI_Protein` int(11) NOT NULL AUTO_INCREMENT,
  `EntryName` varchar(45) DEFAULT NULL,
  `Accession` varchar(45) DEFAULT NULL,
  `CAFA_ID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`AI_Protein`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Protein_GO`
--

DROP TABLE IF EXISTS `Protein_GO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Protein_GO` (
  `AI_Protein_GO` int(11) NOT NULL AUTO_INCREMENT,
  `FK_Protein` int(11) NOT NULL,
  `FK_GO` int(11) NOT NULL,
  PRIMARY KEY (`AI_Protein_GO`,`FK_Protein`,`FK_GO`),
  KEY `fk_Describes_Protein1_idx` (`FK_Protein`),
  KEY `fk_Describes_Ontological_Domains1_idx` (`FK_GO`),
  CONSTRAINT `fk_Describes_Protein1` FOREIGN KEY (`FK_Protein`) REFERENCES `Protein` (`AI_Protein`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Describes_Ontological_Domains1` FOREIGN KEY (`FK_GO`) REFERENCES `GO` (`AI_GO`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-29 15:29:06
