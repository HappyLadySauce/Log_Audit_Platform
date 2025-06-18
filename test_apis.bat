@echo off
chcp 65001
echo =======================================
echo       API接口测试批处理脚本
echo =======================================

echo.
echo 🔍 测试健康检查接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method Get; Write-Host '✅ 健康检查成功:' $response } catch { Write-Host '❌ 健康检查失败:' $_.Exception.Message }"

echo.
echo 🔍 测试根路径接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/' -Method Get; Write-Host '✅ 根路径成功:' $response.message } catch { Write-Host '❌ 根路径失败:' $_.Exception.Message }"

echo.
echo 🔍 测试资产列表接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/assets' -Method Get; Write-Host '✅ 资产列表成功，共' $response.Count '条记录' } catch { Write-Host '❌ 资产列表失败:' $_.Exception.Message }"

echo.
echo 🔍 测试告警规则接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/alert-rules' -Method Get; Write-Host '✅ 告警规则成功，共' $response.Count '条规则' } catch { Write-Host '❌ 告警规则失败:' $_.Exception.Message }"

echo.
echo 🔍 测试告警统计接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/alerts/stats' -Method Get; Write-Host '✅ 告警统计成功: 待处理:' $response.pending ', 处理中:' $response.processing ', 已解决:' $response.resolved } catch { Write-Host '❌ 告警统计失败:' $_.Exception.Message }"

echo.
echo 🔍 测试触发故障接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/simulation/trigger-fault' -Method Post; Write-Host '✅ 触发故障成功:' $response.message } catch { Write-Host '❌ 触发故障失败:' $_.Exception.Message }"

timeout /t 2 /nobreak >nul

echo.
echo 🔍 再次检查告警统计...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/alerts/stats' -Method Get; Write-Host '✅ 故障后告警统计: 待处理:' $response.pending ', 处理中:' $response.processing ', 已解决:' $response.resolved } catch { Write-Host '❌ 告警统计失败:' $_.Exception.Message }"

echo.
echo 🔍 测试修复故障接口...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/simulation/fix-fault' -Method Post; Write-Host '✅ 修复故障成功:' $response.message } catch { Write-Host '❌ 修复故障失败:' $_.Exception.Message }"

timeout /t 2 /nobreak >nul

echo.
echo 🔍 最终检查告警统计...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/alerts/stats' -Method Get; Write-Host '✅ 修复后告警统计: 待处理:' $response.pending ', 处理中:' $response.processing ', 已解决:' $response.resolved } catch { Write-Host '❌ 告警统计失败:' $_.Exception.Message }"

echo.
echo =======================================
echo          🎉 API测试完成！
echo =======================================
echo.
echo 📝 如需查看详细API文档，请访问:
echo    http://localhost:8000/docs
echo.
echo 按任意键退出...
pause >nul 