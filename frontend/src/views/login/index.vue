<template>
  <div class="login-page">
    <!-- 背景遮罩层 -->
    <div class="background-overlay"></div>

    <!-- 主容器 -->
    <div class="login-container">
      <!-- 登录卡片 -->
      <div class="login-card">
        <!-- 头部logo和标题 -->
        <div class="login-header">
          <div class="logo-section">
            <div class="logo-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1Z" 
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 12L11 14L15 10" 
                      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h1 class="platform-title">综合日志审计分析平台</h1>
            <p class="platform-subtitle">企业级安全监控与智能分析系统</p>
          </div>
        </div>

        <!-- 登录表单区域 -->
        <div class="form-section">

          <a-form
            ref="formRef"
            :model="loginForm"
            :rules="formRules"
            layout="vertical"
            @submit="handleLogin"
            class="login-form"
          >
            <!-- 用户名输入 -->
            <a-form-item 
              field="username" 
              class="form-item"
            >
              <template #label>
                <div class="field-label">
                  <icon-user class="field-icon" />
                  <span>用户名</span>
                </div>
              </template>
              <a-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                size="large"
                class="form-input"
                allow-clear
              />
            </a-form-item>

            <!-- 密码输入 -->
            <a-form-item 
              field="password" 
              class="form-item"
            >
              <template #label>
                <div class="field-label">
                  <icon-lock class="field-icon" />
                  <span>密码</span>
                </div>
              </template>
              <a-input-password
                v-model="loginForm.password"
                placeholder="请输入密码"
                size="large"
                class="form-input"
                allow-clear
              />
            </a-form-item>

            <!-- 记住密码选项 -->
            <div class="form-options">
              <a-checkbox v-model="rememberPassword">记住密码</a-checkbox>
              <a-link class="forgot-link">忘记密码？</a-link>
            </div>

            <!-- 登录按钮 -->
            <a-form-item class="submit-item">
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                long
                :loading="isLoading"
                class="login-button"
              >
                {{ isLoading ? '登录中...' : '立即登录' }}
              </a-button>
            </a-form-item>
          </a-form>
        </div>

        <!-- 底部信息 -->
        <div class="footer-section">
          <div class="version-info">
            <span class="version">v2.1.0</span>
            <span class="separator">|</span>
            <span class="copyright">© 2024 综合日志审计分析平台</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import { IconUser, IconLock } from '@arco-design/web-vue/es/icon'

const router = useRouter()
const formRef = ref()

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 其他状态
const isLoading = ref(false)
const rememberPassword = ref(false)

// 表单验证规则
const formRules = {
  username: [
    { required: true, message: '请输入用户名' },
    { minLength: 2, message: '用户名长度不能少于2位' }
  ],
  password: [
    { required: true, message: '请输入密码' },
    { minLength: 6, message: '密码长度不能少于6位' }
  ]
}

// 登录处理函数
const handleLogin = async () => {
  try {
    const valid = await formRef.value?.validate()
    if (!valid) return

    isLoading.value = true

    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 1500))

    // 保存登录状态
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userInfo', JSON.stringify({
      username: loginForm.username,
      loginTime: new Date().toISOString(),
      rememberPassword: rememberPassword.value
    }))

    Message.success('登录成功！正在跳转...')
    
    // 跳转到主页
    setTimeout(() => {
      router.push('/')
      // 触发登录状态变更事件
      window.dispatchEvent(new Event('loginStatusChanged'))
    }, 500)

  } catch (error) {
    console.error('登录错误:', error)
    Message.error('登录失败，请检查用户名和密码')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: url('/images/55.png') center center;
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 20px 156px 20px 20px;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Helvetica Neue', sans-serif;
}



/* 背景遮罩层 */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 20, 40, 0.3) 0%, rgba(0, 40, 80, 0.2) 100%);
  z-index: 1;
}

/* 主容器 */
.login-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 440px;
}

/* 登录卡片 */
.login-card {
  background: rgba(15, 30, 50, 0.85);
  backdrop-filter: blur(25px);
  border-radius: 20px;
  padding: 24px 35px;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.3),
    0 10px 25px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(100, 200, 255, 0.2);
  position: relative;
  animation: slideInRight 0.8s ease-out;
  overflow: hidden;
}

/* 卡片内部光效 */
.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(100, 200, 255, 0.6), transparent);
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 头部区域 */
.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 12px;
  box-shadow: 
    0 15px 35px rgba(0, 210, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.platform-title {
  font-size: 26px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.platform-subtitle {
  font-size: 14px;
  color: #b8d4f0;
  margin: 0;
  font-weight: 500;
}

/* 表单区域 */
.form-section {
  margin-bottom: 20px;
}



/* 表单项 */
.form-item {
  margin-bottom: 16px;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 8px;
}

.field-icon {
  font-size: 16px;
  color: #64c8ff;
}

/* 输入框样式 */
:deep(.form-input .arco-input-wrapper) {
  height: 70px !important;
  background: rgba(30, 50, 80, 0.6) !important;
  border: 2px solid rgba(100, 200, 255, 0.3) !important;
  border-radius: 12px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

:deep(.form-input .arco-input-wrapper:hover) {
  border-color: rgba(100, 200, 255, 0.5) !important;
  background: rgba(30, 50, 80, 0.8) !important;
  box-shadow: 
    0 6px 20px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

:deep(.form-input .arco-input-wrapper.arco-input-focus) {
  border-color: #64c8ff !important;
  background: rgba(30, 50, 80, 0.9) !important;
  box-shadow: 
    0 0 0 4px rgba(100, 200, 255, 0.2),
    0 8px 25px rgba(100, 200, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

:deep(.form-input .arco-input) {
  font-size: 16px !important;
  font-weight: 500 !important;
  color: #ffffff !important;
  padding: 0 20px !important;
  border: none !important;
  background: transparent !important;
}

:deep(.form-input .arco-input::placeholder) {
  color: #9ca3af !important;
  font-weight: 400 !important;
}

/* 密码输入框特殊样式 */
:deep(.form-input .arco-input-password .arco-input-wrapper) {
  height: 70px !important;
  background: rgba(30, 50, 80, 0.6) !important;
  border: 2px solid rgba(100, 200, 255, 0.3) !important;
  border-radius: 12px !important;
}

:deep(.form-input .arco-input-password .arco-input) {
  color: #ffffff !important;
  font-size: 16px !important;
}

:deep(.form-input .arco-input-password .arco-input-suffix) {
  color: #9ca3af !important;
}

/* 复选框样式 */
:deep(.form-options .arco-checkbox) {
  color: #e2e8f0 !important;
}

:deep(.form-options .arco-checkbox .arco-checkbox-icon) {
  border-color: rgba(100, 200, 255, 0.4) !important;
  background-color: rgba(30, 50, 80, 0.6) !important;
}

:deep(.form-options .arco-checkbox.arco-checkbox-checked .arco-checkbox-icon) {
  background-color: #64c8ff !important;
  border-color: #64c8ff !important;
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px;
  color: #e2e8f0;
}

.forgot-link {
  color: #64c8ff;
  text-decoration: none;
  font-weight: 500;
}

.forgot-link:hover {
  color: #38bdf8;
  text-decoration: underline;
}

/* 提交按钮 */
.submit-item {
  margin-bottom: 0;
}

.login-button {
  height: 70px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  color: white !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 10px 30px rgba(14, 165, 233, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    0 0 0 1px rgba(14, 165, 233, 0.2);
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s ease;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
  transform: translateY(-2px);
  box-shadow: 
    0 15px 40px rgba(14, 165, 233, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    0 0 0 1px rgba(14, 165, 233, 0.3);
}

.login-button:active {
  transform: translateY(0px);
}

/* 底部区域 */
.footer-section {
  border-top: 1px solid rgba(100, 200, 255, 0.2);
  padding-top: 16px;
}



.version-info {
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

.separator {
  margin: 0 8px;
  color: #64748b;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-page {
    justify-content: center;
    padding: 20px;
  }
  
  .login-container {
    max-width: 400px;
  }
}

@media (max-width: 640px) {
  .login-page {
    padding: 16px;
  }
  
  .login-card {
    padding: 20px 28px;
  }
  
  .platform-title {
    font-size: 22px;
  }
  
  .platform-subtitle {
    font-size: 13px;
  }
  
  :deep(.form-input .arco-input-wrapper) {
    height: 65px !important;
  }
  
  .login-button {
    height: 65px !important;
    font-size: 15px !important;
  }
  

}

@media (max-width: 480px) {
  .login-card {
    padding: 17px 24px;
  }
  
  .platform-title {
    font-size: 20px;
  }
  
  .logo-icon {
    width: 60px;
    height: 60px;
  }
  
  :deep(.form-input .arco-input-wrapper) {
    height: 60px !important;
  }
  
  .login-button {
    height: 100px !important;
    font-size: 14px !important;
  }
}
</style> image.png