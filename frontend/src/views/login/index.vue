<template>
  <div class="login-container">
    <!-- 左侧安全审计元素展示 -->
    <div class="security-section">
      <div class="security-content">
        <div class="system-info">
          <h2 class="system-title">综合日志审计分析平台</h2>
          <p class="system-desc">Log Audit Analysis Platform</p>
        </div>
        
        <!-- 功能特性列表 -->
        <div class="features-section">
          <div class="feature-list">
            <div class="feature-item">
              <div class="feature-dot"></div>
              <div class="feature-text">
                <span class="feature-title">全方位安全防护</span>
                <span class="feature-desc">多层次安全防护体系，确保系统安全</span>
              </div>
            </div>
            
            <div class="feature-item">
              <div class="feature-dot"></div>
              <div class="feature-text">
                <span class="feature-title">完整审计追踪</span>
                <span class="feature-desc">记录所有操作行为，提供完整审计链</span>
              </div>
            </div>
            
            <div class="feature-item">
              <div class="feature-dot"></div>
              <div class="feature-text">
                <span class="feature-title">实时监控告警</span>
                <span class="feature-desc">7×24小时实时监控，及时发现异常</span>
              </div>
            </div>
            
            <div class="feature-item">
              <div class="feature-dot"></div>
              <div class="feature-text">
                <span class="feature-title">智能数据分析</span>
                <span class="feature-desc">AI驱动的行为分析，精准识别威胁</span>
              </div>
            </div>
            
            <div class="feature-item">
              <div class="feature-dot"></div>
              <div class="feature-text">
                <span class="feature-title">企业级加密</span>
                <span class="feature-desc">端到端加密保护，确保数据安全</span>
              </div>
            </div>
          </div>
          
          <!-- 装饰性元素 -->
          <div class="decorative-elements">
            <div class="floating-shape shape-1"></div>
            <div class="floating-shape shape-2"></div>
            <div class="floating-shape shape-3"></div>
            <div class="pulse-ring"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧登录区域 -->
    <div class="login-section">
      <div class="login-card">
        <div class="login-header">
          <div class="brand-icon">
            <icon-desktop />
          </div>
          <h3 class="login-title">系统登录</h3>
          <p class="login-subtitle">请输入您的登录凭据</p>
        </div>

        <a-form
          ref="loginForm"
          :model="form"
          :rules="rules"
          layout="vertical"
          @submit="handleLogin"
          class="login-form"
        >
          <a-form-item field="username">
            <a-input
              v-model="form.username"
              placeholder="用户名或邮箱"
              size="large"
              class="tech-input"
            >
              <template #prefix>
                <icon-user />
              </template>
            </a-input>
          </a-form-item>

          <a-form-item field="password">
            <a-input-password
              v-model="form.password"
              placeholder="密码"
              size="large"
              class="tech-input"
            >
              <template #prefix>
                <icon-lock />
              </template>
            </a-input-password>
          </a-form-item>

          <div class="login-options">
            <a-checkbox v-model="rememberMe" class="remember-me">记住登录状态</a-checkbox>
          </div>

          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              long
              :loading="loading"
              class="tech-login-button"
            >
              <span v-if="!loading">登录系统</span>
              <span v-else>验证中...</span>
            </a-button>
          </a-form-item>
        </a-form>

        <div class="login-footer">
          <p class="version-info">Version 2.1.0</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import { IconDesktop, IconUser, IconLock } from '@arco-design/web-vue/es/icon'

const router = useRouter()

const form = ref({
  username: '',
  password: ''
})

const rememberMe = ref(false)
const loading = ref(false)

const rules = {
  username: [
    { required: true, message: '请输入用户名' }
  ],
  password: [
    { required: true, message: '请输入密码' }
  ]
}

const handleLogin = async () => {
  loading.value = true
  
  // 模拟登录延迟
  setTimeout(() => {
    // 设置登录状态
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userInfo', JSON.stringify({
      username: form.value.username,
      loginTime: new Date().toISOString()
    }))
    
    Message.success('登录成功！')
    loading.value = false
    
    // 跳转到主页
    router.push('/')
    
    // 触发登录状态变化事件
    window.dispatchEvent(new Event('loginStatusChanged'))
  }, 1000)
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f1419 0%, #1a1f36 50%, #151b2d 100%);
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 50%, rgba(168, 85, 247, 0.05) 100%),
    linear-gradient(90deg, rgba(59, 130, 246, 0.02) 1px, transparent 1px),
    linear-gradient(rgba(59, 130, 246, 0.02) 1px, transparent 1px);
  background-size: 100% 100%, 40px 40px, 40px 40px;
  pointer-events: none;
}

/* 左侧安全审计元素区域 */
.security-section {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 60px 40px 60px 80px;
  position: relative;
}

.security-content {
  width: 100%;
  max-width: 600px;
}

.system-info {
  margin-bottom: 80px;
  text-align: center;
}

.system-title {
  font-size: 47px;
  font-weight: 300;
  color: #ffffff;
  margin: 0 0 16px 0;
  letter-spacing: -0.5px;
}

.system-desc {
  font-size: 21px;
  color: rgba(148, 163, 184, 0.8);
  margin: 0;
  font-weight: 300;
  letter-spacing: 0.5px;
}

/* 功能特性列表 */
.features-section {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feature-list {
  max-width: 480px;
  width: 100%;
  margin-left: 114px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 38px;
  opacity: 0;
  transform: translateX(-30px);
  animation: slideInUp 0.6s ease forwards;
}

.feature-item:nth-child(1) { animation-delay: 0.1s; }
.feature-item:nth-child(2) { animation-delay: 0.2s; }
.feature-item:nth-child(3) { animation-delay: 0.3s; }
.feature-item:nth-child(4) { animation-delay: 0.4s; }
.feature-item:nth-child(5) { animation-delay: 0.5s; }

.feature-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  margin-right: 24px;
  margin-top: 8px;
  flex-shrink: 0;
  position: relative;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

.feature-dot::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.feature-text {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.feature-title {
  font-size: 22px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}

.feature-desc {
  font-size: 16px;
  color: #94a3b8;
  line-height: 1.5;
  font-weight: 400;
}

/* 装饰性元素 */
.decorative-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
}

.shape-1 {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  top: 10%;
  right: 15%;
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #10b981, #059669);
  top: 60%;
  right: 10%;
  animation: float 8s ease-in-out infinite reverse;
}

.shape-3 {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  bottom: 20%;
  right: 20%;
  animation: float 7s ease-in-out infinite;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  right: 12%;
  width: 200px;
  height: 200px;
  border: 2px solid rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  transform: translate(50%, -50%);
  animation: pulse 3s infinite;
}

/* 动画效果 */
@keyframes slideInUp {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.1;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 右侧登录区域 */
.login-section {
  width: 550px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 22px 60px 20px;
  transform: translateX(-114px);
}

.login-card {
  background: rgba(30, 41, 59, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 45px;
  width: 100%;
  max-width: 480px;
  border: 1px solid rgba(71, 85, 105, 0.4);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.brand-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 12px;
  margin-bottom: 20px;
  color: white;
  font-size: 24px;
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 8px 0;
}

.login-subtitle {
  font-size: 14px;
  color: #94a3b8;
  margin: 0;
  font-weight: 400;
}

.login-form .arco-form-item {
  margin-bottom: 20px;
}

.login-options {
  margin: 20px 0 24px 0;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.version-info {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  font-family: 'Monaco', 'Consolas', monospace;
}

/* 科技风输入框 */
:deep(.tech-input .arco-input-wrapper) {
  background: rgba(51, 65, 85, 0.4);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  height: 48px;
  transition: all 0.3s ease;
}

:deep(.tech-input .arco-input-wrapper:hover) {
  border-color: rgba(59, 130, 246, 0.6);
  background: rgba(51, 65, 85, 0.6);
}

:deep(.tech-input .arco-input-wrapper.arco-input-focus) {
  border-color: #3b82f6;
  background: rgba(51, 65, 85, 0.8);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.tech-input .arco-input) {
  background: transparent;
  color: #ffffff;
  font-size: 15px;
}

:deep(.tech-input .arco-input::placeholder) {
  color: rgba(148, 163, 184, 0.6);
}

:deep(.tech-input .arco-input-prefix) {
  color: rgba(148, 163, 184, 0.8);
}

/* 科技风登录按钮 */
.tech-login-button {
  height: 48px;
  font-size: 15px;
  font-weight: 500;
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  border: none;
  border-radius: 10px;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
  letter-spacing: 0.3px;
}

.tech-login-button:hover {
  transform: translateY(-1px);
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.tech-login-button:active {
  transform: translateY(0);
}

/* 记住我选项 */
:deep(.remember-me .arco-checkbox-label) {
  color: #cbd5e1;
  font-size: 14px;
}

:deep(.remember-me .arco-checkbox) {
  color: #3b82f6;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .security-section {
    padding: 40px 20px;
  }
  
  .login-section {
    width: 480px;
    padding: 40px 40px 40px 20px;
    transform: translateX(-80px);
  }
  
  .feature-list {
    max-width: 400px;
    margin-left: 80px;
  }
  
  .feature-item {
    margin-bottom: 28px;
  }
  
  .feature-dot {
    width: 13px;
    height: 13px;
    margin-right: 22px;
    margin-top: 7px;
  }
  
  .feature-title {
    font-size: 20px;
  }
  
  .feature-desc {
    font-size: 15px;
  }
}

@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }
  
  .security-section {
    padding: 30px 20px 20px 20px;
  }
  
  .login-section {
    width: 100%;
    padding: 20px;
    transform: translateX(0);
  }
  
  .system-title {
    font-size: 28px;
  }
  
  .system-desc {
    font-size: 16px;
  }
  
  .feature-list {
    max-width: 320px;
    margin-left: 20px;
  }
  
  .feature-item {
    margin-bottom: 24px;
  }
  
  .feature-dot {
    width: 12px;
    height: 12px;
    margin-right: 20px;
    margin-top: 6px;
  }
  
  .feature-title {
    font-size: 18px;
  }
  
  .feature-desc {
    font-size: 14px;
  }
  
  .decorative-elements {
    display: none;
  }
}
</style> 