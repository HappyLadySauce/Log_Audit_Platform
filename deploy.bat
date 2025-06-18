@echo off
chcp 65001
echo =======================================
echo    安全日志审计平台 - 快速部署脚本
echo =======================================

echo.
echo [1/5] 检查Docker环境...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker未安装或未启动，请先安装Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker环境正常

echo.
echo [2/5] 启动MySQL数据库...
cd backend
docker-compose up -d mysql
echo ✅ MySQL数据库已启动

echo.
echo [3/5] 安装后端依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 后端依赖安装失败
    pause
    exit /b 1
)
echo ✅ 后端依赖安装完成

echo.
echo [4/5] 安装前端依赖...
cd ..\frontend
npm install
if %errorlevel% neq 0 (
    echo ⚠️  npm安装失败，尝试使用pnpm...
    pnpm install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败
        pause
        exit /b 1
    )
)
echo ✅ 前端依赖安装完成

echo.
echo [5/5] 启动服务...
echo 🚀 启动后端服务（后台运行）...
cd ..\backend
start "LogSystem Backend" cmd /c "python main.py"

echo 🚀 启动前端服务...
cd ..\frontend
start "LogSystem Frontend" cmd /c "npm run dev"

echo.
echo =======================================
echo          🎉 部署完成！
echo =======================================
echo.
echo 📝 服务地址：
echo    前端访问：http://localhost:5173
echo    后端API：http://localhost:8000
echo    API文档：http://localhost:8000/docs
echo.
echo 📋 预设账号信息：
echo    数据库：logsystem（MySQL）
echo    用户名：root
echo    密码：123456
echo.
echo 🔧 演示功能：
echo    1. 点击右上角"触发故障"按钮模拟故障
echo    2. 在资产管理中添加服务器设备
echo    3. 查看告警记录和处理流程
echo    4. 点击"修复故障"恢复正常状态
echo.
echo 按任意键退出...
pause >nul 