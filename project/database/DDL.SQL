-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: cs361_final
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `Foods`
--

DROP TABLE IF EXISTS `Foods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Foods` (
  `foodId` int NOT NULL AUTO_INCREMENT,
  `foodName` varchar(45) NOT NULL,
  `carbohydrate` int NOT NULL,
  `fat` int NOT NULL,
  `protein` int NOT NULL,
  PRIMARY KEY (`foodId`),
  UNIQUE KEY `foodName_UNIQUE` (`foodName`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `mealLogEntries`
--

DROP TABLE IF EXISTS `mealLogEntries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mealLogEntries` (
  `mealLogEntryId` int NOT NULL AUTO_INCREMENT,
  `mealDate` datetime NOT NULL,
  `mealNum` int NOT NULL,
  `mealLogs_mealLogId` int NOT NULL,
  `meals_mealId` int NOT NULL,
  PRIMARY KEY (`mealLogEntryId`),
  KEY `meals_mealId_idx` (`meals_mealId`),
  CONSTRAINT `mealId` FOREIGN KEY (`meals_mealId`) REFERENCES `Meals` (`mealId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `MealLogs`
--

DROP TABLE IF EXISTS `MealLogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MealLogs` (
  `mealLogId` int NOT NULL AUTO_INCREMENT,
  `users_userId` int NOT NULL,
  `mealLogEntries_mealLogEntryId` int DEFAULT NULL,
  PRIMARY KEY (`mealLogId`),
  KEY `users_userId_idx` (`users_userId`),
  KEY `mealLogEntryId_idx` (`mealLogEntries_mealLogEntryId`),
  CONSTRAINT `mealLogEntryId` FOREIGN KEY (`mealLogEntries_mealLogEntryId`) REFERENCES `mealLogEntries` (`mealLogEntryId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `users_userId` FOREIGN KEY (`users_userId`) REFERENCES `Users` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Meals`
--

DROP TABLE IF EXISTS `Meals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Meals` (
  `mealId` int NOT NULL AUTO_INCREMENT,
  `totalCalories` int DEFAULT NULL,
  `foods_foodId` int NOT NULL,
  PRIMARY KEY (`mealId`),
  KEY `foods_foodId_idx` (`foods_foodId`),
  CONSTRAINT `foods_foodId` FOREIGN KEY (`foods_foodId`) REFERENCES `Foods` (`foodId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `height` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `suggested_calories` int DEFAULT NULL,
  `mealLogs_mealLogId` int DEFAULT NULL,
  PRIMARY KEY (`userId`),
  KEY `mealLogs_mealLogId_idx` (`mealLogs_mealLogId`),
  CONSTRAINT `mealLogs_mealLogId` FOREIGN KEY (`mealLogs_mealLogId`) REFERENCES `MealLogs` (`mealLogId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data
--


INSERT INTO `Foods` VALUES (1,'beef',0,8,23);

INSERT INTO `Meals` VALUES (1,180,1);

INSERT INTO `mealLogEntries` VALUES (1,'2022-11-27 19:51:09',1,1,1);

INSERT INTO `MealLogs` VALUES (1,1,NULL),(2,1,1);

INSERT INTO `Users` VALUES (1,'joe','test@gmail.com','1234',NULL,NULL,NULL,NULL,NULL);
--



/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-27 20:02:24
