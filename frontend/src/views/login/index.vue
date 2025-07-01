<template>
  <div class="login-container">
    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- 简洁标题 -->
      <div class="login-header">
        <h2 class="login-title">综合日志审计分析平台</h2>
        <p class="login-subtitle">请输入您的账户信息</p>
      </div>

      <!-- 登录表单 -->
      <a-form
        ref="loginForm"
        :model="form"
        :rules="rules"
        layout="vertical"
        @submit="handleLogin"
        class="login-form"
      >
        <a-form-item field="username" class="form-item">
          <template #label>
            <span class="field-label">用户名</span>
          </template>
          <a-input
            v-model="form.username"
            placeholder="请输入用户名"
            size="large"
            class="form-input"
          />
        </a-form-item>

        <a-form-item field="password" class="form-item">
          <template #label>
            <span class="field-label">密码</span>
          </template>
          <a-input-password
            v-model="form.password"
            placeholder="请输入密码"
            size="large"
            class="form-input"
          />
        </a-form-item>

        <a-form-item class="form-item">
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            long
            :loading="loading"
            class="login-button"
          >
            <span v-if="!loading">登录</span>
            <span v-else>登录中...</span>
          </a-button>
        </a-form-item>
      </a-form>

      <!-- 版本信息 -->
      <div class="version-info">
        <p class="version-text">版本 v2.1.0 | 企业级安全认证</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'

const router = useRouter()

const form = ref({
  username: '',
  password: ''
})

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
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userInfo', JSON.stringify({
      username: form.value.username,
      loginTime: new Date().toISOString()
    }))
    
    Message.success('登录成功！')
    router.push('/')
    window.dispatchEvent(new Event('loginStatusChanged'))
  } catch (error) {
    Message.error('登录失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background-image: url('/images/33.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 298px;
  padding-left: 20px;
  padding-top: 20px;
  padding-bottom: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
  position: relative;
  overflow: hidden;
}

/* 登录卡片 */
.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  width: 100%;
  max-width: 420px;
  padding: 50px 40px 40px;
  position: relative;
  z-index: 2;
  border: 1px solid rgba(255, 255, 255, 0.6);
}

/* 登录头部 */
.login-header {
  text-align: center;
  margin-bottom: 36px;
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 10px 0;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.login-subtitle {
  font-size: 15px;
  color: #6b7280;
  margin: 0;
  font-weight: 400;
}

/* 表单样式 */
.form-item {
  margin-bottom: 24px;
}

.field-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

/* 输入框样式 */
:deep(.form-input .arco-input-wrapper) {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  height: 56px;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

:deep(.form-input .arco-input-wrapper:hover) {
  border-color: #cbd5e1;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  transform: translateY(-1px);
}

:deep(.form-input .arco-input-wrapper.arco-input-focus) {
  border-color: #3b82f6;
  background: rgba(255, 255, 255, 1);
  box-shadow: 
    0 0 0 4px rgba(59, 130, 246, 0.08),
    0 6px 20px rgba(59, 130, 246, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 1);
  transform: translateY(-1px);
}

:deep(.form-input .arco-input) {
  background: transparent;
  color: #1f2937;
  font-size: 16px;
  font-weight: 500;
  padding: 0 18px;
  line-height: 1.4;
}

:deep(.form-input .arco-input::placeholder) {
  color: #94a3b8;
  font-weight: 400;
  font-size: 15px;
}

/* 登录按钮 */
.login-button {
  height: 56px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border: none;
  border-radius: 12px;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px rgba(59, 130, 246, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  margin-top: 8px;
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
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(59, 130, 246, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.login-button:active {
  transform: translateY(-1px);
}

/* 版本信息 */
.version-info {
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.version-text {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
  font-weight: 400;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .login-container {
    padding: 20px;
    justify-content: center;
  }
  
  .login-card {
    max-width: 100%;
    padding: 40px 24px 32px;
  }
  
  .login-title {
    font-size: 20px;
  }
  
  .login-subtitle {
    font-size: 13px;
  }
  
  .form-item {
    margin-bottom: 20px;
  }
  
  :deep(.form-input .arco-input-wrapper) {
    height: 52px;
  }
  
  .login-button {
    height: 52px;
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 20px 28px;
  }
  
  .login-title {
    font-size: 18px;
  }
  
  .login-subtitle {
    font-size: 12px;
  }
  
  :deep(.form-input .arco-input-wrapper) {
    height: 48px;
  }
  
  .login-button {
    height: 48px;
    font-size: 14px;
  }

  .version-info {
    margin-top: 24px;
    padding-top: 16px;
  }
}
</style> 