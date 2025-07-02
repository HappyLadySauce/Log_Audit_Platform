from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 数据库配置
DATABASE_CONFIG = {
    # MySQL配置
    "MYSQL_HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "MYSQL_PORT": os.getenv("MYSQL_PORT", "3306"),
    "MYSQL_USER": os.getenv("MYSQL_USER", "logsystem"),
    "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD", "logsystem"),
    "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE", "logsystem"),
}

# MySQL数据库URL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_CONFIG['MYSQL_USER']}:{DATABASE_CONFIG['MYSQL_PASSWORD']}@"
    f"{DATABASE_CONFIG['MYSQL_HOST']}:{DATABASE_CONFIG['MYSQL_PORT']}/{DATABASE_CONFIG['MYSQL_DATABASE']}"
    f"?charset=utf8mb4"
)

# 如果在开发环境中没有MySQL，回退到SQLite
try:
    # 尝试连接MySQL
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    engine.connect()
    print("✅ 使用MySQL数据库")
except Exception as e:
    print(f"⚠️  MySQL连接失败，回退到SQLite: {e}")
    # 创建data目录如果不存在
    if not os.path.exists("data"):
        os.makedirs("data")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./data/logsystem.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    print("✅ 使用SQLite数据库")

# 创建会话本地类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 