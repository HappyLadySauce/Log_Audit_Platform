from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models import AlertRule as AlertRuleModel, Alert as AlertModel, AlertStatus, AlertLevel
from ..schemas import AlertRule, AlertRuleCreate, Alert, AlertCreate, AlertProcess, AlertArchive, AlertStats, ResponseModel

router = APIRouter()

# 告警规则相关
@router.get("/alert-rules", response_model=List[AlertRule], summary="获取告警规则列表")
async def get_alert_rules(
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """获取告警规则列表"""
    rules = db.query(AlertRuleModel).offset(skip).limit(limit).all()
    return rules

@router.post("/alert-rules", response_model=AlertRule, summary="创建告警规则")
async def create_alert_rule(rule: AlertRuleCreate, db: Session = Depends(get_db)):
    """创建新的告警规则"""
    db_rule = AlertRuleModel(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.put("/alert-rules/{rule_id}", response_model=AlertRule, summary="更新告警规则")
async def update_alert_rule(rule_id: int, rule: AlertRuleCreate, db: Session = Depends(get_db)):
    """更新指定ID的告警规则"""
    db_rule = db.query(AlertRuleModel).filter(AlertRuleModel.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="告警规则不存在")
    
    # 更新字段
    for field, value in rule.dict(exclude_unset=True).items():
        setattr(db_rule, field, value)
    
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.delete("/alert-rules/{rule_id}", summary="删除告警规则")
async def delete_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    """删除指定ID的告警规则"""
    db_rule = db.query(AlertRuleModel).filter(AlertRuleModel.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="告警规则不存在")
    
    # 检查是否有关联的告警记录
    alert_count = db.query(AlertModel).filter(AlertModel.rule_id == rule_id).count()
    if alert_count > 0:
        raise HTTPException(status_code=400, detail=f"无法删除规则，存在 {alert_count} 条关联的告警记录")
    
    db.delete(db_rule)
    db.commit()
    return {"success": True, "message": "告警规则删除成功"}

# 告警记录相关
@router.get("/alerts", response_model=List[Alert], summary="获取告警记录列表")
async def get_alerts(
    status: Optional[AlertStatus] = Query(None, description="按状态筛选"),
    alert_level: Optional[AlertLevel] = Query(None, description="按告警级别筛选"),
    skip: int = Query(0, description="跳过的记录数"),
    limit: int = Query(100, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """获取告警记录列表，支持按状态和级别筛选"""
    query = db.query(AlertModel).options(
        joinedload(AlertModel.asset),
        joinedload(AlertModel.rule)
    )
    
    if status:
        query = query.filter(AlertModel.status == status)
    if alert_level:
        query = query.filter(AlertModel.alert_level == alert_level)
    
    alerts = query.order_by(AlertModel.triggered_at.desc()).offset(skip).limit(limit).all()
    return alerts

@router.get("/alerts/stats", response_model=AlertStats, summary="获取告警统计信息")
async def get_alert_stats(db: Session = Depends(get_db)):
    """获取各状态告警的统计数据"""
    stats = AlertStats()
    
    # 统计各状态的告警数量
    stats.pending = db.query(AlertModel).filter(AlertModel.status == AlertStatus.PENDING).count()
    stats.resolved = db.query(AlertModel).filter(AlertModel.status == AlertStatus.RESOLVED).count()
    stats.archived = db.query(AlertModel).filter(AlertModel.status == AlertStatus.ARCHIVED).count()
    # Note: ignored status is currently handled separately in frontend
    
    return stats

@router.get("/alerts/{alert_id}", response_model=Alert, summary="获取单个告警详情")
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """获取指定ID的告警详情"""
    alert = db.query(AlertModel).options(
        joinedload(AlertModel.asset),
        joinedload(AlertModel.rule)
    ).filter(AlertModel.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    return alert

@router.post("/alerts", response_model=Alert, summary="创建告警记录")
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """创建新的告警记录"""
    db_alert = AlertModel(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.post("/alerts/{alert_id}/process", response_model=Alert, summary="处理告警")
async def process_alert(alert_id: int, process_data: AlertProcess, db: Session = Depends(get_db)):
    """将告警状态更新为已处理"""
    db_alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    
    if db_alert.status != AlertStatus.PENDING:
        raise HTTPException(status_code=400, detail="只能处理待处理状态的告警")
    
    db_alert.status = AlertStatus.RESOLVED
    db_alert.processed_at = datetime.utcnow()
    db_alert.resolved_at = datetime.utcnow()
    db_alert.processor = process_data.processor
    
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.post("/alerts/{alert_id}/resolve", response_model=Alert, summary="解决告警")
async def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """将告警状态更新为已解决"""
    db_alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    
    db_alert.status = AlertStatus.RESOLVED
    db_alert.resolved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.post("/alerts/{alert_id}/archive", response_model=Alert, summary="归档告警")
async def archive_alert(alert_id: int, archive_data: AlertArchive, db: Session = Depends(get_db)):
    """归档已解决的告警"""
    db_alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    
    if db_alert.status != AlertStatus.RESOLVED:
        raise HTTPException(status_code=400, detail="只能归档已解决的告警")
    
    # 更新告警信息
    db_alert.status = AlertStatus.ARCHIVED
    db_alert.processor = archive_data.processor
    db_alert.root_cause = archive_data.root_cause
    db_alert.solution = archive_data.solution
    db_alert.remaining_issues = archive_data.remaining_issues
    
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.post("/alerts/{alert_id}/ignore", response_model=Alert, summary="忽略告警")
async def ignore_alert(alert_id: int, db: Session = Depends(get_db)):
    """将告警状态更新为已忽略"""
    db_alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    
    db_alert.status = AlertStatus.IGNORED
    db_alert.processed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_alert)
    return db_alert