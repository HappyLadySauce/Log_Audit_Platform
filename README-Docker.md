# LogSystem Docker 部署指南

## 🏗️ 构建方式

本项目采用 **本地构建 + Docker 打包** 的方式：
1. 首先在本地环境构建 Vue 项目
2. 然后将构建产物拷贝到 Docker 镜像中
3. 使用 Nginx 提供静态文件服务

这种方式的优势：
- 镜像更小（只包含 Nginx + 静态文件）
- 构建更快（避免在容器内安装 Node.js 依赖）
- 更灵活（可以在不同环境构建）

## 📁 文件结构

```
├── Dockerfile              # 简化的 Dockerfile
├── docker-compose.yml      # Docker Compose 配置
├── .dockerignore           # Docker 忽略文件
├── docker/
│   └── nginx.conf          # Nginx 配置文件
└── scripts/
    ├── build-and-docker.ps1  # PowerShell 构建脚本
    └── build-and-docker.bat  # 批处理构建脚本
```

## 🚀 快速开始

### 方法一：使用构建脚本（推荐）

#### PowerShell 脚本
```powershell
# 完整构建流程（本地构建 + Docker 打包）
.\scripts\build-and-docker.ps1

# 指定版本
.\scripts\build-and-docker.ps1 -Version "v1.0.0"

# 跳过本地构建（如果已经构建过）
.\scripts\build-and-docker.ps1 -SkipBuild

# 构建并推送到镜像仓库
.\scripts\build-and-docker.ps1 -Version "v1.0.0" -Registry "your-registry.com" -Push
```

#### 批处理脚本
```cmd
REM 完整构建流程
scripts\build-and-docker.bat

REM 指定版本
scripts\build-and-docker.bat v1.0.0

REM 跳过本地构建
scripts\build-and-docker.bat latest "" skip

REM 构建并推送到镜像仓库
scripts\build-and-docker.bat v1.0.0 your-registry.com
```

### 方法二：手动步骤

#### 1. 本地构建项目
```bash
# 安装依赖（如果尚未安装）
pnpm install

# 构建项目
pnpm build
```

#### 2. 构建 Docker 镜像
```bash
# 构建镜像
docker build -t logsystem:latest .

# 或者使用 docker-compose
docker-compose build
```

#### 3. 运行容器
```bash
# 直接运行
docker run -d -p 8080:80 logsystem:latest

# 或者使用 docker-compose
docker-compose up -d
```

## 🔧 配置说明

### Dockerfile
```dockerfile
FROM nginx:alpine
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY dist/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx 特性
- **SPA 路由支持**：支持 Vue Router 的 history 模式
- **静态资源缓存**：自动缓存 JS/CSS/图片等静态文件
- **Gzip 压缩**：启用 Gzip 压缩提高传输效率
- **安全头部**：添加安全相关的 HTTP 头部
- **健康检查**：提供 `/health` 端点

### 端口映射
- 容器端口：80
- 主机端口：8080
- 访问地址：http://localhost:8080

## 📊 构建脚本参数

### PowerShell 脚本参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-Version` | String | "latest" | Docker 镜像版本标签 |
| `-Registry` | String | "" | 镜像仓库地址 |
| `-SkipBuild` | Switch | False | 跳过本地构建步骤 |
| `-Push` | Switch | False | 推送镜像到仓库 |

### 批处理脚本参数
| 位置 | 参数 | 默认值 | 说明 |
|------|------|--------|------|
| 1 | VERSION | "latest" | Docker 镜像版本标签 |
| 2 | REGISTRY | "" | 镜像仓库地址 |
| 3 | SKIP_BUILD | "" | 填写 "skip" 跳过本地构建 |

## 🛠️ 开发工作流

### 标准开发流程
```bash
# 1. 修改代码
# 2. 本地测试
pnpm dev

# 3. 构建和 Docker 打包
.\scripts\build-and-docker.ps1

# 4. 测试 Docker 容器
docker-compose up -d

# 5. 访问 http://localhost:8080 测试
```

### 快速重新构建
```bash
# 如果只修改了代码，可以先本地构建再 Docker 打包
pnpm build
.\scripts\build-and-docker.ps1 -SkipBuild
```

## 🔍 健康检查

```bash
# 检查容器状态
docker-compose ps

# 查看容器日志
docker-compose logs

# 健康检查端点
curl http://localhost:8080/health
```

## 🐳 Docker Compose 命令

```bash
# 构建并启动
docker-compose up -d --build

# 仅启动（使用现有镜像）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止并移除容器
docker-compose down

# 重启服务
docker-compose restart
```

## 📈 性能优化

### 镜像大小优化
- 使用 Alpine 基础镜像（~5MB）
- 仅复制构建产物，不包含源代码
- 启用 Nginx Gzip 压缩

### 构建优化
- 本地构建避免重复下载依赖
- 可以并行进行多个版本构建
- 支持增量构建（跳过构建步骤）

## 🔧 故障排除

### 常见问题

1. **构建产物不存在**
   ```bash
   # 确保先执行本地构建
   pnpm build
   
   # 检查 dist 目录是否存在
   ls dist/
   ```

2. **Docker 构建失败**
   ```bash
   # 检查 Dockerfile 和构建产物
   docker build --no-cache -t logsystem:latest .
   ```

3. **容器无法访问**
   ```bash
   # 检查端口映射
   docker ps
   
   # 检查容器日志
   docker logs <container_id>
   ```

4. **Nginx 配置问题**
   ```bash
   # 进入容器检查配置
   docker exec -it <container_id> sh
   nginx -t
   ```

## 📝 维护建议

### 定期清理
```bash
# 清理未使用的镜像
docker image prune -f

# 清理构建缓存
docker builder prune -f
```

### 版本管理
```bash
# 为发布版本打标签
.\scripts\build-and-docker.ps1 -Version "v1.0.0"

# 保留多个版本
docker images | grep logsystem
```

---

**快速构建，轻松部署！🚀** 