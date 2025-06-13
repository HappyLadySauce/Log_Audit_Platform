<template>
  <div class="simple-chart" :style="{ height: height, width: width }">
    <v-chart :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent])

interface Props {
  height?: string
  width?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '300px',
  width: '100%'
})

const option = {
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [120, 200, 150, 80, 70, 110, 130],
      type: 'line'
    }
  ]
}
</script>

<style scoped>
.simple-chart {
  border: 1px solid #e8e8e8;
  border-radius: 4px;
}
</style> 