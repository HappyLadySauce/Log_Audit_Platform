<template>
  <a-card class="stat-card" :bordered="false">
    <div class="stat-content">
      <div class="stat-icon" :style="{ backgroundColor: iconBgColor }">
        <component :is="icon" :style="{ color: iconColor }" />
      </div>
      <div class="stat-info">
        <div class="stat-value">{{ value }}</div>
        <div class="stat-label">{{ label }}</div>
        <div v-if="subtitle" class="stat-subtitle">{{ subtitle }}</div>
      </div>
    </div>
    <div v-if="trend" class="stat-trend">
      <a-tag :color="trend.type === 'increase' ? 'green' : trend.type === 'decrease' ? 'red' : 'blue'">
        <template #icon>
          <icon-arrow-up v-if="trend.type === 'increase'" />
          <icon-arrow-down v-if="trend.type === 'decrease'" />
          <icon-minus v-if="trend.type === 'stable'" />
        </template>
        {{ trend.value }}
      </a-tag>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import type { Component } from 'vue'
import { IconArrowUp, IconArrowDown, IconMinus } from '@arco-design/web-vue/es/icon'

interface Trend {
  type: 'increase' | 'decrease' | 'stable'
  value: string
}

interface Props {
  icon: Component
  iconColor?: string
  iconBgColor?: string
  value: string | number
  label: string
  subtitle?: string
  trend?: Trend
}

const props = withDefaults(defineProps<Props>(), {
  iconColor: '#fff',
  iconBgColor: '#1890ff'
})
</script>

<style scoped>
.stat-card {
  height: 120px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  align-items: center;
  height: 80px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 12px;
  font-size: 24px;
  margin-right: 16px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #1d2129;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #86909c;
  line-height: 1;
  margin-bottom: 2px;
}

.stat-subtitle {
  font-size: 12px;
  color: #c9cdd4;
  line-height: 1;
}

.stat-trend {
  margin-top: 8px;
}
</style> 