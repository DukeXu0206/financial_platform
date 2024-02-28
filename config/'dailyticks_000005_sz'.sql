
 SET NAMES utf8mb4 ;

DROP TABLE IF EXISTS `'dailyticks_000005_sz'`;

 SET character_set_client = utf8mb4 ;
CREATE TABLE `'dailyticks_000005_sz'` (
  `DAILY_TICKS` varchar(64) DEFAULT NULL,
  `REAL_TIME_QUOTES` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


LOCK TABLES `'dailyticks_000005_sz'` WRITE;

INSERT INTO `'dailyticks_000005_sz'` VALUES ('10:18:12',3.16),('11:10:45',3.17),('11:13:42',3.17),('11:16:45',3.17),('11:19:36',3.16),('11:23:06',3.16),('11:26:06',3.16),('11:28:57',3.16),('13:00:09',3.16),('13:03:27',3.16),('13:08:36',3.17),('13:13:09',3.17),('13:18:00',3.18),('13:22:57',3.18),('13:28:42',3.17),('13:34:09',3.17),('13:40:18',3.17),('13:45:06',3.17),('13:50:03',3.18),('13:53:21',3.18),('13:56:30',3.17),('13:59:39',3.17),('14:02:48',3.17),('14:05:57',3.18),('14:09:12',3.18),('14:12:39',3.19),('14:16:03',3.18),('14:19:33',3.19),('14:22:57',3.2),('14:26:24',3.21),('14:29:54',3.2),('14:32:57',3.19),('14:36:06',3.2),('14:39:12',3.2),('14:42:12',3.2),('14:45:00',3.19),('14:48:06',3.2),('14:50:48',3.2),('14:53:27',3.2),('14:56:09',3.2),('14:58:48',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2),('15:00:03',3.2);

UNLOCK TABLES;

