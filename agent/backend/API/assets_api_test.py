#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产管理API接口测试脚本
测试新增的"其他"设备类型功能
"""

import requests
import json
import time
from datetime import datetime

# 配置API基础地址
BASE_URL = "http://localhost:8000/api"

class AssetsAPITest:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_asset_id = None
        
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✓ 通过" if success else "✗ 失败"
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {test_name}: {status}")
        if message:
            print(f"    {message}")
        print()
    
    def test_get_assets_list(self):
        """测试获取资产列表"""
        try:
            response = self.session.get(f"{self.base_url}/assets")
            success = response.status_code == 200
            data = response.json() if success else None
            
            message = f"返回 {len(data)} 个资产" if success else f"状态码: {response.status_code}"
            self.log_test("获取资产列表", success, message)
            
            return data
        except Exception as e:
            self.log_test("获取资产列表", False, f"异常: {str(e)}")
            return None
    
    def test_create_other_asset(self):
        """测试创建"其他"类型资产"""
        test_data = {
            "name": "测试其他设备_" + str(int(time.time())),
            "asset_type": "other",
            "ip_address": f"192.168.{int(time.time()) % 255}.{int(time.time()) % 255}",
            "location": "测试环境机房",
            "security_level": "中高防护级别",
            "admin_contact": "test@example.com",
            "asset_description": "API测试创建的其他类型设备",
            "last_security_scan": "2023-12-01"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/assets",
                json=test_data
            )
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.test_asset_id = data.get("id")
                message = f"创建成功，ID: {self.test_asset_id}, 类型: {data.get('asset_type')}"
            else:
                message = f"创建失败，状态码: {response.status_code}"
                
            self.log_test("创建其他类型资产", success, message)
            return data if success else None
            
        except Exception as e:
            self.log_test("创建其他类型资产", False, f"异常: {str(e)}")
            return None
    
    def test_get_asset_detail(self):
        """测试获取资产详情"""
        if not self.test_asset_id:
            self.log_test("获取资产详情", False, "没有可用的测试资产ID")
            return None
            
        try:
            response = self.session.get(f"{self.base_url}/assets/{self.test_asset_id}")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                message = f"获取成功，设备: {data.get('name')}, 类型: {data.get('asset_type')}"
            else:
                message = f"获取失败，状态码: {response.status_code}"
                
            self.log_test("获取资产详情", success, message)
            return data if success else None
            
        except Exception as e:
            self.log_test("获取资产详情", False, f"异常: {str(e)}")
            return None
    
    def test_update_other_asset(self):
        """测试更新"其他"类型资产"""
        if not self.test_asset_id:
            self.log_test("更新其他类型资产", False, "没有可用的测试资产ID")
            return None
            
        update_data = {
            "name": "更新后的其他设备_" + str(int(time.time())),
            "asset_type": "other",
            "ip_address": f"10.0.{int(time.time()) % 255}.{int(time.time()) % 255}",
            "location": "更新后的测试机房位置",
            "security_level": "高防护级别",
            "status": "normal",
            "admin_contact": "updated@example.com"
        }
        
        try:
            response = self.session.put(
                f"{self.base_url}/assets/{self.test_asset_id}",
                json=update_data
            )
            success = response.status_code == 200
            
            if success:
                data = response.json()
                message = f"更新成功，新名称: {data.get('name')}"
            else:
                message = f"更新失败，状态码: {response.status_code}"
                
            self.log_test("更新其他类型资产", success, message)
            return data if success else None
            
        except Exception as e:
            self.log_test("更新其他类型资产", False, f"异常: {str(e)}")
            return None
    
    def test_filter_by_type(self):
        """测试按类型筛选资产"""
        try:
            # 测试筛选"其他"类型
            response = self.session.get(f"{self.base_url}/assets?asset_type=other")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                other_count = len(data)
                message = f"筛选到 {other_count} 个其他类型设备"
            else:
                message = f"筛选失败，状态码: {response.status_code}"
                
            self.log_test("按其他类型筛选", success, message)
            
            # 测试筛选其他类型
            for asset_type in ["linux_server", "windows_server", "network_device"]:
                response = self.session.get(f"{self.base_url}/assets?asset_type={asset_type}")
                if response.status_code == 200:
                    count = len(response.json())
                    print(f"    {asset_type}: {count} 个设备")
                    
        except Exception as e:
            self.log_test("按类型筛选", False, f"异常: {str(e)}")
    
    def test_delete_asset(self):
        """测试删除资产"""
        if not self.test_asset_id:
            self.log_test("删除测试资产", False, "没有可用的测试资产ID")
            return
            
        try:
            response = self.session.delete(f"{self.base_url}/assets/{self.test_asset_id}")
            success = response.status_code == 200
            
            if success:
                data = response.json()
                message = f"删除成功: {data.get('message', '删除完成')}"
            else:
                message = f"删除失败，状态码: {response.status_code}"
                
            self.log_test("删除测试资产", success, message)
            
        except Exception as e:
            self.log_test("删除测试资产", False, f"异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("资产管理API接口测试")
        print("=" * 60)
        print(f"测试目标: {self.base_url}")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        # 1. 获取资产列表
        self.test_get_assets_list()
        
        # 2. 创建"其他"类型资产
        self.test_create_other_asset()
        
        # 3. 获取资产详情
        self.test_get_asset_detail()
        
        # 4. 更新资产信息
        self.test_update_other_asset()
        
        # 5. 按类型筛选
        self.test_filter_by_type()
        
        # 6. 删除测试资产
        self.test_delete_asset()
        
        print("=" * 60)
        print("测试完成")
        print("=" * 60)

def main():
    """主函数"""
    tester = AssetsAPITest()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 