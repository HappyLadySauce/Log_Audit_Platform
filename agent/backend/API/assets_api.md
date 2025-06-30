# 资产管理API接口文档

## 接口概述
资产管理模块提供了完整的IT资产管理功能，包括资产的增删改查操作，支持多种设备类型的管理。

## 支持的设备类型
- `linux_server` - Linux服务器
- `windows_server` - Windows服务器  
- `network_device` - 网络设备
- `other` - 其他设备

## API接口列表

### 1. 获取资产列表
**接口地址：** `GET /api/assets`

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| asset_type | string | 否 | 资产类型筛选 |
| status | string | 否 | 状态筛选(normal/warning/error) |
| skip | int | 否 | 跳过的记录数，默认0 |
| limit | int | 否 | 返回的记录数，默认100 |

**响应示例：**
```json
[
  {
    "id": 1,
    "name": "Web服务器01",
    "asset_type": "linux_server",
    "ip_address": "192.168.1.100",
    "location": "数据中心A栋",
    "security_level": "中高防护级别",
    "status": "normal",
    "created_at": "2023-12-01T10:00:00",
    "updated_at": "2023-12-01T10:00:00",
    "admin_contact": "admin@example.com"
  }
]
```

### 2. 获取单个资产详情
**接口地址：** `GET /api/assets/{id}`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 资产ID |

**响应示例：**
```json
{
  "id": 1,
  "name": "Web服务器01",
  "asset_type": "linux_server",
  "ip_address": "192.168.1.100",
  "location": "数据中心A栋",
  "security_level": "中高防护级别",
  "status": "normal",
  "created_at": "2023-12-01T10:00:00",
  "updated_at": "2023-12-01T10:00:00",
  "admin_contact": "admin@example.com",
  "asset_description": "生产环境Web服务器",
  "last_security_scan": "2023-11-30"
}
```

### 3. 创建新资产
**接口地址：** `POST /api/assets`

**请求体：**
```json
{
  "name": "新服务器01",
  "asset_type": "other",
  "ip_address": "192.168.1.200",
  "location": "数据中心B栋",
  "security_level": "中高防护级别",
  "admin_contact": "admin@example.com",
  "asset_description": "其他类型设备描述",
  "last_security_scan": "2023-12-01"
}
```

**响应示例：**
```json
{
  "id": 15,
  "name": "新服务器01",
  "asset_type": "other",
  "ip_address": "192.168.1.200",
  "location": "数据中心B栋",
  "security_level": "中高防护级别",
  "status": "normal",
  "created_at": "2023-12-01T15:30:00",
  "updated_at": "2023-12-01T15:30:00",
  "admin_contact": "admin@example.com",
  "asset_description": "其他类型设备描述",
  "last_security_scan": "2023-12-01"
}
```

### 4. 更新资产信息
**接口地址：** `PUT /api/assets/{id}`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 资产ID |

**请求体：**
```json
{
  "name": "更新后的服务器名称",
  "asset_type": "other",
  "ip_address": "192.168.1.201",
  "location": "数据中心C栋",
  "security_level": "高防护级别",
  "status": "normal",
  "admin_contact": "newadmin@example.com"
}
```

### 5. 删除资产
**接口地址：** `DELETE /api/assets/{id}`

**路径参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | int | 是 | 资产ID |

**响应示例：**
```json
{
  "success": true,
  "message": "资产删除成功"
}
```

## 更新说明
**版本：** v2.1.0  
**更新时间：** 2023-12-01  
**更新内容：**
- 新增设备类型支持：添加"其他"类型设备，value为"other"
- 前端界面同步更新：添加资产和编辑资产弹窗均支持选择"其他"类型
- 列表筛选功能：支持按"其他"类型进行资产筛选
- 显示优化：为"其他"类型设备设置紫色标签样式

## 错误码说明
| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误或IP地址已存在 |
| 404 | 资产不存在 |
| 500 | 服务器内部错误 | 