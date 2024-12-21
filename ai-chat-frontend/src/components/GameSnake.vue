<template>
  <div class="game-snake">
    <button class="back-button" @click="$emit('back-to-menu')">返回菜单</button>
    <div class="game-content">
      <div class="game-header">
        <div class="score">得分: {{ score }}</div>
        <div class="high-score">最高分: {{ highScore }}</div>
      </div>

      <!-- 游戏开始界面 -->
      <div v-if="!isPlaying && !gameOver" class="game-start">
        <h2>贪吃蛇</h2>
        <button @click="startGame">开始游戏</button>
        <div class="controls-info">
          <p>使用方向键或 WASD 控制蛇的移动</p>
          <p>P 键暂停游戏</p>
        </div>
      </div>

      <!-- 游戏结束界面 -->
      <div v-if="gameOver" class="game-over">
        <h2>游戏结束</h2>
        <p>最终得分: {{ score }}</p>
        <button @click="startGame">重新开始</button>
      </div>

      <!-- 游戏画布 -->
      <canvas
        ref="gameCanvas"
        :width="canvasWidth"
        :height="canvasHeight"
        v-show="isPlaying"
      ></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { defineEmits } from 'vue'

defineEmits(['back-to-menu'])

// 游戏配置
const GRID_SIZE = 20
const GAME_SPEED = 100
const canvasWidth = 600
const canvasHeight = 600
const GRID_WIDTH = canvasWidth / GRID_SIZE
const GRID_HEIGHT = canvasHeight / GRID_SIZE

// 游戏状态
const gameCanvas = ref(null)
const score = ref(0)
const highScore = ref(localStorage.getItem('snakeHighScore') || 0)
const isPlaying = ref(false)
const gameOver = ref(false)
let ctx = null

// 蛇的状态
let snake = []
let food = null
let direction = 'right'
let nextDirection = 'right'
let gameLoop = null

// 初始化蛇
const initSnake = () => {
  snake = [
    { x: 5, y: 5 },
    { x: 4, y: 5 },
    { x: 3, y: 5 }
  ]
  direction = 'right'
  nextDirection = 'right'
}

// 生成食物
const generateFood = () => {
  const maxAttempts = 100 // 设置最大尝试次数
  let attempts = 0

  while (attempts < maxAttempts) {
    const x = Math.floor(Math.random() * GRID_WIDTH)
    const y = Math.floor(Math.random() * GRID_HEIGHT)

    // 检查食物是否与蛇身重叠
    const isOnSnake = snake.some(segment => segment.x === x && segment.y === y)

    if (!isOnSnake) {
      food = { x, y }
      return true // 成功生成食物
    }

    attempts++
  }

  return false // 无法生成食物（游戏区域可能已被蛇身填满）
}

// 绘制游戏
const draw = () => {
  if (!ctx) return

  // 清空画布
  ctx.fillStyle = '#1a1a1a'
  ctx.fillRect(0, 0, canvasWidth, canvasHeight)

  // 绘制蛇
  ctx.fillStyle = '#00ff00'
  snake.forEach((segment, index) => {
    if (index === 0) {
      // 蛇头
      ctx.fillStyle = '#00cc00'
    } else {
      // 蛇身
      ctx.fillStyle = '#00ff00'
    }
    ctx.fillRect(
      segment.x * GRID_SIZE,
      segment.y * GRID_SIZE,
      GRID_SIZE - 1,
      GRID_SIZE - 1
    )
  })

  // 绘制食物
  if (food) {
    ctx.fillStyle = '#ff0000'
    ctx.beginPath()
    ctx.arc(
      food.x * GRID_SIZE + GRID_SIZE / 2,
      food.y * GRID_SIZE + GRID_SIZE / 2,
      GRID_SIZE / 2 - 1,
      0,
      Math.PI * 2
    )
    ctx.fill()
  }
}

// 更新游戏状态
const update = () => {
  direction = nextDirection

  // 移动蛇
  const head = { ...snake[0] }
  switch (direction) {
    case 'up': head.y--; break
    case 'down': head.y++; break
    case 'left': head.x--; break
    case 'right': head.x++; break
  }

  // 检查碰撞
  if (
    head.x < 0 || head.x >= GRID_WIDTH ||
    head.y < 0 || head.y >= GRID_HEIGHT ||
    snake.some(segment => segment.x === head.x && segment.y === head.y)
  ) {
    endGame()
    return
  }

  // 添加新头部
  snake.unshift(head)

  // 检查是否吃到食物
  if (food && head.x === food.x && head.y === food.y) {
    score.value += 10
    if (score.value > highScore.value) {
      highScore.value = score.value
      localStorage.setItem('snakeHighScore', highScore.value)
    }

    // 尝试生成新食物
    if (!generateFood()) {
      // 如果无法生成食物，说明游戏胜利
      endGame(true)
      return
    }
  } else {
    // 如果没吃到食物，移除尾部
    snake.pop()
  }
}

// 处理键盘输入
const handleKeydown = (e) => {
  if (!isPlaying.value) return

  const key = e.key.toLowerCase()

  if ((key === 'arrowup' || key === 'w') && direction !== 'down') {
    nextDirection = 'up'
  } else if ((key === 'arrowdown' || key === 's') && direction !== 'up') {
    nextDirection = 'down'
  } else if ((key === 'arrowleft' || key === 'a') && direction !== 'right') {
    nextDirection = 'left'
  } else if ((key === 'arrowright' || key === 'd') && direction !== 'left') {
    nextDirection = 'right'
  } else if (key === 'p') {
    togglePause()
  }
}

// 开始游戏
const startGame = () => {
  isPlaying.value = true
  gameOver.value = false
  score.value = 0
  initSnake()
  generateFood()
  if (gameLoop) clearInterval(gameLoop)
  gameLoop = setInterval(() => {
    update()
    draw()
  }, GAME_SPEED)
}

// 结束游戏
const endGame = (isWin = false) => {
  isPlaying.value = false
  gameOver.value = true
  if (gameLoop) clearInterval(gameLoop)

  // 可以添加胜利提示
  if (isWin) {
    alert('恭喜你赢得了游戏！')
  }
}

// 暂停/继续游戏
const togglePause = () => {
  if (gameLoop) {
    clearInterval(gameLoop)
    gameLoop = null
  } else {
    gameLoop = setInterval(() => {
      update()
      draw()
    }, GAME_SPEED)
  }
}

onMounted(() => {
  ctx = gameCanvas.value.getContext('2d')
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  if (gameLoop) clearInterval(gameLoop)
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.game-snake {
  width: 100%;
  height: 100%;
  position: relative;
  background: #000;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.game-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.game-header {
  display: flex;
  gap: 40px;
  font-size: 24px;
  margin-bottom: 20px;
}

.score, .high-score {
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 20px;
  border-radius: 6px;
}

canvas {
  border: 2px solid #333;
  border-radius: 4px;
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
}

.game-start, .game-over {
  text-align: center;
  padding: 40px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.game-start h2, .game-over h2 {
  font-size: 36px;
  margin-bottom: 20px;
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.game-over p {
  font-size: 24px;
  margin-bottom: 20px;
  color: #fff;
}

button {
  padding: 12px 24px;
  font-size: 18px;
  background: #00ff00;
  color: #000;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background: #00cc00;
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

.controls-info {
  margin-top: 20px;
  color: #ccc;
}

.controls-info p {
  margin: 5px 0;
}
</style>