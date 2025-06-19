/*
 Navicat Premium Dump SQL

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 90300 (9.3.0)
 Source Host           : 127.0.0.1:3306
 Source Schema         : logsystem

 Target Server Type    : MySQL
 Target Server Version : 90300 (9.3.0)
 File Encoding         : 65001

 Date: 18/06/2025 22:05:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alert_rules
-- ----------------------------
DROP TABLE IF EXISTS `alert_rules`;
CREATE TABLE `alert_rules`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `target_asset_id` int NULL DEFAULT NULL,
  `trigger_condition` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `alert_level` enum('LOW','MEDIUM','HIGH','CRITICAL') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_active` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `target_asset_id`(`target_asset_id` ASC) USING BTREE,
  INDEX `ix_alert_rules_id`(`id` ASC) USING BTREE,
  CONSTRAINT `alert_rules_ibfk_1` FOREIGN KEY (`target_asset_id`) REFERENCES `assets` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alert_rules
-- ----------------------------
INSERT INTO `alert_rules` VALUES (1, '核心网络设备离线告警', 2, '连续5分钟未收到心跳', 'CRITICAL', 'active', '2025-06-18 04:35:54');
INSERT INTO `alert_rules` VALUES (2, 'K8S集群API Server无响应', 2, 'Kube-apiserver 连接超时', 'CRITICAL', 'active', '2025-06-18 04:35:54');

-- ----------------------------
-- Table structure for alerts
-- ----------------------------
DROP TABLE IF EXISTS `alerts`;
CREATE TABLE `alerts`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `rule_id` int NULL DEFAULT NULL,
  `asset_id` int NULL DEFAULT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `alert_level` enum('LOW','MEDIUM','HIGH','CRITICAL') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('PENDING','PROCESSING','RESOLVED','ARCHIVED') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `triggered_at` datetime NULL DEFAULT NULL,
  `processed_at` datetime NULL DEFAULT NULL,
  `resolved_at` datetime NULL DEFAULT NULL,
  `processor` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `root_cause` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `solution` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `remaining_issues` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `rule_id`(`rule_id` ASC) USING BTREE,
  INDEX `asset_id`(`asset_id` ASC) USING BTREE,
  INDEX `ix_alerts_id`(`id` ASC) USING BTREE,
  CONSTRAINT `alerts_ibfk_1` FOREIGN KEY (`rule_id`) REFERENCES `alert_rules` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `alerts_ibfk_2` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alerts
-- ----------------------------
INSERT INTO `alerts` VALUES (1, 1, NULL, '核心网络设备离线告警', '设备 分部集群接入交换机 (192.168.10.1) 连续5分钟未收到心跳信号，设备可能已离线。', 'CRITICAL', 'RESOLVED', '2025-06-18 06:33:51', '2025-06-18 13:01:51', '2025-06-18 13:02:02', '当前用户', NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (2, 2, NULL, 'K8S集群API Server无响应', 'K8S集群 分部K8S集群 的API Server无法连接，集群服务可能中断。', 'CRITICAL', 'RESOLVED', '2025-06-18 06:33:51', '2025-06-18 13:01:50', '2025-06-18 13:02:02', '当前用户', NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (3, 1, NULL, '核心网络设备离线告警', '设备 分部集群接入交换机 (192.168.10.1) 连续5分钟未收到心跳信号，设备可能已离线。', 'CRITICAL', 'RESOLVED', '2025-06-18 12:26:37', '2025-06-18 13:01:49', '2025-06-18 13:02:02', '当前用户', NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (4, 2, NULL, 'K8S集群API Server无响应', 'K8S集群 分部K8S集群 的API Server无法连接，集群服务可能中断。', 'CRITICAL', 'RESOLVED', '2025-06-18 12:26:37', '2025-06-18 13:01:49', '2025-06-18 13:02:02', '当前用户', NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (5, 1, 14, '核心网络设备离线告警', '设备 分部集群接入交换机 (192.168.10.1) 连续5分钟未收到心跳信号，设备可能已离线。', 'CRITICAL', 'RESOLVED', '2025-06-18 13:02:03', '2025-06-18 13:10:26', '2025-06-18 13:30:41', '当前用户', NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (6, 2, 15, 'K8S集群API Server无响应', 'K8S集群 分部K8S集群 的API Server无法连接，集群服务可能中断。', 'CRITICAL', 'RESOLVED', '2025-06-18 13:02:03', '2025-06-18 13:10:26', '2025-06-18 13:30:41', '当前用户', NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (7, 1, 14, '核心网络设备离线告警', '设备 分部集群接入交换机 (192.168.10.1) 连续5分钟未收到心跳信号，设备可能已离线。', 'CRITICAL', 'PENDING', '2025-06-18 13:41:12', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `alerts` VALUES (8, 2, 15, 'K8S集群API Server无响应', 'K8S集群 分部K8S集群 的API Server无法连接，集群服务可能中断。', 'CRITICAL', 'PENDING', '2025-06-18 13:41:12', NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for assets
-- ----------------------------
DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `asset_type` enum('NETWORK_DEVICE','LINUX_SERVER','WINDOWS_SERVER','K8S_CLUSTER') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ip_address` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `security_level` enum('LEVEL_ONE','LEVEL_TWO','LEVEL_THREE') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('NORMAL','WARNING','ERROR') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `admin_contact` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '管理员联系方式',
  `asset_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '资产描述',
  `last_security_scan` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最后安全扫描时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_assets_name`(`name` ASC) USING BTREE,
  INDEX `ix_assets_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of assets
-- ----------------------------
INSERT INTO `assets` VALUES (1, '分部防火墙', 'NETWORK_DEVICE', '10.10.20.1', '分部机房B-01', 'LEVEL_THREE', 'NORMAL', '2025-06-18 04:35:54', '2025-06-18 04:35:54', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (2, '分部集群接入交换机', 'NETWORK_DEVICE', '10.10.10.150', '分部机房B-02', 'LEVEL_THREE', 'NORMAL', '2025-06-18 04:35:54', '2025-06-18 04:35:54', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (3, '分部彩光交换机', 'NETWORK_DEVICE', '192.168.100.1', '分部机房B-03', 'LEVEL_TWO', 'NORMAL', '2025-06-18 04:35:54', '2025-06-18 04:35:54', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (4, '分部无线控制器', 'NETWORK_DEVICE', '192.168.100.2', '分部机房B-04', 'LEVEL_TWO', 'NORMAL', '2025-06-18 04:35:54', '2025-06-18 04:35:54', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (5, '分部用户接入交换机', 'NETWORK_DEVICE', '192.168.100.3', '分部机房B-05', 'LEVEL_TWO', 'NORMAL', '2025-06-18 04:35:54', '2025-06-18 04:35:54', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (6, '分部AP', 'NETWORK_DEVICE', '192.168.30.2', '分部办公区域', 'LEVEL_ONE', 'NORMAL', '2025-06-18 04:35:54', '2025-06-18 04:35:54', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (14, '分部集群接入交换机', 'NETWORK_DEVICE', '192.168.10.1', '分部机房', 'LEVEL_TWO', 'ERROR', '2025-06-18 13:02:03', '2025-06-18 13:41:12', NULL, NULL, NULL);
INSERT INTO `assets` VALUES (15, '分部K8S集群', 'K8S_CLUSTER', '192.168.20.100', '数据中心B栋', 'LEVEL_THREE', 'ERROR', '2025-06-18 13:02:03', '2025-06-18 13:41:12', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `asset_id` int NULL DEFAULT NULL,
  `log_type` enum('SECURITY_AUDIT','SYSTEM_OPERATION','APPLICATION_ERROR','NETWORK_TRAFFIC','K8S_EVENT') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `timestamp` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `asset_id`(`asset_id` ASC) USING BTREE,
  INDEX `ix_logs_id`(`id` ASC) USING BTREE,
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of logs
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
