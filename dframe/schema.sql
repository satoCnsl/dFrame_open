DROP TABLE IF EXISTS `__account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `__account` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `roleID` int NOT NULL,
  `modifiedBy` varchar(45) DEFAULT NULL,
  `modifiedAt` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `createdAt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `__account`
--

LOCK TABLES `__account` WRITE;
/*!40000 ALTER TABLE `__account` DISABLE KEYS */;
INSERT INTO `__account` VALUES (1,'admin','admin@test.jp','pbkdf2:sha256:260000$5eruvNGm2AEEIXaL$bd15dfff8faf9037301856e6fa25a03a5976941ffb5cc25a444eb0fdc0c8335c',1,'1','2023-12-10 14:37:31',NULL),(2,'テスト　ABC','ichi@test.jp','pbkdf2:sha256:260000$604yogwDSXYevaFM$e051a52d7ae6bf36be6e1c3e096225b7223b2510d2577c99a704c5e097298765',2,'1','2023-12-11 11:17:26','2023-12-10 14:36:45');
/*!40000 ALTER TABLE `__account` ENABLE KEYS */;
UNLOCK TABLES;
