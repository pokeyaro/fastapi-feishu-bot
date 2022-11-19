/*
 Copy right (C)2022, Pokeya.

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 80029 (8.0.29)
 Source Host           : 127.0.0.1:3306
 Source Schema         : bot

 Target Server Type    : MySQL
 Target Server Version : 80029 (8.0.29)
 File Encoding         : 65001

 Date: 19/11/2022
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t-authinfo
-- ----------------------------
DROP TABLE IF EXISTS `t-authinfo`;
CREATE TABLE `t-authinfo`
(
    `id`                 int                                     NOT NULL AUTO_INCREMENT,
    `username`           varchar(16) COLLATE utf8mb4_general_ci  NOT NULL COMMENT '登录名',
    `encrypted_password` varchar(256) COLLATE utf8mb4_general_ci NOT NULL COMMENT '加密密码',
    `dynamic_token`      varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '动态密钥',
    `email`              varchar(64) COLLATE utf8mb4_general_ci  NOT NULL COMMENT '电子邮箱',
    `is_active`          tinyint(1)                              NOT NULL COMMENT '是否激活',
    `created_at`         datetime                                DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`         datetime                                DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `encrypted_password` (`encrypted_password`),
    UNIQUE KEY `email` (`email`),
    KEY        `ix_t-authinfo_id` (`id`),
    CONSTRAINT `t-authinfo_chk_1` CHECK ((`is_active` in (0, 1)))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of t-authinfo
-- ----------------------------
BEGIN;

INSERT INTO `t-authinfo`
    (`id`, `username`, `encrypted_password`, `dynamic_token`, `email`, `is_active`, `created_at`, `updated_at`)
VALUES
    (1, 'admin', 'a73bc5f930ae2b53ca9fe6f3df6a054b78acd8a43f188e905666568a33a3dbd67ac61e02d4d98fd8ac9bf6669995bf35',
        NULL, 'xiaoming@gmail.com', 1, '2022-11-18 11:12:10', '2022-11-18 11:12:10');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
