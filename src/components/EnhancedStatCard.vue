<template>
  <div class="enhanced-stat-card" :class="{ 'card-hover': !disabled }">
    <div class="card-content">
      <div class="card-header">
        <div class="icon-wrapper" :style="{ backgroundColor: iconBgColor }">
          <component :is="icon" class="card-icon" />
        </div>
        <div class="trend-indicator" v-if="trend">
          <span class="trend-value" :class="trendClass">
            <component :is="trendIcon" class="trend-icon" />
            {{ trend.value }}
          </span>
        </div>
      </div>
      
      <div class="card-body">
        <div class="main-value">
          <span class="value-display">{{ displayValue }}</span>
          <span class="value-unit" v-if="unit">{{ unit }}</span>
        </div>
        <div class="card-labels">
          <div class="primary-label">{{ label }}</div>
          <div class="secondary-label" v-if="subtitle">{{ subtitle }}</div>
        </div>
      </div>
      
      <div class="card-footer" v-if="showProgress">
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ 
              width: progressPercent + '%',
              backgroundColor: progressColor 
            }"
          ></div>
        </div>
        <div class="progress-text">{{ progressText }}</div>
      </div>
    </div>
    
    <!-- 背景装饰 -->
    <div class="card-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { 
  IconArrowUp, 
  IconArrowDown, 
  IconMinus 
} from '@arco-design/web-vue/es/icon'

interface CountUpOptions {
  useEasing: boolean
  useGrouping: boolean
  separator: string
  decimal: string
  prefix: string
  suffix: string
}

interface TrendData {
  type: 'increase' | 'decrease' | 'stable'
  value: string
}

interface Props {
  icon: any
  iconBgColor?: string
  value: string | number
  label: string
  subtitle?: string
  unit?: string
  trend?: TrendData
  disabled?: boolean
  animationDuration?: number
  showProgress?: boolean
  progressPercent?: number
  progressColor?: string
  progressText?: string
}

const props = withDefaults(defineProps<Props>(), {
  iconBgColor: '#1890ff',
  disabled: false,
  animationDuration: 2000,
  showProgress: false,
  progressPercent: 0,
  progressColor: '#52c41a',
  progressText: ''
})

// CountUp 组件简单实现
const CountUp = {
  props: {
    endVal: {
      type: Number,
      required: true
    },
    duration: {
      type: Number,
      default: 2000
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props: any) {
    const displayValue = ref(0)
    
    onMounted(() => {
      const startTime = Date.now()
      const startVal = 0
      const endVal = props.endVal
      const duration = props.duration
      
      const animate = () => {
        const now = Date.now()
        const progress = Math.min((now - startTime) / duration, 1)
        
        // 使用缓动函数
        const easeOutQuart = 1 - Math.pow(1 - progress, 4)
        displayValue.value = Math.floor(startVal + (endVal - startVal) * easeOutQuart)
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          displayValue.value = endVal
        }
      }
      
      requestAnimationFrame(animate)
    })
    
    return {
      displayValue
    }
  },
  template: '<span>{{ displayValue.toLocaleString() }}</span>'
}

// 数值处理 - 支持多种格式
const numericValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value
  }
  
  if (typeof props.value === 'string') {
    // 处理 "3K", "11.2G" 等格式
    const str = props.value.toUpperCase()
    if (str.includes('K')) {
      return parseFloat(str.replace('K', '')) * 1000
    } else if (str.includes('G')) {
      return parseFloat(str.replace('G', '')) * 1000000000
    } else if (str.includes('M')) {
      return parseFloat(str.replace('M', '')) * 1000000
    } else {
      const val = parseFloat(str)
      return isNaN(val) ? 0 : val
    }
  }
  
  return 0
})

// 显示值 - 保持原始格式
const displayValue = computed(() => {
  return props.value
})

// CountUp 配置
const countUpOptions: CountUpOptions = {
  useEasing: true,
  useGrouping: true,
  separator: ',',
  decimal: '.',
  prefix: '',
  suffix: ''
}

// 趋势样式
const trendClass = computed(() => {
  if (!props.trend) return ''
  return `trend-${props.trend.type}`
})

// 趋势图标
const trendIcon = computed(() => {
  if (!props.trend) return null
  switch (props.trend.type) {
    case 'increase':
      return IconArrowUp
    case 'decrease':
      return IconArrowDown
    case 'stable':
      return IconMinus
    default:
      return IconMinus
  }
})
</script>

<style scoped>
.enhanced-stat-card {
  position: relative;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.card-hover:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border-color: rgba(24, 144, 255, 0.3);
}

.card-content {
  position: relative;
  z-index: 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}

.card-hover:hover .icon-wrapper {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.card-icon {
  font-size: 24px;
  color: white;
}

.trend-indicator {
  display: flex;
  align-items: center;
}

.trend-value {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
}

.trend-increase {
  color: #52c41a;
}

.trend-decrease {
  color: #f5222d;
}

.trend-stable {
  color: #8c8c8c;
}

.trend-icon {
  font-size: 10px;
  margin-right: 2px;
}

.card-body {
  margin-bottom: 16px;
}

.main-value {
  display: flex;
  align-items: baseline;
  font-size: 36px;
  font-weight: 700;
  color: #262626;
  margin-bottom: 8px;
  line-height: 1;
}

.value-display {
  font-size: inherit;
  font-weight: inherit;
  color: inherit;
}

.value-unit {
  font-size: 16px;
  font-weight: 400;
  color: #8c8c8c;
  margin-left: 4px;
}

.card-labels {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.primary-label {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
}

.secondary-label {
  font-size: 12px;
  color: #8c8c8c;
}

.card-footer {
  margin-top: 16px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(90deg, currentColor 0%, rgba(255, 255, 255, 0.3) 100%);
}

.progress-text {
  font-size: 12px;
  color: #8c8c8c;
  text-align: center;
}

.card-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(24, 144, 255, 0.1), rgba(24, 144, 255, 0.05));
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 80px;
  height: 80px;
  top: -40px;
  right: -40px;
  animation-delay: 0s;
}

.circle-2 {
  width: 60px;
  height: 60px;
  bottom: -30px;
  left: -30px;
  animation-delay: 2s;
}

.circle-3 {
  width: 40px;
  height: 40px;
  top: 50%;
  right: 20px;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.5;
  }
  50% {
    transform: translateY(-10px) rotate(180deg);
    opacity: 0.8;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .enhanced-stat-card {
    padding: 16px;
  }
  
  .main-value {
    font-size: 28px;
  }
  
  .icon-wrapper {
    width: 48px;
    height: 48px;
  }
  
  .card-icon {
    font-size: 20px;
  }
}
</style> 