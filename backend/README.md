 # 安全综合日志审计分析平台 - 后端部署指南

## 环境要求

- Python 3.9+
- MySQL 8.0+ （推荐）或使用Docker
- pip 包管理器

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动MySQL数据库

#### 方式一：使用Docker（推荐）

```bash
# 启动MySQL容器
docker-compose up -d mysql

# 查看容器状态
docker-compose ps
```

#### 方式二：使用本地MySQL

1. 安装并启动MySQL服务
2. 创建数据库：
```sql
CREATE DATABASE logsystem CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置数据库连接

默认配置（与Docker Compose一致）：
- 主机：localhost
- 端口：3306
- 用户名：root
- 密码：123456
- 数据库：logsystem

如需修改，可设置环境变量：
```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
export MYSQL_DATABASE=logsystem
```

### 4. 启动后端服务

```bash
# 开发模式启动
python main.py

# 或使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 验证部署

访问以下地址验证服务：
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health
- 获取资产列表：http://localhost:8000/api/assets

## 功能特性

### 数据库自动切换
- 优先使用MySQL数据库
- MySQL连接失败时自动回退到SQLite
- 自动创建数据表和初始化预设数据

### 预设数据
系统启动时会自动创建：
- 6个网络设备（防火墙、交换机、AP等）
- 2个告警规则（网络设备离线、K8S集群无响应）

### 演示功能
- 全局故障触发：`POST /api/simulation/trigger-fault`
- 全局故障修复：`POST /api/simulation/fix-fault`

## API端点

| 模块 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 资产管理 | GET | `/api/assets` | 获取资产列表 |
| 资产管理 | POST | `/api/assets` | 添加新资产 |
| 告警管理 | GET | `/api/alerts` | 获取告警记录 |
| 告警管理 | GET | `/api/alerts/stats` | 获取告警统计 |
| 仿真控制 | POST | `/api/simulation/trigger-fault` | 触发故障 |
| 仿真控制 | POST | `/api/simulation/fix-fault` | 修复故障 |

## 故障排除

### MySQL连接问题
1. 确认MySQL服务已启动
2. 检查端口3306是否开放
3. 验证用户名密码是否正确
4. 如果使用Docker，确认容器状态：`docker-compose logs mysql`

### 依赖安装问题
```bash
# 升级pip
pip install --upgrade pip

# 如果cryptography安装失败（Windows）
pip install --upgrade setuptools
```

### 端口占用
如果8000端口被占用，可修改启动命令：
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 生产部署建议

1. 使用专用的MySQL服务器
2. 配置SSL连接
3. 使用Gunicorn等WSGI服务器
4. 配置反向代理（Nginx）
5. 设置系统服务自启动