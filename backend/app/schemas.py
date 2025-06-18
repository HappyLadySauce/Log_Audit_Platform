from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .models import AssetType, AssetStatus, SecurityLevel, AlertStatus, AlertLevel, LogType

# 基础模式
class AssetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="资产名称")
    asset_type: AssetType = Field(..., description="资产类型")
    ip_address: str = Field(..., pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", description="IP地址")
    location: str = Field(..., min_length=1, max_length=200, description="位置")
    security_level: SecurityLevel = Field(..., description="安全防护等级")
    # 扩展信息字段
    admin_contact: Optional[str] = Field(None, max_length=200, description="管理员联系方式")
    asset_description: Optional[str] = Field(None, description="资产描述")
    last_security_scan: Optional[str] = Field(None, max_length=20, description="最后安全扫描时间")

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[AssetType] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    security_level: Optional[SecurityLevel] = None
    status: Optional[AssetStatus] = None
    # 扩展信息字段
    admin_contact: Optional[str] = None
    asset_description: Optional[str] = None
    last_security_scan: Optional[str] = None

class Asset(AssetBase):
    id: int
    status: AssetStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 告警规则相关
class AlertRuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="规则名称")
    target_asset_id: int = Field(..., description="目标资产ID")
    trigger_condition: str = Field(..., min_length=1, description="触发条件")
    alert_level: AlertLevel = Field(..., description="告警级别")

class AlertRuleCreate(AlertRuleBase):
    is_active: str = Field(default="active", description="规则状态")

class AlertRule(AlertRuleBase):
    id: int
    is_active: str
    created_at: datetime

    class Config:
        from_attributes = True

# 告警记录相关
class AlertBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="告警标题")
    description: Optional[str] = Field(None, description="告警描述")
    alert_level: AlertLevel = Field(..., description="告警级别")

class AlertCreate(AlertBase):
    rule_id: int
    asset_id: int

class AlertProcess(BaseModel):
    processor: str = Field(..., min_length=1, max_length=100, description="处理人")

class AlertArchive(BaseModel):
    processor: str = Field(..., min_length=2, max_length=100, description="处理人")
    root_cause: str = Field(..., min_length=10, max_length=1000, description="根本原因分析")
    solution: str = Field(..., min_length=10, max_length=1000, description="解决方案")
    remaining_issues: Optional[str] = Field(None, max_length=1000, description="遗留问题")

class Alert(AlertBase):
    id: int
    rule_id: Optional[int] = None
    asset_id: Optional[int] = None
    status: AlertStatus
    triggered_at: datetime
    processed_at: Optional[datetime]
    resolved_at: Optional[datetime]
    processor: Optional[str]
    root_cause: Optional[str]
    solution: Optional[str]
    remaining_issues: Optional[str]
    
    # 关联数据
    asset: Optional[Asset] = None
    rule: Optional[AlertRule] = None

    class Config:
        from_attributes = True

# 告警统计
class AlertStats(BaseModel):
    pending: int = 0
    resolved: int = 0
    archived: int = 0

# 日志相关
class LogBase(BaseModel):
    log_type: LogType = Field(..., description="日志类型")
    title: str = Field(..., min_length=1, max_length=200, description="日志标题")
    content: str = Field(..., min_length=1, description="日志内容")
    level: str = Field(default="INFO", description="日志级别")

class LogCreate(LogBase):
    asset_id: int

class Log(LogBase):
    id: int
    asset_id: int
    timestamp: datetime
    asset: Optional[Asset] = None

    class Config:
        from_attributes = True

# 响应模式
class ResponseModel(BaseModel):
    success: bool = True
    message: str = "操作成功"
    data: Optional[dict] = None

# 分页响应
class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int = 1
    size: int = 20
    pages: int 