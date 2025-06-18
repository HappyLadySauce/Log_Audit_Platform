from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import assets, alerts, logs, simulation
from app.database import engine, Base
from app.init_data import init_database
import uvicorn

# 初始化数据库和预设数据
init_database()

app = FastAPI(
    title="安全日志审计平台 API",
    description="LogSystem Backend API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(assets.router, prefix="/api", tags=["assets"])
app.include_router(alerts.router, prefix="/api", tags=["alerts"])
app.include_router(logs.router, prefix="/api", tags=["logs"])
app.include_router(simulation.router, prefix="/api", tags=["simulation"])

@app.get("/")
async def root():
    return {"message": "安全日志审计平台 API 服务已启动"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 