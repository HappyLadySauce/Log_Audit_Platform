#!/usr/bin/env python3
"""
API接口测试脚本
"""

import urllib.request
import urllib.parse
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_api(method: str, endpoint: str, data: Dict[Any, Any] = None, description: str = ""):
    """测试API接口"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n🔍 测试: {description}")
    print(f"📡 {method} {url}")
    
    try:
        # 准备请求数据
        req_data = None
        headers = {'Content-Type': 'application/json'}
        
        if data:
            req_data = json.dumps(data).encode('utf-8')
        
        # 创建请求
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        # 发送请求
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_data = response.read().decode('utf-8')
            
            print(f"📊 状态码: {status_code}")
            
            if status_code < 400:
                try:
                    result = json.loads(response_data)
                    print(f"✅ 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                except:
                    print(f"✅ 响应: {response_data}")
                return True
            else:
                print(f"❌ 错误: {response_data}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误 {e.code}: {e.read().decode('utf-8')}")
        return False
    except urllib.error.URLError as e:
        print(f"❌ 连接失败: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始API接口测试")
    print(f"🎯 测试目标: {BASE_URL}")
    
    tests = [
        # 基础接口
        ("GET", "/", None, "根路径"),
        ("GET", "/health", None, "健康检查"),
        
        # 资产管理接口
        ("GET", "/api/assets", None, "获取资产列表"),
        ("POST", "/api/assets", {
            "name": "测试K8S节点",
            "asset_type": "linux_server", 
            "ip_address": "192.168.1.100",
            "location": "测试机房",
            "security_level": "等级二"
        }, "添加新资产"),
        ("GET", "/api/assets", None, "获取更新后的资产列表"),
        
        # 告警管理接口
        ("GET", "/api/alert-rules", None, "获取告警规则"),
        ("GET", "/api/alerts", None, "获取告警记录"),
        ("GET", "/api/alerts/stats", None, "获取告警统计"),
        
        # 日志管理接口
        ("GET", "/api/logs", None, "获取日志记录"),
        
        # 仿真控制接口
        ("POST", "/api/simulation/trigger-fault", None, "触发故障"),
        ("GET", "/api/alerts/stats", None, "故障后告警统计"),
        ("GET", "/api/assets", None, "故障后资产状态"),
        
        ("POST", "/api/simulation/fix-fault", None, "修复故障"),
        ("GET", "/api/alerts/stats", None, "修复后告警统计"),
        ("GET", "/api/assets", None, "修复后资产状态"),
    ]
    
    success_count = 0
    total_count = len(tests)
    
    for method, endpoint, data, description in tests:
        success = test_api(method, endpoint, data, description)
        if success:
            success_count += 1
        
        # 添加延迟避免过快请求
        import time
        time.sleep(0.5)
    
    print(f"\n📊 测试结果:")
    print(f"✅ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有接口测试通过！")
        return True
    else:
        print("⚠️ 部分接口测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 