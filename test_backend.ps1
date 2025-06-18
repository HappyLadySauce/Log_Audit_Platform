# 测试后端服务器
Write-Host "🔧 测试后端服务器状态..." -ForegroundColor Yellow

# 等待几秒钟让服务器启动
Start-Sleep -Seconds 5

try {
    # 测试健康检查端点
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 10
    Write-Host "✅ 后端健康检查成功: $($healthResponse | ConvertTo-Json)" -ForegroundColor Green
    
    # 初始化数据库
    Write-Host "🔧 初始化数据库..." -ForegroundColor Yellow
    $initResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/init-database" -Method Post -TimeoutSec 30
    Write-Host "✅ 数据库初始化结果: $($initResponse | ConvertTo-Json)" -ForegroundColor Green
    
    # 测试资产API
    Write-Host "🔧 测试资产API..." -ForegroundColor Yellow
    $assetsResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/assets" -Method Get -TimeoutSec 10
    Write-Host "✅ 资产API测试成功，返回 $($assetsResponse.Count) 个资产" -ForegroundColor Green
    
    Write-Host "🎉 后端服务器运行正常！" -ForegroundColor Green
    
} catch {
    Write-Host "❌ 后端测试失败: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "详细错误: $($_.Exception)" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键继续..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 