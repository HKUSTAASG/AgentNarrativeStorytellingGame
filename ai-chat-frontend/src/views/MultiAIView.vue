<template>
  <div class="multi-ai-view">
    <div class="multi-ai-container">
      <MultiAIChatBox />
    </div>
  </div>
</template>

<script setup>
import MultiAIChatBox from '@/components/MultiAIChatBox.vue'
</script>

<style scoped>
.multi-ai-view {
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, #1a1a1a 0%, #363636 100%);
  position: relative;
  overflow: hidden;
}

.multi-ai-container {
  width: 100%;
  max-width: 1400px;
  height: 90vh;
  max-height: 900px;
  margin: 0 auto;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>