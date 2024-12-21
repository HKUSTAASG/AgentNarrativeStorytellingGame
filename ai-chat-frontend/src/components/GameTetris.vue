<template>
  <div class="game-tetris">
    <button class="back-button" @click="$emit('back-to-menu')">返回菜单</button>
    <div class="game-content">
      <!-- 游戏状态显示 -->
      <div class="game-stats">
        <div class="score">分数: {{ score }}</div>
        <div class="level">等级: {{ level }}</div>
        <div class="lines">消除行数: {{ lines }}</div>
        <div class="next-piece">
          <h3>下一个方块</h3>
          <div class="next-piece-grid">
            <div v-for="(row, y) in nextPieceGrid"
                 :key="y"
                 class="row">
              <div v-for="(cell, x) in row"
                   :key="x"
                   class="cell"
                   :style="{ backgroundColor: cell || 'transparent' }">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 游戏主画布 -->
      <canvas ref="gameCanvas"
              :width="canvasWidth"
              :height="canvasHeight"
              v-show="isPlaying">
      </canvas>

      <!-- 开始界面 -->
      <div v-if="!isPlaying && !gameOver" class="game-menu">
        <h2>俄罗斯方块</h2>
        <button @click="startGame">开始游戏</button>
        <div class="controls-info">
          <p>← → : 左右移动</p>
          <p>↑ : 旋转</p>
          <p>↓ : 加速下落</p>
          <p>空格 : 直接落下</p>
          <p>P : 暂停游戏</p>
        </div>
      </div>

      <!-- 游戏结束界面 -->
      <div v-if="gameOver" class="game-over">
        <h2>游戏结束</h2>
        <p>最终得分: {{ score }}</p>
        <button @click="startGame">重新开始</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { defineEmits } from 'vue'

defineEmits(['back-to-menu'])

// 游戏配置
const BLOCK_SIZE = 30
const BOARD_WIDTH = 10
const BOARD_HEIGHT = 20
const canvasWidth = BLOCK_SIZE * BOARD_WIDTH
const canvasHeight = BLOCK_SIZE * BOARD_HEIGHT

// 游戏状态
const gameCanvas = ref(null)
const score = ref(0)
const level = ref(1)
const lines = ref(0)
const isPlaying = ref(false)
const gameOver = ref(false)
const nextPieceGrid = ref([])
let ctx = null
let board = []
let currentPiece = null
let nextPiece = null
let gameLoop = null

// 方块形状定义
const SHAPES = {
  I: [
    [1, 1, 1, 1]
  ],
  O: [
    [1, 1],
    [1, 1]
  ],
  T: [
    [0, 1, 0],
    [1, 1, 1]
  ],
  S: [
    [0, 1, 1],
    [1, 1, 0]
  ],
  Z: [
    [1, 1, 0],
    [0, 1, 1]
  ],
  J: [
    [1, 0, 0],
    [1, 1, 1]
  ],
  L: [
    [0, 0, 1],
    [1, 1, 1]
  ]
}

const COLORS = {
  I: '#00f0f0',
  O: '#f0f000',
  T: '#a000f0',
  S: '#00f000',
  Z: '#f00000',
  J: '#0000f0',
  L: '#f0a000'
}

// 初始化游戏板
const initBoard = () => {
  board = Array(BOARD_HEIGHT).fill().map(() => Array(BOARD_WIDTH).fill(0))
}

// 创建新方块
const createPiece = () => {
  const shapes = Object.keys(SHAPES)
  const shape = shapes[Math.floor(Math.random() * shapes.length)]
  const piece = {
    shape,
    color: COLORS[shape],
    x: Math.floor((BOARD_WIDTH - SHAPES[shape][0].length) / 2),
    y: 0,
    matrix: SHAPES[shape]
  }
  return piece
}

// 绘制方块
const drawBlock = (x, y, color) => {
  ctx.fillStyle = color
  ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
  ctx.strokeStyle = '#fff'
  ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
}

// 绘制游戏板
const draw = () => {
  if (!ctx) return

  // 清空画布
  ctx.fillStyle = '#000'
  ctx.fillRect(0, 0, canvasWidth, canvasHeight)

  // 绘制固定的方块
  for (let y = 0; y < BOARD_HEIGHT; y++) {
    for (let x = 0; x < BOARD_WIDTH; x++) {
      if (board[y][x]) {
        drawBlock(x, y, board[y][x])
      }
    }
  }

  // 绘制当前方块
  if (currentPiece) {
    currentPiece.matrix.forEach((row, y) => {
      row.forEach((value, x) => {
        if (value) {
          drawBlock(currentPiece.x + x, currentPiece.y + y, currentPiece.color)
        }
      })
    })
  }
}

// 更新下一个方块预览
const updateNextPiecePreview = () => {
  if (!nextPiece) return

  const matrix = nextPiece.matrix
  const grid = Array(4).fill().map(() => Array(4).fill(null))

  // 计算居中偏移
  const offsetY = Math.floor((4 - matrix.length) / 2)
  const offsetX = Math.floor((4 - matrix[0].length) / 2)

  // 填充预览网格
  matrix.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value) {
        grid[y + offsetY][x + offsetX] = nextPiece.color
      }
    })
  })

  nextPieceGrid.value = grid
}

// 碰撞检测
const isCollision = (piece, offsetX = 0, offsetY = 0) => {
  return piece.matrix.some((row, y) => {
    return row.some((value, x) => {
      const newX = piece.x + x + offsetX
      const newY = piece.y + y + offsetY
      return (
        value &&
        (newX < 0 ||
          newX >= BOARD_WIDTH ||
          newY >= BOARD_HEIGHT ||
          (newY >= 0 && board[newY][newX]))
      )
    })
  })
}

// 旋转方块
const rotatePiece = () => {
  const matrix = currentPiece.matrix
  const N = matrix.length
  const rotated = Array(N).fill().map(() => Array(N).fill(0))

  for (let y = 0; y < N; y++) {
    for (let x = 0; x < N; x++) {
      rotated[x][N - 1 - y] = matrix[y][x]
    }
  }

  const previousMatrix = currentPiece.matrix
  currentPiece.matrix = rotated

  if (isCollision(currentPiece)) {
    currentPiece.matrix = previousMatrix
  }
}

// 合并方块到游戏板
const merge = () => {
  currentPiece.matrix.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value) {
        board[currentPiece.y + y][currentPiece.x + x] = currentPiece.color
      }
    })
  })
}

// 清除完整的行
const clearLines = () => {
  let linesCleared = 0

  for (let y = BOARD_HEIGHT - 1; y >= 0; y--) {
    if (board[y].every(value => value)) {
      board.splice(y, 1)
      board.unshift(Array(BOARD_WIDTH).fill(0))
      linesCleared++
      y++
    }
  }

  if (linesCleared > 0) {
    lines.value += linesCleared
    score.value += linesCleared * 100 * level.value
    level.value = Math.floor(lines.value / 10) + 1
  }
}

// 移动方块
const movePiece = (direction) => {
  if (!currentPiece) return

  const offset = direction === 'left' ? -1 : 1
  if (!isCollision(currentPiece, offset, 0)) {
    currentPiece.x += offset
  }
}

// 下落方块
const dropPiece = () => {
  if (!currentPiece) return

  if (!isCollision(currentPiece, 0, 1)) {
    currentPiece.y++
  } else {
    merge()
    clearLines()
    currentPiece = nextPiece
    nextPiece = createPiece()
    updateNextPiecePreview()

    if (isCollision(currentPiece)) {
      endGame()
    }
  }
}

// 快速下落
const hardDrop = () => {
  while (!isCollision(currentPiece, 0, 1)) {
    currentPiece.y++
    score.value += 2
  }
  dropPiece()
}

// 处理键盘输入
const handleKeydown = (e) => {
  if (!isPlaying.value) return

  switch (e.key) {
    case 'ArrowLeft':
      movePiece('left')
      break
    case 'ArrowRight':
      movePiece('right')
      break
    case 'ArrowUp':
      rotatePiece()
      break
    case 'ArrowDown':
      dropPiece()
      score.value += 1
      break
    case ' ':
      hardDrop()
      break
    case 'p':
    case 'P':
      togglePause()
      break
  }
}

// 开始游戏
const startGame = () => {
  initBoard()
  score.value = 0
  level.value = 1
  lines.value = 0
  isPlaying.value = true
  gameOver.value = false
  currentPiece = createPiece()
  nextPiece = createPiece()
  updateNextPiecePreview()

  if (gameLoop) clearInterval(gameLoop)
  gameLoop = setInterval(() => {
    dropPiece()
    draw()
  }, 1000 / level.value)
}

// 结束游戏
const endGame = () => {
  isPlaying.value = false
  gameOver.value = true
  if (gameLoop) clearInterval(gameLoop)
}

// 暂停/继续游戏
const togglePause = () => {
  if (gameLoop) {
    clearInterval(gameLoop)
    gameLoop = null
  } else {
    gameLoop = setInterval(() => {
      dropPiece()
      draw()
    }, 1000 / level.value)
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
.game-tetris {
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
  gap: 40px;
  align-items: flex-start;
}

.game-stats {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  min-width: 200px;
}

.score, .level, .lines {
  font-size: 24px;
  margin-bottom: 16px;
}

.next-piece {
  margin-top: 30px;
}

.next-piece h3 {
  margin-bottom: 10px;
  color: #00ff00;
}

.next-piece-grid {
  display: grid;
  grid-template-rows: repeat(4, 30px);
  gap: 1px;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px;
  border-radius: 5px;
}

.row {
  display: grid;
  grid-template-columns: repeat(4, 30px);
  gap: 1px;
}

.cell {
  width: 100%;
  height: 100%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: background-color 0.3s ease;
}

canvas {
  border: 2px solid #333;
  border-radius: 4px;
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
}

.game-menu, .game-over {
  text-align: center;
  padding: 40px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.game-menu h2, .game-over h2 {
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