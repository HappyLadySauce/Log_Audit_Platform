// 图表配置工具类
export class ChartConfig {
  // 默认颜色主题
  static readonly COLORS = {
    primary: ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2'],
    gradient: [
      'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
      'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
      'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
    ],
    status: {
      success: '#52c41a',
      warning: '#faad14',
      error: '#f5222d',
      info: '#1890ff',
      processing: '#722ed1'
    }
  }

  // 默认动画配置
  static readonly ANIMATION = {
    duration: 1000,
    easing: 'cubicOut',
    delay: 0,
    threshold: 2000
  }

  // 通用样式配置
  static readonly COMMON_STYLE = {
    textStyle: {
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    },
    backgroundColor: 'transparent'
  }

  // 获取线图配置
  static getLineChartConfig(options: {
    data: any[]
    title?: string
    smooth?: boolean
    area?: boolean
    colors?: string[]
    showLegend?: boolean
    showGrid?: boolean
  }) {
    const { data, title, smooth = false, area = false, colors = this.COLORS.primary, showLegend = true, showGrid = true } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      color: colors,
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e8e8e8',
        borderWidth: 1,
        textStyle: {
          color: '#262626'
        },
        axisPointer: {
          type: 'cross',
          crossStyle: {
            color: '#999'
          }
        }
      },
      legend: {
        show: showLegend,
        bottom: 10,
        textStyle: {
          color: '#595959'
        }
      },
      grid: {
        show: showGrid,
        left: '3%',
        right: '4%',
        bottom: showLegend ? '15%' : '3%',
        containLabel: true,
        borderColor: '#f0f0f0'
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.name || item.x),
        axisLine: {
          lineStyle: {
            color: '#d9d9d9'
          }
        },
        axisLabel: {
          color: '#8c8c8c'
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          lineStyle: {
            color: '#d9d9d9'
          }
        },
        axisLabel: {
          color: '#8c8c8c'
        },
        splitLine: {
          lineStyle: {
            color: '#f0f0f0'
          }
        }
      },
      series: [{
        type: 'line',
        data: data.map(item => item.value || item.y),
        smooth,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3
        },
        areaStyle: area ? {
          opacity: 0.3
        } : undefined,
        emphasis: {
          focus: 'series',
          blurScope: 'coordinateSystem'
        }
      }]
    }
  }

  // 获取柱状图配置
  static getBarChartConfig(options: {
    data: any[]
    title?: string
    colors?: string[]
    horizontal?: boolean
  }) {
    const { data, title, colors = this.COLORS.primary, horizontal = false } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      color: colors,
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e8e8e8',
        borderWidth: 1,
        textStyle: {
          color: '#262626'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: horizontal ? 'value' : 'category',
        data: horizontal ? undefined : data.map(item => item.name || item.x),
        axisLine: {
          lineStyle: {
            color: '#d9d9d9'
          }
        },
        axisLabel: {
          color: '#8c8c8c'
        }
      },
      yAxis: {
        type: horizontal ? 'category' : 'value',
        data: horizontal ? data.map(item => item.name || item.x) : undefined,
        axisLine: {
          lineStyle: {
            color: '#d9d9d9'
          }
        },
        axisLabel: {
          color: '#8c8c8c'
        },
        splitLine: {
          lineStyle: {
            color: '#f0f0f0'
          }
        }
      },
      series: [{
        type: 'bar',
        data: data.map(item => item.value || item.y),
        barWidth: '60%',
        itemStyle: {
          borderRadius: horizontal ? [0, 4, 4, 0] : [4, 4, 0, 0]
        },
        emphasis: {
          focus: 'series'
        }
      }]
    }
  }

  // 获取饼图配置
  static getPieChartConfig(options: {
    data: any[]
    title?: string
    colors?: string[]
    radius?: [string, string]
    showLegend?: boolean
    roseType?: boolean
  }) {
    const { 
      data, 
      title, 
      colors = this.COLORS.primary, 
      radius = ['40%', '70%'], 
      showLegend = true,
      roseType = false 
    } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      color: colors,
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e8e8e8',
        borderWidth: 1,
        textStyle: {
          color: '#262626'
        },
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        show: showLegend,
        bottom: 10,
        textStyle: {
          color: '#595959'
        }
      },
      series: [{
        name: title || '数据分布',
        type: 'pie',
        radius,
        roseType: roseType ? 'area' : false,
        center: ['50%', '50%'],
        data: data.map(item => ({
          name: item.name,
          value: item.value
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          show: true,
          formatter: '{b}: {d}%'
        },
        labelLine: {
          show: true
        }
      }]
    }
  }

  // 获取仪表盘配置
  static getGaugeChartConfig(options: {
    value: number
    title?: string
    min?: number
    max?: number
    color?: string
  }) {
    const { value, title, min = 0, max = 100, color = this.COLORS.primary[0] } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      series: [{
        type: 'gauge',
        center: ['50%', '60%'],
        startAngle: 200,
        endAngle: -40,
        min,
        max,
        splitNumber: 10,
        itemStyle: {
          color
        },
        progress: {
          show: true,
          width: 30
        },
        pointer: {
          show: false
        },
        axisLine: {
          lineStyle: {
            width: 30
          }
        },
        axisTick: {
          distance: -45,
          splitNumber: 5,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        splitLine: {
          distance: -52,
          length: 14,
          lineStyle: {
            width: 3,
            color: '#999'
          }
        },
        axisLabel: {
          distance: -20,
          color: '#999',
          fontSize: 20
        },
        anchor: {
          show: false
        },
        title: {
          show: false
        },
        detail: {
          valueAnimation: true,
          width: '60%',
          lineHeight: 40,
          borderRadius: 8,
          offsetCenter: [0, '-15%'],
          fontSize: 60,
          fontWeight: 'bolder',
          formatter: '{value}%',
          color: 'inherit'
        },
        data: [{
          value
        }]
      }]
    }
  }

  // 获取雷达图配置
  static getRadarChartConfig(options: {
    data: any[]
    title?: string
    colors?: string[]
    showLegend?: boolean
  }) {
    const { data, title, colors = this.COLORS.primary, showLegend = true } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      color: colors,
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e8e8e8',
        borderWidth: 1,
        textStyle: {
          color: '#262626'
        }
      },
      legend: {
        show: showLegend,
        bottom: 10,
        textStyle: {
          color: '#595959'
        }
      },
      radar: {
        indicator: data.map(item => ({
          name: item.name,
          max: item.max || 100
        })),
        center: ['50%', '50%'],
        radius: '70%'
      },
      series: [{
        type: 'radar',
        data: [{
          value: data.map(item => item.value),
          name: title || '数据'
        }],
        areaStyle: {
          opacity: 0.3
        }
      }]
    }
  }

  // 获取散点图配置
  static getScatterChartConfig(options: {
    data: any[]
    title?: string
    colors?: string[]
    symbolSize?: number
  }) {
    const { data, title, colors = this.COLORS.primary, symbolSize = 10 } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      color: colors,
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e8e8e8',
        borderWidth: 1,
        textStyle: {
          color: '#262626'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        axisLine: {
          lineStyle: {
            color: '#d9d9d9'
          }
        },
        axisLabel: {
          color: '#8c8c8c'
        },
        splitLine: {
          lineStyle: {
            color: '#f0f0f0'
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLine: {
          lineStyle: {
            color: '#d9d9d9'
          }
        },
        axisLabel: {
          color: '#8c8c8c'
        },
        splitLine: {
          lineStyle: {
            color: '#f0f0f0'
          }
        }
      },
      series: [{
        type: 'scatter',
        data: data.map(item => [item.x, item.y]),
        symbolSize,
        emphasis: {
          focus: 'series'
        }
      }]
    }
  }

  // 获取热力图配置
  static getHeatmapChartConfig(options: {
    data: any[]
    xAxisData: string[]
    yAxisData: string[]
    title?: string
    colors?: string[]
  }) {
    const { data, xAxisData, yAxisData, title, colors = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'] } = options

    return {
      ...this.COMMON_STYLE,
      ...this.getAnimationConfig(),
      title: title ? {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
          color: '#262626'
        }
      } : undefined,
      tooltip: {
        position: 'top',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e8e8e8',
        borderWidth: 1,
        textStyle: {
          color: '#262626'
        }
      },
      grid: {
        height: '50%',
        top: '10%'
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: yAxisData,
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: 0,
        max: 10,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '15%',
        inRange: {
          color: colors
        }
      },
      series: [{
        name: 'Punch Card',
        type: 'heatmap',
        data,
        label: {
          show: true
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    }
  }

  // 获取动画配置
  static getAnimationConfig() {
    return {
      animation: true,
      animationThreshold: this.ANIMATION.threshold,
      animationDuration: this.ANIMATION.duration,
      animationEasing: this.ANIMATION.easing,
      animationDelay: this.ANIMATION.delay,
      animationDurationUpdate: 300,
      animationEasingUpdate: 'cubicOut',
      animationDelayUpdate: 0
    }
  }

  // 获取响应式配置
  static getResponsiveConfig() {
    return {
      media: [
        {
          query: {
            maxWidth: 768
          },
          option: {
            grid: {
              left: '5%',
              right: '5%'
            },
            legend: {
              bottom: 5,
              itemWidth: 15,
              itemHeight: 10,
              textStyle: {
                fontSize: 10
              }
            },
            title: {
              textStyle: {
                fontSize: 14
              }
            }
          }
        }
      ]
    }
  }

  // 获取主题配置
  static getThemeConfig(theme: 'light' | 'dark' = 'light') {
    if (theme === 'dark') {
      return {
        backgroundColor: '#1a1a1a',
        textStyle: {
          color: '#ffffff'
        },
        title: {
          textStyle: {
            color: '#ffffff'
          }
        },
        legend: {
          textStyle: {
            color: '#cccccc'
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          borderColor: '#333333',
          textStyle: {
            color: '#ffffff'
          }
        }
      }
    }
    return {}
  }
}

// 导出常用配置
export const CHART_COLORS = ChartConfig.COLORS
export const CHART_ANIMATION = ChartConfig.ANIMATION
export const CHART_COMMON_STYLE = ChartConfig.COMMON_STYLE 