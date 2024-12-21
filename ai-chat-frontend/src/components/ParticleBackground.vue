<template>
  <div class="particle-container">
    <div v-for="n in particleCount"
         :key="n"
         class="particle"
         :style="getRandomStyle()">
    </div>
  </div>
</template>

<script setup>
const particleCount = 500 // 粒子数量

const getRandomStyle = () => {
  const size = Math.random() * 10 + 1
  const left = Math.random() * 100
  const animationDuration = Math.random() * 20 + 10
  const delay = Math.random() * -20

  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDuration: `${animationDuration}s`,
    animationDelay: `${delay}s`
  }
}
</script>

<style scoped>
.particle-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: float linear infinite;
}

@keyframes float {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  20% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
  80% {
    opacity: 0.5;
  }
  100% {
    transform: translateY(-20vh) scale(1);
    opacity: 0;
  }
}
</style>