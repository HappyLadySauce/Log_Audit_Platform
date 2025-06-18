import urllib.request
import json

def test_get(url, description):
    print(f"\n🔍 测试: {description}")
    print(f"📡 GET {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            status_code = response.getcode()
            data = response.read().decode('utf-8')
            
            print(f"📊 状态码: {status_code}")
            
            if status_code == 200:
                try:
                    result = json.loads(data)
                    print(f"✅ 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                except:
                    print(f"✅ 响应: {data}")
                return True
            else:
                print(f"❌ 错误: {data}")
                return False
                
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

# 测试基本接口
base_url = "http://localhost:8000"

print("🚀 开始API接口测试")

tests = [
    (f"{base_url}/", "根路径"),
    (f"{base_url}/health", "健康检查"),
    (f"{base_url}/api/assets", "获取资产列表"),
    (f"{base_url}/api/alert-rules", "获取告警规则"),
    (f"{base_url}/api/alerts", "获取告警记录"),
    (f"{base_url}/api/alerts/stats", "获取告警统计"),
    (f"{base_url}/api/logs", "获取日志记录"),
]

success_count = 0
for url, description in tests:
    if test_get(url, description):
        success_count += 1

print(f"\n📊 测试结果: {success_count}/{len(tests)} 成功") 