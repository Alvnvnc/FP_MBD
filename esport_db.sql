-- MariaDB dump 10.19-11.3.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: esport_db
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Event`
--

DROP TABLE IF EXISTS `Event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Event` (
  `Event_ID` char(6) NOT NULL,
  `Jenis_Event` varchar(30) DEFAULT NULL,
  `Tanggal_Event` date DEFAULT NULL,
  `Deskripsi_Event` varchar(20) DEFAULT NULL,
  `Schedule_Schedule_ID` char(6) DEFAULT NULL,
  PRIMARY KEY (`Event_ID`),
  KEY `Schedule_Schedule_ID` (`Schedule_Schedule_ID`),
  CONSTRAINT `Event_ibfk_1` FOREIGN KEY (`Schedule_Schedule_ID`) REFERENCES `Schedule` (`Schedule_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Event`
--

LOCK TABLES `Event` WRITE;
/*!40000 ALTER TABLE `Event` DISABLE KEYS */;
INSERT INTO `Event` VALUES
('E001','Match','2024-06-22','Quarter Finals','SC001'),
('E002','Match','2024-07-02','Semi Finals','SC002'),
('E003','Match','2024-07-06','Finals','SC003');
/*!40000 ALTER TABLE `Event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Player`
--

DROP TABLE IF EXISTS `Player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Player` (
  `Player_ID` char(6) NOT NULL,
  `Nama` varchar(50) DEFAULT NULL,
  `Umur` int(11) DEFAULT NULL,
  `Email` varchar(30) DEFAULT NULL,
  `Detail_Player` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Player_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Player`
--

LOCK TABLES `Player` WRITE;
/*!40000 ALTER TABLE `Player` DISABLE KEYS */;
INSERT INTO `Player` VALUES
('P001','Alice',25,'alice@example.com','Mobile Legends/Marksman'),
('P002','Bob',30,'bob@example.com','Mobile Legends/Tank'),
('P003','Charlie',22,'charlie@example.com','Dota 2/Carry'),
('P004','Dave',28,'dave@example.com','Dota 2/Support'),
('P005','Eve',26,'eve@example.com','CS:GO/Sniper');
/*!40000 ALTER TABLE `Player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Player_Team`
--

DROP TABLE IF EXISTS `Player_Team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Player_Team` (
  `Player_Player_ID` char(6) NOT NULL,
  `Team_Team_ID` char(6) NOT NULL,
  PRIMARY KEY (`Player_Player_ID`,`Team_Team_ID`),
  KEY `Team_Team_ID` (`Team_Team_ID`),
  CONSTRAINT `Player_Team_ibfk_1` FOREIGN KEY (`Player_Player_ID`) REFERENCES `Player` (`Player_ID`),
  CONSTRAINT `Player_Team_ibfk_2` FOREIGN KEY (`Team_Team_ID`) REFERENCES `Team` (`Team_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Player_Team`
--

LOCK TABLES `Player_Team` WRITE;
/*!40000 ALTER TABLE `Player_Team` DISABLE KEYS */;
INSERT INTO `Player_Team` VALUES
('P001','T001'),
('P002','T001'),
('P003','T002'),
('P004','T002'),
('P005','T003');
/*!40000 ALTER TABLE `Player_Team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Salary`
--

DROP TABLE IF EXISTS `Salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Salary` (
  `Salary_ID` char(6) NOT NULL,
  `Jumlah_Pembayar` decimal(10,2) DEFAULT NULL,
  `Tanggal_Pembayar` date DEFAULT NULL,
  `Deskripsi` varchar(150) DEFAULT NULL,
  `Player_Player_ID` char(6) DEFAULT NULL,
  PRIMARY KEY (`Salary_ID`),
  KEY `Player_Player_ID` (`Player_Player_ID`),
  CONSTRAINT `Salary_ibfk_1` FOREIGN KEY (`Player_Player_ID`) REFERENCES `Player` (`Player_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Salary`
--

LOCK TABLES `Salary` WRITE;
/*!40000 ALTER TABLE `Salary` DISABLE KEYS */;
INSERT INTO `Salary` VALUES
('S001',5000.00,'2024-01-01','Monthly Salary','P001'),
('S002',6000.00,'2024-01-01','Monthly Salary','P002'),
('S003',7000.00,'2024-01-01','Monthly Salary','P003'),
('S004',8000.00,'2024-01-01','Monthly Salary','P004'),
('S005',9000.00,'2024-01-01','Monthly Salary','P005');
/*!40000 ALTER TABLE `Salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Schedule`
--

DROP TABLE IF EXISTS `Schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Schedule` (
  `Schedule_ID` char(6) NOT NULL,
  `Jenis_Kegiatan` varchar(50) DEFAULT NULL,
  `Tanggal_Kegiatan` date DEFAULT NULL,
  `Waktu_Mulai` time DEFAULT NULL,
  `Waktu_Selesai` time DEFAULT NULL,
  `Team_Team_ID` char(6) DEFAULT NULL,
  PRIMARY KEY (`Schedule_ID`),
  KEY `Team_Team_ID` (`Team_Team_ID`),
  CONSTRAINT `Schedule_ibfk_1` FOREIGN KEY (`Team_Team_ID`) REFERENCES `Team` (`Team_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Schedule`
--

LOCK TABLES `Schedule` WRITE;
/*!40000 ALTER TABLE `Schedule` DISABLE KEYS */;
INSERT INTO `Schedule` VALUES
('SC001','Training','2024-06-21','08:00:00','10:00:00','T001'),
('SC002','Match','2024-07-01','14:00:00','16:00:00','T002'),
('SC003','Training','2024-07-05','09:00:00','11:00:00','T003');
/*!40000 ALTER TABLE `Schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sponsor`
--

DROP TABLE IF EXISTS `Sponsor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sponsor` (
  `Sponsor_ID` char(6) NOT NULL,
  `Nama_Sponsor` varchar(50) DEFAULT NULL,
  `Kontak_Sponsor` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Sponsor_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sponsor`
--

LOCK TABLES `Sponsor` WRITE;
/*!40000 ALTER TABLE `Sponsor` DISABLE KEYS */;
INSERT INTO `Sponsor` VALUES
('SP001','Sponsor A','contact@sponsorA.com'),
('SP002','Sponsor B','contact@sponsorB.com'),
('SP003','Sponsor C','contact@sponsorC.com');
/*!40000 ALTER TABLE `Sponsor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sponsor_Team`
--

DROP TABLE IF EXISTS `Sponsor_Team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sponsor_Team` (
  `Sponsor_ID` char(6) NOT NULL,
  `Team_ID` char(6) NOT NULL,
  PRIMARY KEY (`Sponsor_ID`,`Team_ID`),
  KEY `Team_ID` (`Team_ID`),
  CONSTRAINT `Sponsor_Team_ibfk_1` FOREIGN KEY (`Sponsor_ID`) REFERENCES `Sponsor` (`Sponsor_ID`),
  CONSTRAINT `Sponsor_Team_ibfk_2` FOREIGN KEY (`Team_ID`) REFERENCES `Team` (`Team_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sponsor_Team`
--

LOCK TABLES `Sponsor_Team` WRITE;
/*!40000 ALTER TABLE `Sponsor_Team` DISABLE KEYS */;
INSERT INTO `Sponsor_Team` VALUES
('SP001','T001'),
('SP002','T002'),
('SP003','T003');
/*!40000 ALTER TABLE `Sponsor_Team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Team`
--

DROP TABLE IF EXISTS `Team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Team` (
  `Team_ID` char(6) NOT NULL,
  `Nama_Tim` varchar(30) DEFAULT NULL,
  `Pelatih` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Team_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Team`
--

LOCK TABLES `Team` WRITE;
/*!40000 ALTER TABLE `Team` DISABLE KEYS */;
INSERT INTO `Team` VALUES
('T001','Team A','Coach A'),
('T002','Team B','Coach B'),
('T003','Team C','Coach C');
/*!40000 ALTER TABLE `Team` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-27  9:43:19
