/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50709
Source Host           : 127.0.0.1:3306
Source Database       : property_system_dev

Target Server Type    : MYSQL
Target Server Version : 50709
File Encoding         : 65001

Date: 2017-06-10 01:28:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for authorizations
-- ----------------------------
DROP TABLE IF EXISTS `authorizations`;
CREATE TABLE `authorizations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_hash` varchar(255) NOT NULL,
  `authorizer_username` varchar(255) NOT NULL,
  `authorized_username` varchar(255) NOT NULL,
  `type` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `txhash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `file_hash` (`file_hash`),
  KEY `authorizer_username` (`authorizer_username`),
  KEY `authorized_username` (`authorized_username`),
  CONSTRAINT `authorizations_ibfk_1` FOREIGN KEY (`file_hash`) REFERENCES `files` (`hash`),
  CONSTRAINT `authorizations_ibfk_2` FOREIGN KEY (`authorizer_username`) REFERENCES `users` (`username`),
  CONSTRAINT `authorizations_ibfk_3` FOREIGN KEY (`authorized_username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for files
-- ----------------------------
DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
  `hash` varchar(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(255) DEFAULT NULL,
  `owner` varchar(255) NOT NULL,
  `txhash` varchar(255) NOT NULL,
  `for_sell` tinyint(1) NOT NULL,
  `price` float DEFAULT NULL,
  PRIMARY KEY (`hash`),
  KEY `owner` (`owner`),
  CONSTRAINT `files_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `seller` varchar(255) NOT NULL,
  `buyer` varchar(255) NOT NULL,
  `txhash` varchar(255) NOT NULL,
  `money` float NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `file_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `seller` (`seller`),
  KEY `buyer` (`buyer`),
  KEY `file_hash` (`file_hash`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`seller`) REFERENCES `users` (`username`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`buyer`) REFERENCES `users` (`username`),
  CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`file_hash`) REFERENCES `files` (`hash`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for transfers
-- ----------------------------
DROP TABLE IF EXISTS `transfers`;
CREATE TABLE `transfers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_hash` varchar(255) NOT NULL,
  `from_username` varchar(255) NOT NULL,
  `to_username` varchar(255) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `txhash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `file_hash` (`file_hash`),
  KEY `from_username` (`from_username`),
  KEY `to_username` (`to_username`),
  CONSTRAINT `transfers_ibfk_1` FOREIGN KEY (`file_hash`) REFERENCES `files` (`hash`),
  CONSTRAINT `transfers_ibfk_2` FOREIGN KEY (`from_username`) REFERENCES `users` (`username`),
  CONSTRAINT `transfers_ibfk_3` FOREIGN KEY (`to_username`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `role` int(11) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for wallets
-- ----------------------------
DROP TABLE IF EXISTS `wallets`;
CREATE TABLE `wallets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(255) NOT NULL,
  `key` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `owner` (`owner`),
  CONSTRAINT `wallets_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `users` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
