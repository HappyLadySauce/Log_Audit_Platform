#!/usr/bin/env python3
"""
简单的数据库迁移脚本
"""
import sqlite3
import os

def migrate_database():
    # 数据库文件路径
    db_path = "./data/logsystem.db"
    
    # 确保数据目录存在
    os.makedirs("./data", exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assets'")
        if not cursor.fetchone():
            print("Assets表不存在，需要先创建基础表")
            return False
        
        # 检查现有字段
        cursor.execute("PRAGMA table_info(assets)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"现有字段: {columns}")
        
        # 需要添加的新字段
        new_fields = [
            ("manufacturer", "VARCHAR(100)"),
            ("model", "VARCHAR(100)"),
            ("purchase_date", "VARCHAR(20)"),
            ("warranty_period", "VARCHAR(50)"),
            ("admin_contact", "VARCHAR(200)"),
            ("security_policies", "TEXT"),
            ("backup_frequency", "VARCHAR(50)"),
            ("last_security_scan", "VARCHAR(20)"),
            ("compliance_status", "VARCHAR(50)")
        ]
        
        # 添加新字段
        for field_name, field_type in new_fields:
            if field_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE assets ADD COLUMN {field_name} {field_type}")
                    print(f"添加字段: {field_name}")
                except sqlite3.OperationalError as e:
                    print(f"添加字段 {field_name} 失败: {e}")
            else:
                print(f"字段 {field_name} 已存在")
        
        conn.commit()
        print("数据库迁移完成")
        return True
        
    except Exception as e:
        print(f"迁移失败: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database() 