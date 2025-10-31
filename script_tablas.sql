CREATE DATABASE `prueba_tecnica` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `prueba_tecnica`;

CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text,
  `price` decimal(10,2) DEFAULT NULL,
  `category` text,
  `description` text,
  `fecha_insercion` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;