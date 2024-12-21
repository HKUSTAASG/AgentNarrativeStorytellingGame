<template>
  <div class="meta-view">
    <div class="meta-container" style="width: 100%; max-width: none;">
      <MetaverseWorld />
    </div>
  </div>
</template>

<script setup>
import MetaverseWorld from '@/components/MetaverseWorld.vue'
</script>

<style scoped>
.meta-view {
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, #1a1a1a 0%, #363636 100%);
  position: relative;
  overflow: hidden;
}

.meta-container {
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
}
</style>