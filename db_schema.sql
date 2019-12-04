-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: drop_table_grades
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `conditions`
--

DROP TABLE IF EXISTS `conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conditions` (
  `cond_name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`cond_name`),
  UNIQUE KEY `cond_name_UNIQUE` (`cond_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conditions`
--

LOCK TABLES `conditions` WRITE;
/*!40000 ALTER TABLE `conditions` DISABLE KEYS */;
INSERT INTO `conditions` VALUES ('cond1','int'),('cond2','int'),('cond3','int');
/*!40000 ALTER TABLE `conditions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiment_conditions`
--

DROP TABLE IF EXISTS `experiment_conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiment_conditions` (
  `exp_id` varchar(45) NOT NULL,
  `cond_name` varchar(45) NOT NULL,
  `cond_val` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`exp_id`,`cond_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiment_conditions`
--

LOCK TABLES `experiment_conditions` WRITE;
/*!40000 ALTER TABLE `experiment_conditions` DISABLE KEYS */;
INSERT INTO `experiment_conditions` VALUES ('a','cond1','9'),('a','cond2','5'),('a','cond3','5'),('b','cond1','5'),('b','cond2','5'),('b','cond3','2'),('c','cond1','8'),('c','cond2','5'),('c','cond3','9'),('d','cond2','5');
/*!40000 ALTER TABLE `experiment_conditions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiment_measurements`
--

DROP TABLE IF EXISTS `experiment_measurements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiment_measurements` (
  `exp_id` varchar(45) NOT NULL,
  `meas_name` varchar(45) NOT NULL,
  `meas_val` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`exp_id`,`meas_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiment_measurements`
--

LOCK TABLES `experiment_measurements` WRITE;
/*!40000 ALTER TABLE `experiment_measurements` DISABLE KEYS */;
INSERT INTO `experiment_measurements` VALUES ('a','meas1','5'),('a','meas2','9'),('a','meas3','yes'),('a','meas4','0'),('b','meas1','5'),('b','meas2','4'),('b','meas3','no'),('b','meas4','0'),('d','meas1','2'),('d','meas3','yes');
/*!40000 ALTER TABLE `experiment_measurements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiments`
--

DROP TABLE IF EXISTS `experiments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiments` (
  `exp_id` varchar(45) NOT NULL,
  `seq_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`exp_id`),
  UNIQUE KEY `exp_id_UNIQUE` (`exp_id`),
  KEY `sequence_name_idx` (`seq_name`),
  CONSTRAINT `sequence_name` FOREIGN KEY (`seq_name`) REFERENCES `sequences` (`seq_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiments`
--

LOCK TABLES `experiments` WRITE;
/*!40000 ALTER TABLE `experiments` DISABLE KEYS */;
INSERT INTO `experiments` VALUES ('a','seq1'),('d','seq1'),('b','seq2'),('c','seq3'),('e','seq3');
/*!40000 ALTER TABLE `experiments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurements`
--

DROP TABLE IF EXISTS `measurements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `measurements` (
  `meas_name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`meas_name`),
  UNIQUE KEY `meas_name_UNIQUE` (`meas_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurements`
--

LOCK TABLES `measurements` WRITE;
/*!40000 ALTER TABLE `measurements` DISABLE KEYS */;
INSERT INTO `measurements` VALUES ('meas1','int'),('meas2','int'),('meas3','str'),('meas4','bool');
/*!40000 ALTER TABLE `measurements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sequences`
--

DROP TABLE IF EXISTS `sequences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sequences` (
  `seq_name` varchar(45) NOT NULL,
  `filename` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`seq_name`),
  UNIQUE KEY `seq_name_UNIQUE` (`seq_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sequences`
--

LOCK TABLES `sequences` WRITE;
/*!40000 ALTER TABLE `sequences` DISABLE KEYS */;
INSERT INTO `sequences` VALUES ('seq1',NULL,NULL),('seq2',NULL,NULL),('seq3',NULL,NULL);
/*!40000 ALTER TABLE `sequences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'drop_table_grades'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-04 17:27:51
