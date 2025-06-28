<template>
  <div class="login-container">
    <div class="login-background">
      <div class="background-overlay"></div>
    </div>
    
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <icon-desktop class="logo-icon" />
          <h1 class="system-title">日志审计平台</h1>
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
        <p class="copyright">© 2024 日志审计平台. All rights reserved.</p>
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
  overflow: hidden;
  /* ======== 背景选择 ======== */
  /* 方案1: 使用本地图片作为背景 (将图片放在 public/images/ 目录下) */
  /* background: url('/images/login-bg.jpg') center/cover no-repeat; */
  
  /* 方案2: 使用网络图片作为背景 (当前启用) */
  background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80') center/cover no-repeat;
  
  /* 方案3: 使用渐变背景 */
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
  
  /* 备用背景色（如果图片加载失败） */
  background-color: #667eea;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3); /* 深色半透明遮罩，提高文字可读性 */
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.2); /* 额外的深色遮罩层 */
}

.login-card {
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 48px;
  width: 420px;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.25),
    0 15px 30px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.3);
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
  color: #667eea;
  margin-right: 12px;
}

.system-title {
  font-size: 28px;
  font-weight: 600;
  color: #1d2129;
  margin: 0;
}

.login-subtitle {
  color: #86909c;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.login-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid #e5e6eb;
}

.copyright {
  color: #86909c;
  font-size: 14px;
  margin: 0;
}

:deep(.arco-input-wrapper) {
  border-radius: 8px;
  border: 1px solid #e5e6eb;
  transition: all 0.3s ease;
}

:deep(.arco-input-wrapper:hover) {
  border-color: #667eea;
}

:deep(.arco-input-wrapper.arco-input-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

:deep(.arco-form-item-label) {
  font-weight: 500;
  color: #1d2129;
}
</style> 