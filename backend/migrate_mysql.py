#!/usr/bin/env python3
"""
MySQL数据库迁移脚本：为Asset表添加安全信息字段
运行此脚本以更新现有MySQL数据库结构
"""

import os
import sys
import pymysql
from datetime import datetime

def migrate_mysql_assets_table():
    """为MySQL资产表添加新的安全信息字段"""
    
    # MySQL配置
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "ChinaSkills!"),
        "database": os.getenv("MYSQL_DATABASE", "logsystem"),
        "charset": "utf8mb4"
    }
    
    try:
        # 连接MySQL数据库
        print(f"正在连接MySQL数据库: {config['host']}:{config['port']}/{config['database']}")
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # 检查assets表是否存在
        cursor.execute("SHOW TABLES LIKE 'assets'")
        if not cursor.fetchone():
            print("❌ assets表不存在！请先运行服务器以创建基础表。")
            return False
        
        # 获取当前表结构
        cursor.execute("DESCRIBE assets")
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"当前字段: {existing_columns}")
        
        # 需要添加的新字段
        new_fields = [
            ("manufacturer", "VARCHAR(100) COMMENT '制造商'"),
            ("model", "VARCHAR(100) COMMENT '设备型号'"), 
            ("purchase_date", "VARCHAR(20) COMMENT '采购日期'"),
            ("warranty_period", "VARCHAR(50) COMMENT '保修期限'"),
            ("admin_contact", "VARCHAR(200) COMMENT '管理员联系方式'"),
            ("security_policies", "TEXT COMMENT '安全策略'"),
            ("backup_frequency", "VARCHAR(50) COMMENT '备份频率'"),
            ("last_security_scan", "VARCHAR(20) COMMENT '最后安全扫描时间'"),
            ("compliance_status", "VARCHAR(50) COMMENT '合规状态'")
        ]
        
        migration_needed = False
        fields_to_add = []
        
        for field_name, field_definition in new_fields:
            if field_name not in existing_columns:
                migration_needed = True
                fields_to_add.append((field_name, field_definition))
        
        if not migration_needed:
            print("✅ 数据库已经是最新版本，无需迁移")
            return True
        
        print("🔄 开始数据库迁移...")
        
        # 添加新字段
        for field_name, field_definition in fields_to_add:
            try:
                sql = f"ALTER TABLE assets ADD COLUMN {field_name} {field_definition}"
                cursor.execute(sql)
                print(f"✅ 添加字段: {field_name}")
            except pymysql.Error as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠️  字段已存在，跳过: {field_name}")
                else:
                    print(f"❌ 添加字段失败 {field_name}: {e}")
                    raise e
        
        conn.commit()
        print("🎉 数据库迁移完成！")
        
        # 验证迁移结果
        cursor.execute("DESCRIBE assets")
        updated_columns = [row[0] for row in cursor.fetchall()]
        print(f"更新后的字段列表: {updated_columns}")
        
        return True
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== MySQL数据库迁移工具 ===")
    print(f"时间: {datetime.now()}")
    print()
    
    success = migrate_mysql_assets_table()
    
    if success:
        print("\n✅ 迁移成功完成！")
        print("现在可以重启服务器以使用新功能。")
    else:
        print("\n❌ 迁移失败！")
        print("请检查错误信息并重试。")
    
    sys.exit(0 if success else 1) 