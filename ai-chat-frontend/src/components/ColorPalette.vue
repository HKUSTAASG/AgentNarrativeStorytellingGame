<template>
  <div class="color-palette">
    <div class="palette-header">
      <h2>颜色推荐</h2>
    </div>
    <div class="palette-content">
      <div class="palette-section">
        <h3>蓝色系</h3>
        <div class="color-grid">
          <div v-for="color in blueColors"
               :key="color"
               class="color-set"
               @click="copyColor(color)">
            <div class="color-preview single"
                 :style="{ backgroundColor: color }">
            </div>
            <div class="color-info">{{ color }}</div>
          </div>
        </div>
      </div>

      <div class="palette-section">
        <h3>绿色系</h3>
        <div class="color-grid">
          <div v-for="color in greenColors"
               :key="color"
               class="color-set"
               @click="copyColor(color)">
            <div class="color-preview single"
                 :style="{ backgroundColor: color }">
            </div>
            <div class="color-info">{{ color }}</div>
          </div>
        </div>
      </div>

      <div class="palette-section">
        <h3>红色系</h3>
        <div class="color-grid">
          <div v-for="color in redColors"
               :key="color"
               class="color-set"
               @click="copyColor(color)">
            <div class="color-preview single"
                 :style="{ backgroundColor: color }">
            </div>
            <div class="color-info">{{ color }}</div>
          </div>
        </div>
      </div>

      <div class="palette-section">
        <h3>黄色系</h3>
        <div class="color-grid">
          <div v-for="color in yellowColors"
               :key="color"
               class="color-set"
               @click="copyColor(color)">
            <div class="color-preview single"
                 :style="{ backgroundColor: color }">
            </div>
            <div class="color-info">{{ color }}</div>
          </div>
        </div>
      </div>

      <div class="palette-section">
        <h3>紫色系</h3>
        <div class="color-grid">
          <div v-for="color in purpleColors"
               :key="color"
               class="color-set"
               @click="copyColor(color)">
            <div class="color-preview single"
                 :style="{ backgroundColor: color }">
            </div>
            <div class="color-info">{{ color }}</div>
          </div>
        </div>
      </div>

      <div class="palette-section">
        <h3>灰色系</h3>
        <div class="color-grid">
          <div v-for="color in grayColors"
               :key="color"
               class="color-set"
               @click="copyColor(color)">
            <div class="color-preview single"
                 :style="{ backgroundColor: color }">
            </div>
            <div class="color-info">{{ color }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const blueColors = [
  '#1890ff', '#40a9ff', '#69c0ff', '#91d5ff', '#bae7ff',
  '#0050b3', '#096dd9', '#1d39c4', '#002766', '#10239e'
]

const greenColors = [
  '#52c41a', '#73d13d', '#95de64', '#b7eb8f', '#d9f7be',
  '#237804', '#389e0d', '#135200', '#389e0d', '#08979c'
]

const redColors = [
  '#f5222d', '#ff4d4f', '#ff7875', '#ffa39e', '#ffccc7',
  '#cf1322', '#a8071a', '#820014', '#5c0011', '#ff7a45'
]

const yellowColors = [
  '#faad14', '#ffc53d', '#ffd666', '#ffe58f', '#fff1b8',
  '#d48806', '#ad6800', '#874d00', '#613400', '#fadb14'
]

const purpleColors = [
  '#722ed1', '#9254de', '#b37feb', '#d3adf7', '#efdbff',
  '#531dab', '#391085', '#22075e', '#120338', '#eb2f96'
]

const grayColors = [
  '#8c8c8c', '#bfbfbf', '#d9d9d9', '#f0f0f0', '#f5f5f5',
  '#595959', '#434343', '#262626', '#1f1f1f', '#141414'
]

const copyColor = (color) => {
  navigator.clipboard.writeText(`"${color}"`).then(() => {
    alert('颜色代码已复制到剪贴板')
  })
}
</script>

<style scoped>
.color-palette {
  width: 300px;
  height: 850px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-right: 20px;
}

.palette-header {
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.palette-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.palette-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.palette-section {
  margin-bottom: 24px;
}

.palette-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #666;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.color-set {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.color-set:hover {
  transform: translateY(-2px);
}

.color-preview {
  height: 40px;
  border-radius: 6px;
  overflow: hidden;
}

.single {
  height: 40px;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1);
}

.color-info {
  margin-top: 4px;
  font-size: 12px;
  color: #666;
  text-align: center;
}

/* 滚动条样式 */
.palette-content::-webkit-scrollbar {
  width: 4px;
}

.palette-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.palette-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.palette-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>