from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Asset, AlertRule, AssetType, AssetStatus, SecurityLevel, AlertLevel
from datetime import datetime

def init_database():
    """初始化数据库表和预设数据"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Asset).count() > 0:
            print("数据库已有数据，跳过初始化")
            return
        
        print("正在初始化数据库预设数据...")
        
        # 预设网络设备数据
        network_devices = [
            {
                "name": "分部防火墙",
                "asset_type": AssetType.NETWORK_DEVICE,
                "ip_address": "10.10.20.1",
                "location": "分部机房B-01",
                "security_level": SecurityLevel.HIGH,
                "status": AssetStatus.NORMAL
            },
            {
                "name": "分部集群接入交换机",
                "asset_type": AssetType.NETWORK_DEVICE,
                "ip_address": "10.10.10.150",
                "location": "分部机房B-02",
                "security_level": SecurityLevel.HIGH,
                "status": AssetStatus.NORMAL
            },
            {
                "name": "分部彩光交换机",
                "asset_type": AssetType.NETWORK_DEVICE,
                "ip_address": "192.168.100.1",
                "location": "分部机房B-03",
                "security_level": SecurityLevel.MEDIUM_LOW,
                "status": AssetStatus.NORMAL
            },
            {
                "name": "分部无线控制器",
                "asset_type": AssetType.NETWORK_DEVICE,
                "ip_address": "192.168.100.2",
                "location": "分部机房B-04",
                "security_level": SecurityLevel.MEDIUM_LOW,
                "status": AssetStatus.NORMAL
            },
            {
                "name": "分部用户接入交换机",
                "asset_type": AssetType.NETWORK_DEVICE,
                "ip_address": "192.168.100.3",
                "location": "分部机房B-05",
                "security_level": SecurityLevel.MEDIUM_LOW,
                "status": AssetStatus.NORMAL
            },
            {
                "name": "分部AP",
                "asset_type": AssetType.NETWORK_DEVICE,
                "ip_address": "192.168.30.2",
                "location": "分部办公区域",
                "security_level": SecurityLevel.LOW,
                "status": AssetStatus.NORMAL
            }
        ]
        
        # 添加网络设备
        for device_data in network_devices:
            device = Asset(**device_data)
            db.add(device)
        
        db.commit()
        
        # 获取创建的设备用于创建告警规则
        switch_device = db.query(Asset).filter(Asset.name == "分部集群接入交换机").first()
        
        # 预设告警规则
        alert_rules = [
            {
                "name": "核心网络设备离线告警",
                "target_asset_id": switch_device.id if switch_device else 1,
                "trigger_condition": "连续5分钟未收到心跳",
                "alert_level": AlertLevel.CRITICAL,
                "is_active": "active"
            },
            {
                "name": "K8S集群API Server无响应",
                "target_asset_id": switch_device.id if switch_device else 1,  # 暂时指向交换机，实际演示时会创建K8S集群
                "trigger_condition": "Kube-apiserver 连接超时",
                "alert_level": AlertLevel.CRITICAL,
                "is_active": "active"
            }
        ]
        
        # 添加告警规则
        for rule_data in alert_rules:
            rule = AlertRule(**rule_data)
            db.add(rule)
        
        db.commit()
        print("✅ 数据库初始化完成")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 