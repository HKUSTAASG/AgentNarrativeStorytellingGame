<template>
  <div class="chart-view">
    <div class="chart-container">
      <div class="chart-layout">
        <ColorPalette />
        <div class="chart-wrapper">
          <ChartDisplay />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ChartDisplay from '@/components/ChartDisplay.vue'
import ColorPalette from '@/components/ColorPalette.vue'
</script>

<style scoped>
.chart-view {
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
}

.chart-container {
  width: 100%;
  max-width: 1400px;
  height: 90vh;
  max-height: 900px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
  position: relative;
}

.chart-layout {
  width: 100%;
  height: 100%;
  display: flex;
  gap: 20px;
}

.chart-wrapper {
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 响应式设计 */
@media (max-width: 1440px) {
  .chart-container {
    max-width: 95%;
  }
}

@media (max-height: 900px) {
  .chart-container {
    height: 95vh;
  }
}

/* 添加动画效果 */
.chart-wrapper {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 添加玻璃态效果 */
.chart-wrapper {
  position: relative;
}

.chart-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.05)
  );
  border-radius: 16px;
  z-index: -1;
}
</style>