#!/usr/bin/env python3
"""
安全综合日志审计平台后端服务启动脚本
运行前请确保已安装所有依赖：pip install -r requirements.txt
"""

import uvicorn
from app.database import engine, Base
from app.models import Asset, AlertRule, Alert, Log
import sys
import os

def init_database():
    """初始化数据库表"""
    print("正在初始化数据库...")
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
        return True
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 启动安全综合日志审计平台后端服务")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 初始化数据库
    if not init_database():
        sys.exit(1)
    
    print("📡 启动FastAPI服务器...")
    print("🌐 API文档地址: http://localhost:8000/docs")
    print("🔧 健康检查: http://localhost:8000/health")
    print("📊 前端开发服务器: http://localhost:5173")
    print("\n按Ctrl+C停止服务\n")
    
    try:
        # 启动服务器
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

if __name__ == "__main__":
    main() 