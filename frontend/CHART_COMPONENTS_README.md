# 综合日志审计平台 - ECharts 图表组件使用指南

## 概述

本项目已集成了基于 ECharts 的高级图表组件系统，提供了炫酷的动画效果、响应式布局和丰富的交互功能。

## 核心组件

### 1. BaseChart 基础图表组件

最底层的图表组件，封装了 ECharts 的基本功能。

```vue
<BaseChart
  :option="chartOption"
  height="400px"
  width="100%"
  :loading="false"
  @click="handleClick"
/>
```

**Props:**
- `option`: ECharts 配置对象
- `height`: 图表高度 (默认: '400px')
- `width`: 图表宽度 (默认: '100%')
- `loading`: 是否显示加载状态
- `theme`: 主题名称

**Events:**
- `click`: 图表点击事件
- `mouseover`: 鼠标悬停事件
- `mouseout`: 鼠标离开事件

### 2. DashboardChart 仪表盘图表组件

专为仪表盘设计的高级图表组件，支持多种图表类型。

```vue
<DashboardChart
  type="line"
  :data="chartData"
  title="数据趋势"
  height="350px"
  :smooth="true"
  :colors="['#1890ff', '#52c41a']"
  @chartClick="handleChartClick"
/>
```

**Props:**
- `type`: 图表类型 ('line' | 'bar' | 'pie' | 'gauge' | 'area' | 'scatter' | 'radar')
- `data`: 图表数据数组
- `title`: 图表标题
- `height`: 图表高度
- `width`: 图表宽度
- `loading`: 加载状态
- `colors`: 颜色数组
- `showLegend`: 是否显示图例
- `showGrid`: 是否显示网格
- `smooth`: 线图是否平滑

**数据格式:**
```javascript
// 线图/柱状图数据
const lineData = [
  { name: '1月', value: 120 },
  { name: '2月', value: 180 },
  { name: '3月', value: 150 }
]

// 饼图数据
const pieData = [
  { name: '类型A', value: 35 },
  { name: '类型B', value: 25 },
  { name: '类型C', value: 40 }
]

// 雷达图数据
const radarData = [
  { name: '指标1', value: 85, max: 100 },
  { name: '指标2', value: 72, max: 100 },
  { name: '指标3', value: 68, max: 100 }
]

// 仪表盘数据
const gaugeData = [{ value: 75 }]
```

### 3. EnhancedStatCard 增强统计卡片

带有动画效果和进度条的统计卡片组件。

```vue
<EnhancedStatCard
  :icon="IconDesktop"
  icon-bg-color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
  :value="1234"
  label="总设备数"
  subtitle="在线设备"
  unit="台"
  :trend="{ type: 'increase', value: '+12%' }"
  :show-progress="true"
  :progress-percent="85"
  progress-color="#667eea"
  progress-text="健康度 85%"
/>
```

**Props:**
- `icon`: 图标组件
- `iconBgColor`: 图标背景色（支持渐变）
- `value`: 主要数值
- `label`: 主标签
- `subtitle`: 副标签
- `unit`: 数值单位
- `trend`: 趋势对象 `{ type: 'increase' | 'decrease' | 'stable', value: string }`
- `showProgress`: 是否显示进度条
- `progressPercent`: 进度百分比
- `progressColor`: 进度条颜色
- `progressText`: 进度条文本

## 图表配置工具类

### ChartConfig 类

提供统一的图表配置和样式管理。

```typescript
import { ChartConfig } from '@/utils/chartConfig'

// 获取线图配置
const lineOption = ChartConfig.getLineChartConfig({
  data: chartData,
  title: '趋势分析',
  smooth: true,
  area: true,
  colors: ChartConfig.COLORS.primary
})

// 获取饼图配置
const pieOption = ChartConfig.getPieChartConfig({
  data: pieData,
  title: '分布统计',
  colors: ChartConfig.COLORS.primary,
  showLegend: true
})

// 获取仪表盘配置
const gaugeOption = ChartConfig.getGaugeChartConfig({
  value: 75,
  title: 'CPU使用率',
  color: '#1890ff'
})
```

### 预定义颜色主题

```typescript
// 主要颜色
ChartConfig.COLORS.primary
// ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2']

// 渐变色
ChartConfig.COLORS.gradient
// 包含多种渐变色配置

// 状态颜色
ChartConfig.COLORS.status
// { success: '#52c41a', warning: '#faad14', error: '#f5222d', ... }
```

## 使用示例

### 1. 创建趋势分析图表

```vue
<template>
  <a-card title="日志采集趋势">
    <DashboardChart
      type="area"
      :data="trendData"
      height="350px"
      :smooth="true"
      :colors="['#1890ff', '#52c41a', '#faad14']"
    />
  </a-card>
</template>

<script setup>
import { ref } from 'vue'
import DashboardChart from '@/components/DashboardChart.vue'

const trendData = ref([
  { name: '00:00', value: 120 },
  { name: '04:00', value: 80 },
  { name: '08:00', value: 300 },
  { name: '12:00', value: 450 },
  { name: '16:00', value: 380 },
  { name: '20:00', value: 280 }
])
</script>
```

### 2. 创建状态分布饼图

```vue
<template>
  <a-card title="设备状态分布">
    <DashboardChart
      type="pie"
      :data="statusData"
      height="300px"
      :colors="['#52c41a', '#faad14', '#f5222d']"
    />
  </a-card>
</template>

<script setup>
const statusData = ref([
  { name: '正常', value: 156 },
  { name: '警告', value: 23 },
  { name: '错误', value: 8 }
])
</script>
```

### 3. 创建系统监控仪表盘

```vue
<template>
  <a-card title="CPU使用率">
    <DashboardChart
      type="gauge"
      :data="[{ value: cpuUsage }]"
      height="250px"
    />
  </a-card>
</template>

<script setup>
const cpuUsage = ref(75)
</script>
```

### 4. 创建威胁雷达图

```vue
<template>
  <a-card title="安全威胁评估">
    <DashboardChart
      type="radar"
      :data="threatData"
      height="300px"
      :colors="['#f5222d', '#faad14']"
    />
  </a-card>
</template>

<script setup>
const threatData = ref([
  { name: '恶意软件', value: 20, max: 100 },
  { name: '网络攻击', value: 35, max: 100 },
  { name: '数据泄露', value: 15, max: 100 },
  { name: '权限滥用', value: 25, max: 100 },
  { name: '系统漏洞', value: 40, max: 100 }
])
</script>
```

## 动画和交互

### 1. 数据更新动画

所有图表都支持数据更新时的平滑动画过渡：

```javascript
// 更新数据时会自动触发动画
trendData.value = newData
```

### 2. 悬停效果

图表支持丰富的悬停交互效果：
- 数据点高亮
- 工具提示显示
- 图例联动
- 区域聚焦

### 3. 点击事件

```vue
<DashboardChart
  @chartClick="handleChartClick"
/>

<script setup>
const handleChartClick = (params) => {
  console.log('点击的数据:', params)
  // 处理点击事件
}
</script>
```

## 响应式设计

所有组件都支持响应式布局：

```vue
<a-row :gutter="[24, 24]">
  <a-col :xs="24" :lg="16">
    <!-- 大屏显示16列，小屏显示24列 -->
    <DashboardChart type="line" :data="data" />
  </a-col>
  <a-col :xs="24" :lg="8">
    <!-- 大屏显示8列，小屏显示24列 -->
    <DashboardChart type="pie" :data="data" />
  </a-col>
</a-row>
```

## 主题定制

### 1. 使用预定义主题

```typescript
import { ChartConfig } from '@/utils/chartConfig'

// 深色主题
const darkTheme = ChartConfig.getThemeConfig('dark')

// 浅色主题（默认）
const lightTheme = ChartConfig.getThemeConfig('light')
```

### 2. 自定义颜色

```vue
<DashboardChart
  :colors="['#667eea', '#764ba2', '#f093fb']"
/>
```

### 3. 自定义渐变背景

```vue
<EnhancedStatCard
  icon-bg-color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
/>
```

## 性能优化

### 1. 懒加载

大数据量图表支持懒加载：

```vue
<DashboardChart
  :loading="isLoading"
  :data="chartData"
/>
```

### 2. 数据采样

对于大数据集，建议进行数据采样：

```javascript
// 采样大数据集
const sampledData = largeDataSet.filter((_, index) => index % 10 === 0)
```

### 3. 防抖更新

频繁更新时使用防抖：

```javascript
import { debounce } from 'lodash-es'

const updateChart = debounce((newData) => {
  chartData.value = newData
}, 300)
```

## 最佳实践

### 1. 数据格式统一

确保数据格式符合组件要求：

```javascript
// ✅ 正确格式
const data = [
  { name: '标签', value: 数值 }
]

// ❌ 错误格式
const data = [
  { label: '标签', count: 数值 }
]
```

### 2. 颜色搭配

使用预定义的颜色主题保持一致性：

```javascript
// ✅ 推荐
:colors="ChartConfig.COLORS.primary"

// ❌ 不推荐
:colors="['red', 'blue', 'green']"
```

### 3. 响应式布局

合理使用栅格系统：

```vue
<!-- ✅ 推荐 -->
<a-col :xs="24" :sm="12" :lg="8">

<!-- ❌ 不推荐 -->
<a-col :span="8">
```

### 4. 加载状态

为异步数据提供加载状态：

```vue
<DashboardChart
  :loading="isLoading"
  :data="chartData"
/>
```

## 故障排除

### 1. 图表不显示

- 检查数据格式是否正确
- 确认容器有足够的高度
- 验证 ECharts 依赖是否正确安装

### 2. 动画不流畅

- 减少数据更新频率
- 使用数据采样
- 检查浏览器性能

### 3. 响应式问题

- 确认使用了正确的栅格断点
- 检查容器的 CSS 样式
- 验证图表的 `autoresize` 属性

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基础图表类型
- 集成动画效果
- 响应式布局支持

### v1.1.0
- 新增 EnhancedStatCard 组件
- 优化动画性能
- 增加更多图表类型

### v1.2.0
- 新增 ChartConfig 工具类
- 支持主题定制
- 改进响应式设计

## 技术支持

如有问题或建议，请联系开发团队或提交 Issue。 