<template>
  <div class="base-chart" :style="{ height: height, width: width }">
    <v-chart
      :option="chartOption"
      :loading="loading"
      :loading-options="loadingOptions"
      autoresize
      @click="handleClick"
      @mouseover="handleMouseover"
      @mouseout="handleMouseout"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import {
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  RadarChart,
  GaugeChart
} from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  PolarComponent
} from 'echarts/components'

// 注册必要的组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  ScatterChart,
  RadarChart,
  GaugeChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  PolarComponent
])

interface Props {
  option: any
  height?: string
  width?: string
  loading?: boolean
  theme?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px',
  width: '100%',
  loading: false,
  theme: 'default'
})

const emit = defineEmits<{
  click: [params: any]
  mouseover: [params: any]
  mouseout: [params: any]
}>()

// 加载动画配置
const loadingOptions = ref({
  text: '加载中...',
  color: '#1890ff',
  textColor: '#000',
  maskColor: 'rgba(255, 255, 255, 0.8)',
  zlevel: 0,
  fontSize: 12,
  showSpinner: true,
  spinnerRadius: 10,
  lineWidth: 5
})

// 默认动画配置
const defaultAnimation = {
  animation: true,
  animationThreshold: 2000,
  animationDuration: 1000,
  animationEasing: 'cubicOut',
  animationDelay: 0,
  animationDurationUpdate: 300,
  animationEasingUpdate: 'cubicOut',
  animationDelayUpdate: 0
}

// 合并配置
const chartOption = computed(() => {
  return {
    ...defaultAnimation,
    ...props.option,
    backgroundColor: 'transparent'
  }
})

// 事件处理
const handleClick = (params: any) => {
  emit('click', params)
}

const handleMouseover = (params: any) => {
  emit('mouseover', params)
}

const handleMouseout = (params: any) => {
  emit('mouseout', params)
}

// 监听配置变化
watch(
  () => props.option,
  () => {
    // 可以在这里添加配置变化时的处理逻辑
  },
  { deep: true }
)
</script>

<style scoped>
.base-chart {
  position: relative;
  transition: all 0.3s ease;
}

.base-chart:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
</style> 