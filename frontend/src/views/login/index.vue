<template>
  <div class="login-container">
    <div class="login-background">
      <div class="background-overlay"></div>
    </div>
    
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <icon-desktop class="logo-icon" />
          <h1 class="system-title">综合日志审计分析平台</h1>
        </div>
        <p class="login-subtitle">请登录您的账户</p>
      </div>

      <a-form
        ref="loginForm"
        :model="form"
        :rules="rules"
        layout="vertical"
        @submit="handleLogin"
        class="login-form"
      >
        <a-form-item field="username" label="用户名">
          <a-input
            v-model="form.username"
            placeholder="请输入用户名"
            size="large"
          >
            <template #prefix>
              <icon-user />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item field="password" label="密码">
          <a-input-password
            v-model="form.password"
            placeholder="请输入密码"
            size="large"
          >
            <template #prefix>
              <icon-lock />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <div class="login-options">
            <a-checkbox v-model="rememberMe">记住我</a-checkbox>
            <a-link>忘记密码？</a-link>
          </div>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            long
            :loading="loading"
            class="login-button"
          >
            登录
          </a-button>
        </a-form-item>
      </a-form>

      <div class="login-footer">
        <p class="copyright">© 2025 综合综合日志审计分析平台. All rights reserved.</p>
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
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: url('/images/33.jpg') center/cover no-repeat;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.3) 0%, transparent 50%);
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 30, 60, 0.3) 0%, rgba(0, 50, 120, 0.2) 100%);
}

.login-card {
  position: relative;
  z-index: 1;
  background: rgba(15, 25, 45, 0.85);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 40px;
  width: 420px;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.5),
    0 15px 30px rgba(0, 120, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(100, 150, 255, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.logo-icon {
  font-size: 48px;
  color: #64b5f6;
  margin-right: 12px;
}

.system-title {
  font-size: 28px;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.login-subtitle {
  color: #b3d4fc;
  font-size: 16px;
  margin: 0;
}

.login-form {
  margin-bottom: 24px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0;
}

.login-button {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
  border: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(66, 165, 245, 0.4);
}

.login-button:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%);
  box-shadow: 0 8px 25px rgba(66, 165, 245, 0.6);
}

.login-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid rgba(100, 150, 255, 0.2);
}

.copyright {
  color: #9bb5d6;
  font-size: 14px;
  margin: 0;
}

:deep(.arco-input-wrapper) {
  border-radius: 8px;
  border: 1px solid rgba(100, 150, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

:deep(.arco-input-wrapper:hover) {
  border-color: #64b5f6;
  background: rgba(255, 255, 255, 0.15);
}

:deep(.arco-input-wrapper.arco-input-focus) {
  border-color: #64b5f6;
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 0 2px rgba(100, 181, 246, 0.2);
}

:deep(.arco-form-item-label) {
  font-weight: 500;
  color: #ffffff;
}

:deep(.arco-input) {
  background: transparent;
  color: #ffffff;
}

:deep(.arco-input::placeholder) {
  color: rgba(255, 255, 255, 0.6);
}

:deep(.arco-input-prefix) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.arco-checkbox-label) {
  color: #ffffff;
}

:deep(.arco-link) {
  color: #64b5f6;
}
</style> 