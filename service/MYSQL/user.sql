
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `username` varchar(80) DEFAULT NULL COMMENT '名字',
  `password` varchar(128) DEFAULT NULL COMMENT '密码',
  `email`  varchar(120) DEFAULT NULL COMMENT '邮箱',

  
  PRIMARY KEY (`id`),
  UNIQUE KEY `apps_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10020 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='应用管理';

SET FOREIGN_KEY_CHECKS = 1;
