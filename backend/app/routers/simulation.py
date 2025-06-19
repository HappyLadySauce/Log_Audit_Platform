from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Asset as AssetModel, AlertRule as AlertRuleModel, Alert as AlertModel, AssetStatus, AlertStatus, AlertLevel
from ..schemas import ResponseModel

router = APIRouter()

@router.post("/simulation/trigger-fault", response_model=ResponseModel, summary="触发模拟故障")
async def trigger_fault(db: Session = Depends(get_db)):
    """
    触发模拟故障，用于演示：
    1. 将指定资产状态设为异常
    2. 生成对应的告警记录
    """
    try:
        # 查找目标资产：分部集群接入交换机 和 分部K8S集群
        switch_asset = db.query(AssetModel).filter(AssetModel.name == "分部集群接入交换机").first()
        k8s_asset = db.query(AssetModel).filter(AssetModel.name.like("%K8S%")).first()
        
        # 如果找不到预设资产，创建它们
        if not switch_asset:
            switch_asset = AssetModel(
                name="分部集群接入交换机",
                asset_type="network_device",
                ip_address="192.168.10.1",
                location="分部机房",
                security_level="等级二",
                status=AssetStatus.ERROR
            )
            db.add(switch_asset)
            db.commit()
            db.refresh(switch_asset)
        else:
            switch_asset.status = AssetStatus.ERROR
        
        if not k8s_asset:
            k8s_asset = AssetModel(
                name="分部K8S集群",
                asset_type="k8s_cluster",
                ip_address="192.168.20.100",
                location="数据中心B栋",
                security_level="等级三",
                status=AssetStatus.ERROR
            )
            db.add(k8s_asset)
            db.commit()
            db.refresh(k8s_asset)
        else:
            k8s_asset.status = AssetStatus.ERROR
        
        # 查找对应的告警规则，如果不存在则创建
        switch_rule = db.query(AlertRuleModel).filter(
            AlertRuleModel.name == "核心网络设备离线告警"
        ).first()
        
        if not switch_rule:
            switch_rule = AlertRuleModel(
                name="核心网络设备离线告警",
                target_asset_id=switch_asset.id,
                trigger_condition="连续5分钟未收到心跳",
                alert_level=AlertLevel.CRITICAL
            )
            db.add(switch_rule)
        
        k8s_rule = db.query(AlertRuleModel).filter(
            AlertRuleModel.name == "K8S集群API Server无响应"
        ).first()
        
        if not k8s_rule:
            k8s_rule = AlertRuleModel(
                name="K8S集群API Server无响应",
                target_asset_id=k8s_asset.id,
                trigger_condition="Kube-apiserver 连接超时",
                alert_level=AlertLevel.CRITICAL
            )
            db.add(k8s_rule)
        
        db.commit()
        
        # 生成告警记录
        switch_alert = AlertModel(
            rule_id=switch_rule.id,
            asset_id=switch_asset.id,
            title="核心网络设备离线告警",
            description=f"设备 {switch_asset.name} ({switch_asset.ip_address}) 连续5分钟未收到心跳信号，设备可能已离线。",
            alert_level=AlertLevel.CRITICAL,
            status=AlertStatus.PENDING
        )
        
        k8s_alert = AlertModel(
            rule_id=k8s_rule.id,
            asset_id=k8s_asset.id,
            title="K8S集群API Server无响应",
            description=f"K8S集群 {k8s_asset.name} 的API Server无法连接，集群服务可能中断。",
            alert_level=AlertLevel.CRITICAL,
            status=AlertStatus.PENDING
        )
        
        db.add(switch_alert)
        db.add(k8s_alert)
        db.commit()
        
        return ResponseModel(
            message="模拟故障已触发，生成了2条严重告警，相关资产状态已更新为异常"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"故障触发失败: {str(e)}")

@router.post("/simulation/fix-fault", response_model=ResponseModel, summary="修复模拟故障")
async def fix_fault(db: Session = Depends(get_db)):
    """
    修复模拟故障，用于演示：
    1. 将异常资产状态恢复为正常
    2. 将对应的告警状态更新为已解决
    """
    try:
        # 恢复资产状态
        affected_assets = db.query(AssetModel).filter(
            AssetModel.status == AssetStatus.ERROR
        ).all()
        
        for asset in affected_assets:
            asset.status = AssetStatus.NORMAL
        
        # 解决相关告警
        pending_alerts = db.query(AlertModel).filter(
            AlertModel.status.in_([AlertStatus.PENDING, AlertStatus.PROCESSING])
        ).all()
        
        for alert in pending_alerts:
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.utcnow()
        
        db.commit()
        
        return ResponseModel(
            message=f"模拟故障已修复，{len(affected_assets)}个资产状态已恢复，{len(pending_alerts)}条告警已自动解决"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"故障修复失败: {str(e)}")

@router.post("/simulation/init-data", response_model=ResponseModel, summary="初始化演示数据")
async def init_demo_data(db: Session = Depends(get_db)):
    """初始化演示所需的基础数据"""
    try:
        # 检查是否已有数据
        existing_assets = db.query(AssetModel).count()
        if existing_assets > 0:
            return ResponseModel(message="演示数据已存在，无需重复初始化")
        
        # 创建预设网络设备
        demo_assets = [
            AssetModel(
                name="Core-Switch-01",
                asset_type="network_device",
                ip_address="192.168.1.1",
                location="数据中心A栋",
                security_level="等级三",
                status=AssetStatus.NORMAL
            ),
            AssetModel(
                name="Firewall-Main",
                asset_type="network_device",
                ip_address="10.0.0.1",
                location="互联网入口",
                security_level="等级三",
                status=AssetStatus.NORMAL
            ),
            AssetModel(
                name="分部集群接入交换机",
                asset_type="network_device",
                ip_address="192.168.10.1",
                location="分部机房",
                security_level="等级二",
                status=AssetStatus.NORMAL
            )
        ]
        
        for asset in demo_assets:
            db.add(asset)
        
        db.commit()
        
        return ResponseModel(message="演示数据初始化成功，已创建3个预设网络设备")
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"数据初始化失败: {str(e)}") 