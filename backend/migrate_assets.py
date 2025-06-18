 #!/usr/bin/env python3
"""
数据库迁移脚本：为Asset表添加安全信息字段
运行此脚本以更新现有数据库结构
"""

import os
import sys
import sqlite3
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import DATABASE_URL

def migrate_assets_table():
    """为资产表添加新的安全信息字段"""
    
    # 提取SQLite数据库文件路径
    db_path = DATABASE_URL.replace("sqlite:///", "")
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查是否已经有新字段
        cursor.execute("PRAGMA table_info(assets)")
        columns = [column[1] for column in cursor.fetchall()]
        
        new_fields = [
            "manufacturer",
            "model", 
            "purchase_date",
            "warranty_period",
            "admin_contact",
            "security_policies",
            "backup_frequency",
            "last_security_scan",
            "compliance_status"
        ]
        
        migration_needed = False
        for field in new_fields:
            if field not in columns:
                migration_needed = True
                break
        
        if not migration_needed:
            print("数据库已经是最新版本，无需迁移")
            return True
        
        print("开始数据库迁移...")
        
        # 添加新字段
        alter_commands = [
            "ALTER TABLE assets ADD COLUMN manufacturer VARCHAR(100)",
            "ALTER TABLE assets ADD COLUMN model VARCHAR(100)", 
            "ALTER TABLE assets ADD COLUMN purchase_date VARCHAR(20)",
            "ALTER TABLE assets ADD COLUMN warranty_period VARCHAR(50)",
            "ALTER TABLE assets ADD COLUMN admin_contact VARCHAR(200)",
            "ALTER TABLE assets ADD COLUMN security_policies TEXT",
            "ALTER TABLE assets ADD COLUMN backup_frequency VARCHAR(50)",
            "ALTER TABLE assets ADD COLUMN last_security_scan VARCHAR(20)",
            "ALTER TABLE assets ADD COLUMN compliance_status VARCHAR(50)"
        ]
        
        for command in alter_commands:
            try:
                cursor.execute(command)
                print(f"执行: {command}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"字段已存在，跳过: {command}")
                else:
                    raise e
        
        conn.commit()
        print("数据库迁移完成！")
        
        # 验证迁移结果
        cursor.execute("PRAGMA table_info(assets)")
        updated_columns = [column[1] for column in cursor.fetchall()]
        print(f"更新后的字段列表: {updated_columns}")
        
        return True
        
    except Exception as e:
        print(f"迁移失败: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 数据库迁移工具 ===")
    print(f"目标数据库: {DATABASE_URL}")
    print(f"时间: {datetime.now()}")
    print()
    
    success = migrate_assets_table()
    
    if success:
        print("\n✅ 迁移成功完成！")
        print("现在可以重启服务器以使用新功能。")
    else:
        print("\n❌ 迁移失败！")
        print("请检查错误信息并重试。")
    
    sys.exit(0 if success else 1)