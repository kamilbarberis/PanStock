-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: panstock
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `panstock`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `panstock` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `panstock`;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activa` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `uq_categorias_nombre` (`nombre`),
  CONSTRAINT `chk_categorias_nombre` CHECK ((char_length(trim(`nombre`)) > 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Panadería','Panes y productos de panificación',1),(2,'Facturería','Facturas y productos de pastelería',1),(3,'Repostería','Tortas y productos dulces',1),(4,'Sandwichería','Sándwiches y productos salados',1),(5,'Bebidas','Bebidas para la venta',1),(6,'Golosinas',NULL,1);
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos`
--

DROP TABLE IF EXISTS `movimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos` (
  `id_movimiento` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `tipo_movimiento` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `observacion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_movimiento`),
  KEY `idx_movimientos_producto` (`id_producto`),
  KEY `idx_movimientos_fecha` (`fecha`),
  KEY `idx_movimientos_tipo_fecha` (`tipo_movimiento`,`fecha`),
  CONSTRAINT `fk_movimientos_productos` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_movimientos_cantidad` CHECK ((`cantidad` > 0)),
  CONSTRAINT `chk_movimientos_tipo` CHECK ((`tipo_movimiento` in (_utf8mb4'ENTRADA',_utf8mb4'SALIDA')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos`
--

LOCK TABLES `movimientos` WRITE;
/*!40000 ALTER TABLE `movimientos` DISABLE KEYS */;
INSERT INTO `movimientos` VALUES (1,1,'ENTRADA',30,'2026-10-01 08:00:00','Producción inicial'),(2,1,'SALIDA',12,'2026-10-01 10:00:00','Venta'),(3,2,'ENTRADA',15,'2026-10-01 08:30:00','Producción inicial'),(4,2,'SALIDA',12,'2026-10-01 11:00:00','Venta'),(5,3,'ENTRADA',25,'2026-10-01 09:00:00','Producción inicial'),(6,3,'SALIDA',20,'2026-10-01 12:00:00','Venta'),(7,4,'ENTRADA',5,'2026-10-01 09:30:00','Producción inicial'),(8,5,'ENTRADA',20,'2026-10-01 10:00:00','Preparación inicial'),(9,5,'SALIDA',8,'2026-10-01 13:00:00','Venta'),(10,6,'ENTRADA',18,'2026-10-01 10:30:00','Reposición');
/*!40000 ALTER TABLE `movimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock_minimo` int NOT NULL DEFAULT '5',
  `id_categoria` int NOT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `idx_productos_nombre` (`nombre`),
  KEY `idx_productos_categoria` (`id_categoria`),
  CONSTRAINT `fk_productos_categorias` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_productos_nombre` CHECK ((char_length(trim(`nombre`)) > 0)),
  CONSTRAINT `chk_productos_precio` CHECK ((`precio` >= 0)),
  CONSTRAINT `chk_productos_stock_minimo` CHECK ((`stock_minimo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Pan francés','Pan tradicional',1800.00,10,1),(2,'Criollos','Criollos salados',3500.00,5,2),(3,'Medialunas','Medialunas de manteca',5000.00,20,2),(4,'Torta selva negra','Torta de chocolate',18000.00,2,3),(5,'Sándwich de miga','Sándwich de jamón y tomate',2500.00,8,4),(6,'Gaseosa','Botella de gaseosa',2200.00,6,5),(7,'Pan integral','Pan elaborado con harina integral',2400.00,5,1),(8,'Bizcochos','Bizcochos salados',3000.00,8,2),(9,'Alfajores','Alfajores de chocolate',1600.00,100,3),(10,'Jugo','Jugo en botella',1900.00,5,5);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'panstock'
--
