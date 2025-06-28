<template>
  <div id="app">
    <!-- 如果是登录页面，直接显示登录组件，否则显示带布局的页面 -->
    <BasicLayout v-if="showLayout" />
    <router-view v-else />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import BasicLayout from '@/layout/BasicLayout.vue'

const route = useRoute()

// 判断是否显示完整布局（非登录页面才显示）
const showLayout = computed(() => {
  return route.path !== '/login'
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

#app {
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
