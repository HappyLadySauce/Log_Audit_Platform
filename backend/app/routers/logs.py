from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..database import get_db
from ..models import Log as LogModel, LogType
from ..schemas import Log, LogCreate

router = APIRouter()

@router.get("/logs", response_model=List[Log], summary="获取日志记录列表")
async def get_logs(
    log_type: Optional[LogType] = Query(None, description="按日志类型筛选"),
    asset_id: Optional[int] = Query(None, description="按资产ID筛选"),
    level: Optional[str] = Query(None, description="按日志级别筛选"),
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """获取日志记录列表，支持多种筛选条件"""
    query = db.query(LogModel).options(joinedload(LogModel.asset))
    
    if log_type:
        query = query.filter(LogModel.log_type == log_type)
    if asset_id:
        query = query.filter(LogModel.asset_id == asset_id)
    if level:
        query = query.filter(LogModel.level == level)
    
    logs = query.order_by(LogModel.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/logs/{log_id}", response_model=Log, summary="获取单个日志详情")
async def get_log(log_id: int, db: Session = Depends(get_db)):
    """获取指定ID的日志详情"""
    log = db.query(LogModel).options(joinedload(LogModel.asset)).filter(LogModel.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="日志记录不存在")
    return log

@router.post("/logs", response_model=Log, summary="创建日志记录")
async def create_log(log: LogCreate, db: Session = Depends(get_db)):
    """创建新的日志记录"""
    db_log = LogModel(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log 