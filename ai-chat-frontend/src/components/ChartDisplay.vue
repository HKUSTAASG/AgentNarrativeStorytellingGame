<template>
  <div class="chart-container">
    <div class="chart-header">
      <input
        v-model="chartTitle"
        class="chart-title-input"
        placeholder="请输入图表标题..."
        @input="updateChart"
      />
    </div>

    <!-- 图表区域 -->
    <div class="chart-area" ref="chartContainer"></div>

    <!-- 控制面板 -->
    <div class="control-panel">
      <div class="control-row">
        <div class="input-group type-select">
          <label>图表类型</label>
          <select v-model="chartType" @change="updateChart">
            <optgroup label="基础图表">
              <option value="line">折线图</option>
              <option value="bar">柱状图</option>
              <option value="pie">饼图</option>
              <option value="scatter">散点图</option>
              <option value="radar">雷达图</option>
              <option value="funnel">漏斗图</option>
              <option value="gauge">仪表盘</option>
              <option value="heatmap">热力图</option>
              <option value="tree">树图</option>
              <option value="sunburst">旭日图</option>
            </optgroup>
            <optgroup label="3D图表">
              <option value="scatter3D">3D散点图</option>
              <option value="line3D">3D折线图</option>
              <option value="surface">3D曲面</option>
            </optgroup>
          </select>
        </div>

        <div class="input-group style-config">
          <label>样式配置</label>
          <textarea
            v-model="styleConfig"
            placeholder="请输入JSON格式的样式配置..."
            @input="validateStyle"
          ></textarea>
        </div>

        <div class="input-group data-input">
          <label>数据输入</label>
          <textarea
            v-model="dataInput"
            placeholder="请输入JSON格式的数据..."
            @input="validateData"
          ></textarea>
        </div>
      </div>

      <button
        @click="updateChart"
        :disabled="!isValidData"
        :class="{ 'loading': isUpdating }"
      >
        {{ isUpdating ? '更新中...' : '更新图表' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'

const chartContainer = ref(null)
const chartTitle = ref('')
const chartType = ref('line')
const styleConfig = ref('')
const dataInput = ref('')
const isValidData = ref(false)
const isValidStyle = ref(true)
const isUpdating = ref(false)
let chart = null

const chartDefaults = {
  line: {
    style: {
      color: ['#2a7af3'],
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      }
    },
    data: {
      categories: ['1月', '2月', '3月', '4月', '5月', '6'],
      values: [150, 230, 224, 218, 135, 147]
    }
  },
  bar: {
    style: {
      color: ['#00c362'],
      grid: {
        containLabel: true
      }
    },
    data: {
      categories: ['北京', '上海', '广州', '深圳', '杭州'],
      values: [200, 180, 160, 150, 140]
    }
  },
  pie: {
    style: {
      color: ['#2a7af3', '#00c362', '#ffd700', '#ff6b6b', '#4a90e2'],
      legend: {
        orient: 'vertical',
        left: 'left'
      }
    },
    data: {
      categories: ['开发', '设计', '运营', '市场', '销售'],
      values: [335, 310, 234, 135, 158]
    }
  },
  radar: {
    style: {
      color: ['#2a7af3'],
      radar: {
        shape: 'circle',
        splitNumber: 5,
        axisLine: {
          lineStyle: {
            color: 'rgba(238, 197, 102, 0.3)'
          }
        }
      }
    },
    data: {
      categories: ['技术', '设计', '运营', '市场', '销售', '管理'],
      values: [90, 85, 70, 75, 80, 85]
    }
  },
  funnel: {
    style: {
      color: ['#2a7af3', '#00c362', '#ffd700', '#ff6b6b', '#4a90e2'],
      legend: {
        data: ['展现', '点击', '访问', '咨询', '订单']
      }
    },
    data: {
      categories: ['展现', '点击', '访问', '咨询', '订单'],
      values: [100, 80, 60, 40, 20]
    }
  },
  gauge: {
    style: {
      color: ['#2a7af3'],
      series: [{
        detail: {
          formatter: '{value}%'
        }
      }]
    },
    data: {
      categories: ['完成率'],
      values: [75.8]
    }
  },
  heatmap: {
    style: {
      visualMap: {
        min: 0,
        max: 10,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '15%'
      }
    },
    data: {
      categories: ['周一', '周二', '周三', '周四', '周五'],
      values: [7, 8, 4, 9, 6]
    }
  },
  tree: {
    style: {
      series: [{
        initialTreeDepth: 2,
        label: {
          position: 'left',
          verticalAlign: 'middle',
          align: 'right'
        }
      }]
    },
    data: {
      categories: ['技术部', '产品部', '设计部', '运营部'],
      values: [80, 70, 60, 50]
    }
  },
  sunburst: {
    style: {
      series: [{
        radius: ['20%', '90%'],
        label: {
          rotate: 'radial'
        }
      }]
    },
    data: {
      categories: ['Q1', 'Q2', 'Q3', 'Q4'],
      values: [100, 80, 60, 40]
    }
  },
  scatter: {
    style: {
      xAxis: {
        type: 'value',
        scale: true
      },
      yAxis: {
        type: 'value',
        scale: true
      },
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'cross'
        }
      },
      grid: {
        top: '10%',
        right: '10%',
        bottom: '10%',
        left: '10%'
      }
    },
    data: {
      values: [
        [10.0, 8.04],
        [8.07, 6.95],
        [13.0, 7.58],
        [9.05, 8.81],
        [11.0, 8.33],
        [14.0, 7.66],
        [13.4, 6.81],
        [10.0, 6.33],
        [14.0, 8.96],
        [12.5, 6.82],
        [9.15, 7.2],
        [11.5, 7.2],
        [3.03, 4.23],
        [12.2, 7.83],
        [2.02, 4.47],
        [1.05, 3.33],
        [4.05, 4.96],
        [6.03, 7.24],
        [12.0, 6.26],
        [12.0, 8.84],
        [7.08, 5.82],
        [5.02, 5.68]
      ]
    }
  },
  scatter3D: {
    style: {
      tooltip: {},
      visualMap: [
        {
          top: 10,
          calculable: true,
          dimension: 3,
          max: 100,
          inRange: {
            color: [
              '#1710c0',
              '#0b9df0',
              '#00fea8',
              '#00ff0d',
              '#f5f811',
              '#f09a09',
              '#fe0300'
            ]
          },
          textStyle: {
            color: '#fff'
          }
        },
        {
          bottom: 10,
          calculable: true,
          dimension: 4,
          max: 50,
          inRange: {
            symbolSize: [10, 40]
          },
          textStyle: {
            color: '#fff'
          }
        }
      ],
      grid3D: {
        axisLine: {
          lineStyle: {
            color: '#fff'
          }
        },
        axisPointer: {
          lineStyle: {
            color: '#ffbd67'
          }
        },
        viewControl: {
          autoRotate: true,
          projection: 'orthographic'
        }
      }
    },
    data: {
      schema: [
        { name: 'protein', index: 0 },
        { name: 'fiber', index: 1 },
        { name: 'sodium', index: 2 },
        { name: 'color', index: 3 },
        { name: 'size', index: 4 }
      ],
      values: [
        [90, 60, 75, 85, 30], // [protein, fiber, sodium, color, size]
        [75, 85, 45, 65, 35],
        [80, 70, 60, 75, 25],
        [65, 55, 85, 95, 40],
        [95, 75, 50, 55, 20],
        [70, 90, 65, 45, 35],
        [85, 65, 80, 70, 45],
        [60, 80, 70, 80, 30],
        [55, 95, 55, 60, 25],
        [50, 85, 90, 50, 40],
        // ... 可以添加更多数据点
        [88, 77, 66, 55, 44],
        [99, 88, 77, 66, 55],
        [77, 66, 55, 44, 33],
        [66, 55, 44, 33, 22],
        [55, 44, 33, 22, 11]
      ]
    }
  },
  line3D: {
    style: {
      grid3D: {
        boxWidth: 100,
        boxHeight: 100,
        boxDepth: 100,
        axisLine: {
          lineStyle: {
            color: '#fff'
          }
        },
        axisPointer: {
          lineStyle: {
            color: '#ffbd67'
          }
        },
        viewControl: {
          autoRotate: true
        }
      }
    },
    data: {
      categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      values: [
        [0, 0, 5],
        [1, 0, 8],
        [2, 0, 12],
        [3, 0, 9],
        [4, 0, 15],
        [5, 0, 10],
        [6, 0, 7]
      ]
    }
  },
  surface: {
    style: {},
    data: {
      tooltip: {},
      backgroundColor: '#fff',
      visualMap: {
        show: false,
        dimension: 2,
        min: -1,
        max: 1,
        inRange: {
          color: [
            '#313695',
            '#4575b4',
            '#74add1',
            '#abd9e9',
            '#e0f3f8',
            '#ffffbf',
            '#fee090',
            '#fdae61',
            '#f46d43',
            '#d73027',
            '#a50026'
          ]
        }
      },
      xAxis3D: {
        type: 'value'
      },
      yAxis3D: {
        type: 'value'
      },
      zAxis3D: {
        type: 'value'
      },
      grid3D: {
        viewControl: {
          autoRotate: true
        }
      },
      series: [
        {
          type: 'surface',
          wireframe: {
            show: false
          },
          equation: {
            x: {
              step: 0.05
            },
            y: {
              step: 0.05
            },
            z: function (x, y) {
              if (Math.abs(x) < 0.1 && Math.abs(y) < 0.1) {
                return '-'
              }
              return Math.sin(x * Math.PI) * Math.sin(y * Math.PI)
            }
          }
        }
      ]
    }
  }
}

const validateData = () => {
  try {
    const data = JSON.parse(dataInput.value)
    switch (chartType.value) {
      case 'scatter':
        isValidData.value = data && Array.isArray(data.values) &&
          data.values.every(item => Array.isArray(item) && item.length === 2)
        break
      case 'scatter3D':
        isValidData.value = Array.isArray(data.values)
        break
      case 'surface':
        isValidData.value = data &&
          data.series &&
          Array.isArray(data.series) &&
          data.series.length > 0 &&
          data.series[0].type === 'surface' &&
          data.series[0].equation
        break
      default:
        isValidData.value = data && data.categories && data.values &&
          Array.isArray(data.categories) && Array.isArray(data.values) &&
          data.categories.length === data.values.length
    }
  } catch {
    isValidData.value = false
  }
}

const validateStyle = () => {
  try {
    if (styleConfig.value) {
      JSON.parse(styleConfig.value)
      isValidStyle.value = true
    }
  } catch {
    isValidStyle.value = false
  }
}

const generateChartOption = (data) => {
  const parsedData = JSON.parse(data)
  const customStyle = styleConfig.value ? JSON.parse(styleConfig.value) : {}
  let heatmapData = []
  let parsedData3D = null

  if (chartType.value === 'scatter3D') {
    parsedData3D = JSON.parse(data)
  }

  const baseOption = {
    title: {
      text: chartTitle.value || '未命名图表',
      left: 20,
      top: 20,
      textAlign: 'left',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis'
    },
    animation: true,
    ...customStyle
  }

  switch (chartType.value) {
    case 'line':
      return {
        ...baseOption,
        xAxis: {
          type: 'category',
          data: parsedData.categories
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: parsedData.values,
          type: 'line',
          smooth: true,
          areaStyle: {},
          markPoint: {
            data: [
              { type: 'max', name: '最大值' },
              { type: 'min', name: '最小值' }
            ]
          }
        }]
      }

    case 'bar':
      return {
        ...baseOption,
        xAxis: {
          type: 'category',
          data: parsedData.categories
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: parsedData.values,
          type: 'bar',
          showBackground: true,
          backgroundStyle: {
            color: 'rgba(180, 180, 180, 0.2)'
          }
        }]
      }

    case 'pie':
      return {
        ...baseOption,
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: true,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {c} ({d}%)'
          },
          data: parsedData.categories.map((cat, index) => ({
            name: cat,
            value: parsedData.values[index]
          }))
        }]
      }

    case 'radar':
      return {
        ...baseOption,
        radar: {
          indicator: parsedData.categories.map(cat => ({
            name: cat,
            max: Math.max(...parsedData.values) * 1.2
          }))
        },
        series: [{
          type: 'radar',
          data: [{
            value: parsedData.values,
            name: '数据分析',
            areaStyle: {
              color: 'rgba(42, 122, 243, 0.3)'
            }
          }]
        }]
      }

    case 'funnel':
      return {
        ...baseOption,
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}'
        },
        series: [{
          type: 'funnel',
          left: '10%',
          top: 60,
          bottom: 60,
          width: '80%',
          min: 0,
          max: Math.max(...parsedData.values),
          minSize: '0%',
          maxSize: '100%',
          sort: 'descending',
          gap: 2,
          label: {
            show: true,
            position: 'inside'
          },
          labelLine: {
            length: 10,
            lineStyle: {
              width: 1,
              type: 'solid'
            }
          },
          itemStyle: {
            borderColor: '#fff',
            borderWidth: 1
          },
          emphasis: {
            label: {
              fontSize: 20
            }
          },
          data: parsedData.categories.map((cat, index) => ({
            name: cat,
            value: parsedData.values[index]
          }))
        }]
      }

    case 'gauge':
      return {
        ...baseOption,
        series: [{
          type: 'gauge',
          progress: {
            show: true,
            width: 18
          },
          axisLine: {
            lineStyle: {
              width: 18
            }
          },
          axisTick: {
            show: false
          },
          splitLine: {
            length: 15,
            lineStyle: {
              width: 2,
              color: '#999'
            }
          },
          pointer: {
            icon: 'path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.23010 2092.40383,617.34993 L2092.40383,617.34993 C2092.40383,618.46975 2091.48372,619.38987 2090.36389,619.38987 L2090.36389,619.38987 C2089.24407,619.38987 2088.32395,618.46975 2088.32395,617.34993 L2088.32395,617.34993 C2088.32395,616.23010 2089.24407,615.30999 2090.36389,615.30999 Z',
            length: '75%',
            width: 16,
            offsetCenter: [0, '5%']
          },
          detail: {
            valueAnimation: true,
            formatter: '{value}',
            color: 'inherit'
          },
          data: [{
            value: parsedData.values[0],
            name: parsedData.categories[0]
          }]
        }]
      }

    case 'heatmap':
      heatmapData = []
      for (let i = 0; i < parsedData.categories.length; i++) {
        for (let j = 0; j < parsedData.categories.length; j++) {
          const value = parsedData.values[i] || Math.random() * 100
          heatmapData.push([i, j, value])
        }
      }

      return {
        ...baseOption,
        tooltip: {
          position: 'top'
        },
        grid: {
          top: '15%'
        },
        xAxis: {
          type: 'category',
          data: parsedData.categories,
          splitArea: {
            show: true
          }
        },
        yAxis: {
          type: 'category',
          data: parsedData.categories,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 100,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%'
        },
        series: [{
          type: 'heatmap',
          data: heatmapData,
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

    case 'tree':
      return {
        ...baseOption,
        tooltip: {
          trigger: 'item',
          triggerOn: 'mousemove'
        },
        series: [{
          type: 'tree',
          data: [{
            name: 'root',
            children: parsedData.categories.map((cat, index) => ({
              name: cat,
              value: parsedData.values[index],
              children: [{
                name: `Value: ${parsedData.values[index]}`
              }]
            }))
          }],
          top: '10%',
          bottom: '10%',
          layout: 'radial',
          symbol: 'emptyCircle',
          symbolSize: 7,
          initialTreeDepth: 3,
          animationDurationUpdate: 750,
          emphasis: {
            focus: 'descendant'
          }
        }]
      }

    case 'sunburst':
      return {
        ...baseOption,
        series: [{
          type: 'sunburst',
          data: [{
            name: 'Total',
            children: parsedData.categories.map((cat, index) => ({
              name: cat,
              value: parsedData.values[index]
            }))
          }],
          radius: ['20%', '90%'],
          emphasis: {
            focus: 'ancestor'
          }
        }]
      }

    case 'scatter3D':
      return {
        ...baseOption,
        tooltip: {},
        visualMap: [
          {
            top: 10,
            calculable: true,
            dimension: 3,
            max: Math.max(...parsedData3D.values.map(item => item[3])),
            inRange: {
              color: [
                '#1710c0',
                '#0b9df0',
                '#00fea8',
                '#00ff0d',
                '#f5f811',
                '#f09a09',
                '#fe0300'
              ]
            },
            textStyle: {
              color: '#fff'
            }
          },
          {
            bottom: 10,
            calculable: true,
            dimension: 4,
            max: Math.max(...parsedData3D.values.map(item => item[4])),
            inRange: {
              symbolSize: [10, 40]
            },
            textStyle: {
              color: '#fff'
            }
          }
        ],
        xAxis3D: {
          name: parsedData3D.schema[0].name,
          type: 'value'
        },
        yAxis3D: {
          name: parsedData3D.schema[1].name,
          type: 'value'
        },
        zAxis3D: {
          name: parsedData3D.schema[2].name,
          type: 'value'
        },
        grid3D: {
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          axisPointer: {
            lineStyle: {
              color: '#ffbd67'
            }
          },
          viewControl: {
            autoRotate: true,
            projection: 'orthographic'
          }
        },
        series: [{
          type: 'scatter3D',
          dimensions: parsedData3D.schema.map(item => item.name),
          data: parsedData3D.values,
          symbolSize: 12,
          itemStyle: {
            borderWidth: 1,
            borderColor: 'rgba(255,255,255,0.8)'
          },
          emphasis: {
            itemStyle: {
              color: '#fff'
            }
          }
        }]
      }

    case 'scatter':
      return {
        ...baseOption,
        xAxis: {
          type: 'value',
          scale: true,
          axisLabel: {
            formatter: '{value}'
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        yAxis: {
          type: 'value',
          scale: true,
          axisLabel: {
            formatter: '{value}'
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'cross'
          },
          formatter: function(params) {
            return `(${params.data[0]}, ${params.data[1]})`
          }
        },
        grid: {
          top: '10%',
          right: '10%',
          bottom: '10%',
          left: '10%'
        },
        series: [{
          type: 'scatter',
          symbolSize: 20,
          data: parsedData.values,
          itemStyle: {
            color: '#5470c6',
            opacity: 0.8,
            borderColor: '#fff',
            borderWidth: 1
          },
          emphasis: {
            itemStyle: {
              opacity: 1,
              shadowBlur: 10,
              shadowColor: 'rgba(84, 112, 198, 0.5)'
            }
          },
          markLine: {
            lineStyle: {
              type: 'solid'
            },
            data: [
              {
                type: 'average',
                name: 'Y 平均值'
              },
              {
                xAxis: 'average',
                name: 'X 平均值'
              }
            ]
          }
        }]
      }

    case 'line3D':
      return {
        ...baseOption,
        tooltip: {},
        grid3D: {
          boxWidth: 100,
          boxHeight: 100,
          boxDepth: 100,
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          axisPointer: {
            lineStyle: {
              color: '#ffbd67'
            }
          },
          viewControl: {
            autoRotate: true
          }
        },
        xAxis3D: {
          type: 'category',
          data: parsedData.categories,
          name: 'X'
        },
        yAxis3D: {
          type: 'value',
          name: 'Y'
        },
        zAxis3D: {
          type: 'value',
          name: 'Z'
        },
        series: [{
          type: 'line3D',
          data: parsedData.values,
          lineStyle: {
            width: 4,
            color: '#2a7af3'
          }
        }]
      }

    case 'surface':
      return {
        tooltip: {},
        backgroundColor: '#fff',
        visualMap: {
          show: false,
          dimension: 2,
          min: -1,
          max: 1,
          inRange: {
            color: [
              '#313695',
              '#4575b4',
              '#74add1',
              '#abd9e9',
              '#e0f3f8',
              '#ffffbf',
              '#fee090',
              '#fdae61',
              '#f46d43',
              '#d73027',
              '#a50026'
            ]
          }
        },
        xAxis3D: {
          type: 'value'
        },
        yAxis3D: {
          type: 'value'
        },
        zAxis3D: {
          type: 'value'
        },
        grid3D: {
          viewControl: {
            autoRotate: true
          }
        },
        series: [
          {
            type: 'surface',
            wireframe: {
              show: false
            },
            equation: {
              x: {
                step: 0.05
              },
              y: {
                step: 0.05
              },
              z: function (x, y) {
                if (Math.abs(x) < 0.1 && Math.abs(y) < 0.1) {
                  return '-'
                }
                return Math.sin(x * Math.PI) * Math.sin(y * Math.PI)
              }
            }
          }
        ]
      }

    default:
      return baseOption
  }
}

const updateChart = async () => {
  if (!isValidData.value || !chart) return

  isUpdating.value = true
  try {
    const option = generateChartOption(dataInput.value)
    await chart.setOption(option, true)
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error) {
    console.error('更新图表错误:', error)
  } finally {
    isUpdating.value = false
  }
}

onMounted(() => {
  nextTick(() => {
    if (chartContainer.value) {
      chart = echarts.init(chartContainer.value, null, {
        renderer: 'canvas',
        useDirtyRect: false
      })

      const defaultConfig = chartDefaults[chartType.value]
      if (defaultConfig) {
        styleConfig.value = JSON.stringify(defaultConfig.style, null, 2)
        dataInput.value = JSON.stringify(defaultConfig.data, null, 2)
      }

      validateData()
      updateChart()

      const handleResize = () => {
        if (chart) {
          chart.resize()
        }
      }

      window.addEventListener('resize', handleResize)

      const resizeObserver = new ResizeObserver(() => {
        handleResize()
      })

      resizeObserver.observe(chartContainer.value)

      onUnmounted(() => {
        window.removeEventListener('resize', handleResize)
        resizeObserver.disconnect()
        if (chart) {
          chart.dispose()
        }
      })
    }
  })
})

watch(chartType, (newType) => {
  const defaultConfig = chartDefaults[newType]
  if (defaultConfig) {
    styleConfig.value = JSON.stringify(defaultConfig.style, null, 2)
    dataInput.value = JSON.stringify(defaultConfig.data, null, 2)
    validateData()
    updateChart()
  }
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: none;
}

.chart-area {
  flex: 1;
  min-height: 400px;
  padding: 20px;
  position: relative;
}

.control-panel {
  padding: 20px;
  background: rgba(248, 249, 250, 0.9);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 0 0 12px 12px;
}

.control-row {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.input-group {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

label {
  font-size: 16px;
  color: #666;
  white-space: nowrap;
  min-width: 80px;
}

select {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  background: white;
  transition: all 0.3s ease;
}

select:focus {
  outline: none;
  border-color: #2a7af3;
  box-shadow: 0 0 0 2px rgba(42, 122, 243, 0.2);
}

textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  background: white;
  resize: none;
  font-family: monospace;
  height: 100px;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #2a7af3;
  box-shadow: 0 0 0 2px rgba(42, 122, 243, 0.2);
}

button {
  width: 100%;
  padding: 14px;
  background: #2a7af3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

button:hover:not(:disabled) {
  background: #1a6ae3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(42, 122, 243, 0.2);
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

button.loading {
  position: relative;
  padding-right: 40px;
}

button.loading::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  width: 16px;
  height: 16px;
  margin-top: -8px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 滚动条样式 */
textarea::-webkit-scrollbar {
  width: 4px;
}

textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
}

textarea::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 添加玻璃态效果 */
.control-panel {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* 添加输入框悬浮效果 */
select:hover,
textarea:hover {
  border-color: #2a7af3;
}

/* 添加阴影效果 */
.chart-container {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.template-row,
.template-buttons,
.template-btn {
  display: none;
}
</style>