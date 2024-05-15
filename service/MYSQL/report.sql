SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `report`;




CREATE TABLE `report`  (
    `id`int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `createDate` datetime NULL COMMENT '创建时间',
  `updataDate` datetime NULL COMMENT '更新时间',
  `updateUser` varchar(20) NULL COMMENT '修改人',
  `test_desc` varchar(2000) NULL COMMENT '结论描述',
  `test_risks` varchar(2000) NULL COMMENT '风险提示',
  `test_cases` varchar(2000) NULL COMMENT '测试用例描述',
  `test_bugs` varchar(1000) NULL COMMENT '缺陷列表',
  `test_file` varchar(255) NULL COMMENT '附件文件地址',
  `test_note` varchar(1000) NULL COMMENT '报告备注',
  `test_email` varchar(1) NULL COMMENT '是否发送消息，0未操作，1成功，2失败',
    PRIMARY KEY (`id`)  
)ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;