@echo off
REM LogSystem 本地构建 + Docker 打包脚本 (Windows 批处理版本)

setlocal EnableDelayedExpansion

REM 切换到项目根目录
cd /d "%~dp0.."

REM 项目信息
set PROJECT_NAME=logsystem
if "%1"=="" (
    set VERSION=latest
) else (
    set VERSION=%1
)
set REGISTRY=%2
set SKIP_BUILD=%3

echo 🚀 LogSystem 构建和 Docker 打包流程开始...
echo 📁 工作目录: %CD%

REM 第一步：本地构建项目
if not "%SKIP_BUILD%"=="skip" (
    echo.
    echo 📦 第一步：本地构建项目...
    
    REM 检查是否存在 dist 目录并清理
    if exist "dist" (
        echo 🗑️  清理旧的构建文件...
        rmdir /s /q "dist"
    )
    
    REM 检查依赖是否已安装
    if not exist "node_modules" (
        echo 📥 安装项目依赖...
        pnpm install
        
        if errorlevel 1 (
            echo ❌ 依赖安装失败
            exit /b 1
        )
    )
    
    REM 执行构建
    echo 🔨 执行项目构建...
    pnpm build
    
    if errorlevel 1 (
        echo ❌ 项目构建失败
        exit /b 1
    )
    
    REM 检查构建产物
    if not exist "dist" (
        echo ❌ 构建产物不存在，请检查构建配置
        exit /b 1
    )
    
    echo ✅ 项目构建成功！
) else (
    echo ⏭️  跳过本地构建步骤
)

REM 第二步：检查 Docker 环境
echo.
echo 🐳 第二步：检查 Docker 环境...

docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker 未运行，请先启动 Docker Desktop
    exit /b 1
) else (
    echo ✅ Docker 环境正常
)

REM 第三步：构建 Docker 镜像
echo.
echo 🏗️  第三步：构建 Docker 镜像...

REM 检查构建产物是否存在
if not exist "dist" (
    echo ❌ dist 目录不存在，请先运行本地构建
    exit /b 1
)

REM 构建 Docker 镜像
echo 🔨 构建 Docker 镜像: %PROJECT_NAME%:%VERSION%
docker build -t %PROJECT_NAME%:%VERSION% -t %PROJECT_NAME%:latest .

if errorlevel 1 (
    echo ❌ Docker 镜像构建失败
    exit /b 1
) else (
    echo ✅ Docker 镜像构建成功！
)

REM 第四步：显示镜像信息
echo.
echo 📋 第四步：镜像信息...
docker images | findstr %PROJECT_NAME%

REM 第五步：推送镜像（可选）
if not "%REGISTRY%"=="" (
    echo.
    echo 🚀 第五步：推送镜像到仓库: %REGISTRY%
    
    REM 标记镜像
    docker tag %PROJECT_NAME%:%VERSION% %REGISTRY%/%PROJECT_NAME%:%VERSION%
    docker tag %PROJECT_NAME%:latest %REGISTRY%/%PROJECT_NAME%:latest
    
    REM 推送镜像
    docker push %REGISTRY%/%PROJECT_NAME%:%VERSION%
    docker push %REGISTRY%/%PROJECT_NAME%:latest
    
    if errorlevel 1 (
        echo ❌ 镜像推送失败
        exit /b 1
    ) else (
        echo ✅ 镜像推送完成！
    )
)

REM 完成
echo.
echo 🎉 所有操作完成！
echo 💡 使用方法：
echo   直接运行: docker run -d -p 8080:80 %PROJECT_NAME%:%VERSION%
echo   使用 compose: docker-compose up -d
echo   访问地址: http://localhost:8080
echo.
echo 📝 其他有用的命令：
echo   查看容器状态: docker ps
echo   查看容器日志: docker logs ^<container_id^>
echo   停止容器: docker-compose down

endlocal 