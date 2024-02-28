
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for history_trade_table
-- ----------------------------
DROP TABLE IF EXISTS `history_trade_table`;
CREATE TABLE `history_trade_table`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trade_price` double NOT NULL,
  `trade_shares` int(11) NOT NULL,
  `trade_time` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stock_id_id` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id_id` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `history_trade_table_stock_id_id_b0518014_fk_stock_info_stock_id`(`stock_id_id`) USING BTREE,
  INDEX `history_trade_table_user_id_id_522fcde1_fk_user_tabl`(`user_id_id`) USING BTREE,
  CONSTRAINT `history_trade_table_stock_id_id_b0518014_fk_stock_info_stock_id` FOREIGN KEY (`stock_id_id`) REFERENCES `stock_info` (`stock_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `history_trade_table_user_id_id_522fcde1_fk_user_tabl` FOREIGN KEY (`user_id_id`) REFERENCES `user_table` (`phone_number`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


INSERT INTO `history_trade_table` VALUES (1, 17.08, 10, '2024-02-27', '000001', '19959008351');
INSERT INTO `history_trade_table` VALUES (2, 17.08, 25, '2024-02-27', '000001', '19959008351');
INSERT INTO `history_trade_table` VALUES (3, 31.54, 10, '2024-02-27', '000002', '19959008351');
INSERT INTO `history_trade_table` VALUES (4, 31.54, 30, '2024-02-27', '000002', '19959008351');
INSERT INTO `history_trade_table` VALUES (5, 17.12, 22, '2024-02-27', '000001', '19959008351');
INSERT INTO `history_trade_table` VALUES (6, 17.08, 12, '2024-02-27', '000001', '19959008351');
INSERT INTO `history_trade_table` VALUES (7, 17.15, 10, '2024-02-27', '000001', '19959008351');
INSERT INTO `history_trade_table` VALUES (8, 3.54, 3, '2024-02-27', '000010', '19959008351');
INSERT INTO `history_trade_table` VALUES (9, 17.15, -70, '22024-02-2718:45', '000001', '19959008351');
INSERT INTO `history_trade_table` VALUES (10, 17.15, -9, '2024-02-2718:47', '000001', '19959008351');

SET FOREIGN_KEY_CHECKS = 1;
