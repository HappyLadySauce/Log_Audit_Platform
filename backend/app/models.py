from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class AssetType(str, enum.Enum):
    NETWORK_DEVICE = "network_device"
    LINUX_SERVER = "linux_server"
    WINDOWS_SERVER = "windows_server"
    K8S_CLUSTER = "k8s_cluster"

class AssetStatus(str, enum.Enum):
    NORMAL = "normal"
    WARNING = "warning"
    ERROR = "error"

class SecurityLevel(str, enum.Enum):
    LEVEL_ONE = "等级一"
    LEVEL_TWO = "等级二"
    LEVEL_THREE = "等级三"

class AlertStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    RESOLVED = "RESOLVED"
    ARCHIVED = "ARCHIVED"
    IGNORED = "IGNORED"

class AlertLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class LogType(str, enum.Enum):
    SECURITY_AUDIT = "安全审计"
    SYSTEM_OPERATION = "系统操作"
    APPLICATION_ERROR = "应用异常"
    NETWORK_TRAFFIC = "网络流量"
    K8S_EVENT = "K8S事件"

# 资产模型
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    ip_address = Column(String(15), nullable=False)
    location = Column(String(200), nullable=False)
    security_level = Column(Enum(SecurityLevel), nullable=False)
    status = Column(Enum(AssetStatus), default=AssetStatus.NORMAL)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 扩展信息字段
    admin_contact = Column(String(200))  # 管理员联系方式
    asset_description = Column(Text)  # 资产描述
    last_security_scan = Column(String(20))  # 最后安全扫描时间

    # 关联关系
    alerts = relationship("Alert", back_populates="asset")

# 告警规则模型
class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    target_asset_id = Column(Integer, ForeignKey("assets.id"))
    trigger_condition = Column(Text, nullable=False)
    alert_level = Column(Enum(AlertLevel), nullable=False)
    is_active = Column(String(10), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联关系
    target_asset = relationship("Asset")
    alerts = relationship("Alert", back_populates="rule")

# 告警记录模型
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    alert_level = Column(Enum(AlertLevel), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.PENDING)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    resolved_at = Column(DateTime)
    
    # 处理信息
    processor = Column(String(100))
    root_cause = Column(Text)
    solution = Column(Text)
    remaining_issues = Column(Text)

    # 关联关系
    rule = relationship("AlertRule", back_populates="alerts")
    asset = relationship("Asset", back_populates="alerts")

# 日志记录模型
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    log_type = Column(Enum(LogType), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    level = Column(String(20), default="INFO")
    timestamp = Column(DateTime, default=datetime.utcnow)

    # 关联关系
    asset = relationship("Asset") 