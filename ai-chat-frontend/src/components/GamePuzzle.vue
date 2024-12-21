<template>
  <div class="game-puzzle">
    <button class="back-button" @click="$emit('back-to-menu')">返回菜单</button>

    <!-- 游戏状态显示 -->
    <div class="game-header">
      <div class="moves">移动次数: {{ moves }}</div>
      <div class="time">用时: {{ formatTime(time) }}</div>
      <div class="difficulty">难度: {{ difficultyText }}</div>
    </div>

    <!-- 游戏区域 -->
    <div class="game-content">
      <!-- 开始界面 -->
      <div v-if="!isPlaying && !gameOver" class="game-start">
        <h2>拼图游戏</h2>
        <div class="game-settings">
          <div class="settings-row">
            <div class="settings-group">
              <label>选择难度：</label>
              <select v-model="gridSize">
                <option value="3">简单 (3 x 3)</option>
                <option value="4">中等 (4 x 4)</option>
                <option value="5">困难 (5 x 5)</option>
                <option value="6">专家 (6 x 6)</option>
                <option value="8">大师 (8 x 8)</option>
              </select>
            </div>
          </div>
          <div class="settings-row">
            <div class="settings-group">
              <label>游戏模式：</label>
              <select v-model="gameMode">
                <option value="normal">普通模式</option>
                <option value="timed">计时模式</option>
                <option value="limited">限步模式</option>
                <option value="rotation">旋转模式</option>
              </select>
            </div>
          </div>
        </div>
        <div class="image-select">
          <label>选择图片：</label>
          <div class="image-options">
            <div class="default-images">
              <div class="image-option upload"
                   :class="{ selected: selectedImage && isCustomImage }">
                <input
                  type="file"
                  @change="handleImageUpload"
                  accept="image/*"
                  ref="fileInput"
                  style="display: none"
                >
                <div class="image-wrapper" @click="$refs.fileInput.click()">
                  <img v-if="uploadedImage"
                       :src="uploadedImage"
                       alt="上传的图片"
                       class="preview-image">
                  <div v-else class="upload-placeholder">
                    <i class="fas fa-upload"></i>
                    <span>上传图片</span>
                  </div>
                  <div class="selection-indicator" v-if="selectedImage && isCustomImage">
                    <i class="fas fa-check"></i>
                  </div>
                </div>
                <div class="image-label">自定义图片</div>
              </div>
              <div v-for="(img, index) in defaultImages"
                   :key="index"
                   class="image-option"
                   :class="{ selected: selectedImage === img && !isCustomImage }"
                   @click="selectImage(img)">
                <div class="image-wrapper">
                  <img :src="img" :alt="`图片 ${index + 1}`">
                  <div class="selection-indicator" v-if="selectedImage === img && !isCustomImage">
                    <i class="fas fa-check"></i>
                  </div>
                </div>
                <div class="image-label">图片 {{ index + 1 }}</div>
              </div>
            </div>
          </div>
        </div>
        <button @click="startGame" :disabled="!selectedImage">开始游戏</button>
      </div>

      <!-- 游戏主界面 -->
      <div v-else-if="isPlaying" class="puzzle-board"
           :style="{ width: boardSize + 'px', height: boardSize + 'px' }">
        <div v-for="(piece, index) in pieces"
             :key="index"
             class="puzzle-piece"
             :class="{
               'correct-position': piece.isCorrect,
               'rotatable': gameMode === 'rotation',
               'rotating': piece.isRotating
             }"
             :style="getPieceStyle(piece)"
             @mousedown="startDrag($event, piece)"
             @touchstart="startDrag($event, piece)"
             @contextmenu.prevent="rotatePiece(piece)">
          <div v-if="showNumbers" class="piece-number">{{ index + 1 }}</div>
          <div v-if="gameMode === 'rotation'" class="rotation-indicator"
               :style="{ transform: `rotate(${piece.rotation}deg)` }">
            ↑
          </div>
        </div>
      </div>

      <!-- 游戏结束界面 -->
      <div v-if="gameOver" class="game-over">
        <h2>{{ isWin ? '恭喜完成！' : '游戏结束' }}</h2>
        <p>移动次数：{{ moves }}</p>
        <p>用时：{{ formatTime(time) }}</p>
        <p v-if="gameMode === 'limited'">剩余步数：{{ remainingMoves }}</p>
        <div class="final-score">得分：{{ calculateScore() }}</div>
        <button @click="restartGame">再玩一次</button>
        <button @click="changeSettings">更改设置</button>
      </div>

      <!-- 游戏控制按钮 -->
      <div v-if="isPlaying" class="game-controls">
        <button @click="toggleHint">{{ showHint ? '隐藏提示' : '显示提示' }}</button>
        <button @click="toggleNumbers">{{ showNumbers ? '隐藏序号' : '显示序号' }}</button>
        <button @click="shufflePieces">重新打乱</button>
        <button @click="togglePause">{{ isPaused ? '继续' : '暂停' }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, computed } from 'vue'
import { defineEmits } from 'vue'

defineEmits(['back-to-menu'])

// 游戏状态
const isPlaying = ref(false)
const gameOver = ref(false)
const moves = ref(0)
const time = ref(0)
let timer = null

// 游戏配置
const gridSize = ref(3)
const boardSize = 600
const pieces = ref([])
const selectedImage = ref(null)
const defaultImages = [
  '/puzzle/image1.png',
  '/puzzle/image2.png',
]

// 拖拽状态
let draggedPiece = null
let startX = 0
let startY = 0

// 添加新的游戏状态
const gameMode = ref('normal')
const showHint = ref(false)
const showNumbers = ref(false)
const isPaused = ref(false)
const isWin = ref(false)
const remainingMoves = ref(100)
const difficultyText = computed(() => {
  const size = parseInt(gridSize.value)
  switch (size) {
    case 3: return '简单'
    case 4: return '中等'
    case 5: return '困难'
    case 6: return '专家'
    case 8: return '大师'
    default: return '未知'
  }
})

// 添加一个标记来区分是否是自定义上传的图片
const isCustomImage = ref(false)

// 添加上传图片的状态
const uploadedImage = ref(null)

// 修改图片选择函数
const selectImage = (img) => {
  selectedImage.value = img
  isCustomImage.value = false
}

// 修改图片上传处理函数
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImage.value = e.target.result // 保存上传的图片
      selectedImage.value = e.target.result
      isCustomImage.value = true
    }
    reader.readAsDataURL(file)
  }
}

// 初始化拼图
const initializePuzzles = () => {
  const size = parseInt(gridSize.value)
  const pieceSize = boardSize / size
  pieces.value = []

  for (let i = 0; i < size * size; i++) {
    const row = Math.floor(i / size)
    const col = i % size
    pieces.value.push({
      id: i,
      currentPos: i,
      targetPos: i,
      row,
      col,
      x: col * pieceSize,
      y: row * pieceSize,
      width: pieceSize,
      height: pieceSize,
      backgroundImage: selectedImage.value,
      backgroundPosition: `-${col * pieceSize}px -${row * pieceSize}px`,
      backgroundSize: `${boardSize}px ${boardSize}px`,
      isCorrect: false
    })
  }
}

// 打乱拼图
const shufflePieces = () => {
  const size = parseInt(gridSize.value)
  const totalPieces = size * size

  for (let i = totalPieces - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const temp = pieces.value[i].currentPos
    pieces.value[i].currentPos = pieces.value[j].currentPos
    pieces.value[j].currentPos = temp

    // 更新位置
    updatePiecePosition(pieces.value[i])
    updatePiecePosition(pieces.value[j])
  }
}

// 更新拼图位置
const updatePiecePosition = (piece) => {
  const size = parseInt(gridSize.value)
  const pieceSize = boardSize / size
  const currentRow = Math.floor(piece.currentPos / size)
  const currentCol = piece.currentPos % size
  piece.x = currentCol * pieceSize
  piece.y = currentRow * pieceSize
}

// 获取拼图样式
const getPieceStyle = (piece) => {
  const style = {
    width: piece.width + 'px',
    height: piece.height + 'px',
    backgroundImage: `url(${piece.backgroundImage})`,
    backgroundPosition: piece.backgroundPosition,
    backgroundSize: piece.backgroundSize,
    transform: `translate(${piece.x}px, ${piece.y}px)`,
    transition: draggedPiece?.id === piece.id ? 'none' : 'transform 0.3s'
  }

  if (gameMode.value === 'rotation') {
    style.transform += ` rotate(${piece.rotation || 0}deg)`
  }

  if (showHint.value) {
    style.opacity = piece.isCorrect ? '1' : '0.7'
  }

  return style
}

// 开始拖拽
const startDrag = (event, piece) => {
  if (!isPlaying.value || isPaused.value) return

  event.preventDefault()
  draggedPiece = piece
  const touch = event.touches ? event.touches[0] : event
  startX = touch.clientX - piece.x
  startY = touch.clientY - piece.y

  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('touchmove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchend', stopDrag)
}

// 处理拖拽
const handleDrag = (event) => {
  if (!draggedPiece) return

  event.preventDefault()
  const touch = event.touches ? event.touches[0] : event
  const x = touch.clientX - startX
  const y = touch.clientY - startY

  draggedPiece.x = x
  draggedPiece.y = y
}

// 停止拖拽
const stopDrag = () => {
  if (!draggedPiece) return

  const size = parseInt(gridSize.value)
  const pieceSize = boardSize / size
  const col = Math.round(draggedPiece.x / pieceSize)
  const row = Math.round(draggedPiece.y / pieceSize)

  // 确保在边界内
  if (col >= 0 && col < size && row >= 0 && row < size) {
    const newPos = row * size + col
    const targetPiece = pieces.value.find(p => p.currentPos === newPos)

    if (targetPiece) {
      // 交换位置
      const tempPos = draggedPiece.currentPos
      draggedPiece.currentPos = targetPiece.currentPos
      targetPiece.currentPos = tempPos

      updatePiecePosition(draggedPiece)
      updatePiecePosition(targetPiece)

      moves.value++
      checkWin()
    } else {
      // 返回原位
      updatePiecePosition(draggedPiece)
    }
  } else {
    // 返回原位
    updatePiecePosition(draggedPiece)
  }

  draggedPiece = null
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchend', stopDrag)
}

// 检查是否胜利
const checkWin = () => {
  const isCorrectPosition = pieces.value.every(piece => piece.currentPos === piece.targetPos)
  const isCorrectRotation = gameMode.value !== 'rotation' ||
    pieces.value.every(piece => !piece.rotation || piece.rotation === 0)

  if (isCorrectPosition && isCorrectRotation) {
    isWin.value = true
    gameOver.value = true
    isPlaying.value = false
    clearInterval(timer)
  }
}

// 格式化时间
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 添加计时器相关的函数
const startTimer = () => {
  // 清除可能存在的旧计时器
  if (timer) {
    clearInterval(timer)
  }
  // 设置倒计时时间（例如：3分钟）
  time.value = 180

  // 创建新的计时器
  timer = setInterval(() => {
    if (time.value > 0) {
      time.value--
    } else {
      // 时间到，结束游戏
      endGame(false)
    }
  }, 1000)
}

// 修改开始游戏函数
const startGame = () => {
  if (!selectedImage.value) return

  isPlaying.value = true
  gameOver.value = false
  isWin.value = false
  moves.value = 0
  time.value = 0

  // 根据游戏模式设置初始值
  switch (gameMode.value) {
    case 'limited':
      remainingMoves.value = parseInt(gridSize.value) * 50
      break
    case 'timed':
      startTimer() // 现在可以正确调用 startTimer 函数
      break
  }

  initializePuzzles()
  shufflePieces()

  if (!timer) {
    timer = setInterval(() => {
      if (!isPaused.value) {
        time.value++
      }
    }, 1000)
  }
}

// 重新开始
const restartGame = () => {
  gameOver.value = false
  startGame()
}

// 组件卸载时清理
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})

// 添加新的游戏功能
const rotatePiece = (piece) => {
  if (gameMode.value !== 'rotation' || !isPlaying.value) return

  piece.isRotating = true
  piece.rotation = (piece.rotation || 0) + 90
  if (piece.rotation >= 360) {
    piece.rotation = 0
  }

  setTimeout(() => {
    piece.isRotating = false
  }, 300)

  moves.value++
  checkWin()
}

const toggleHint = () => {
  showHint.value = !showHint.value
}

const toggleNumbers = () => {
  showNumbers.value = !showNumbers.value
}

const togglePause = () => {
  isPaused.value = !isPaused.value
}

const changeSettings = () => {
  gameOver.value = false
  isPlaying.value = false
}

// 添加计分系统
const calculateScore = () => {
  const baseScore = 1000
  const timeDeduction = Math.floor(time.value / 10)
  const movesDeduction = Math.floor(moves.value / 2)
  const difficultyMultiplier = parseInt(gridSize.value) - 2

  let score = (baseScore - timeDeduction - movesDeduction) * difficultyMultiplier

  if (gameMode.value === 'timed') {
    score *= 1.5
  } else if (gameMode.value === 'rotation') {
    score *= 2
  }

  return Math.max(0, Math.round(score))
}

// 添加 endGame 函数
const endGame = (isWin = false) => {
  isPlaying.value = false
  gameOver.value = true
  if (timer) {
    clearInterval(timer)
  }

  // 如果是胜利结束，显示提示
  if (isWin) {
    alert('恭喜你完成拼图！')
  }
}
</script>

<style scoped>
.game-puzzle {
  width: 100%;
  height: 100%;
  position: relative;
  background: #000;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
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

.game-header {
  display: flex;
  justify-content: space-between;
  width: 600px;
  margin-bottom: 20px;
  font-size: 20px;
}

.game-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.game-start {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  padding: 40px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  width: 80%;
  max-width: 800px;
  box-sizing: border-box;
}

.game-settings {
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-row {
  display: flex;
  justify-content: center;
  width: 100%;
}

.settings-group {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 400px;
  justify-content: center;
}

.settings-group label {
  width: 100px;
  text-align: right;
  margin-right: 10px;
  color: #fff;
  font-size: 16px;
}

.settings-group select {
  width: 200px;
  padding: 8px 16px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
}

.image-select {
  margin: 20px auto;
  max-width: 800px;
  width: 100%;
}

.image-options {
  width: 100%;
  box-sizing: border-box;
}

.default-images {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding: 10px 0;
  width: 100%;
  flex-wrap: nowrap;
}

.image-option {
  flex: 0 0 200px;
  min-width: 200px;
  max-width: 200px;
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 150px;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #fff;
}

.upload-placeholder i {
  font-size: 2rem;
}

.selection-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 24px;
  height: 24px;
  background: #00ff00;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  animation: scaleIn 0.3s ease;
}

.image-label {
  margin-top: 8px;
  text-align: center;
  color: #fff;
  font-size: 14px;
}

.image-option.selected {
  border-color: #00ff00;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}

/* 添加水平滚动条样式 */
.default-images::-webkit-scrollbar {
  height: 6px;
}

.default-images::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.default-images::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.default-images::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}

.puzzle-board {
  position: relative;
  background: #333;
  border-radius: 8px;
  overflow: hidden;
}

.puzzle-piece {
  position: absolute;
  background-size: cover;
  cursor: move;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.3);
  transition: transform 0.3s ease;
}

.puzzle-piece.correct-position {
  box-shadow: inset 0 0 0 2px #00ff00;
}

.game-over {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.9);
  padding: 40px;
  border-radius: 12px;
  text-align: center;
  backdrop-filter: blur(10px);
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
  margin: 20px auto;
  min-width: 200px;
  max-width: 300px;
  width: 100%;
}

button:hover:not(:disabled) {
  background: #00cc00;
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

button:disabled {
  background: #666;
  cursor: not-allowed;
}

select {
  padding: 8px 16px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  margin-left: 10px;
  cursor: pointer;
  appearance: none; /* 移除默认的下拉箭头 */
  -webkit-appearance: none;
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
}

/* 添加自定义下拉箭头 */
.difficulty-select, .game-mode-select {
  position: relative;
}

.difficulty-select::after,
.game-mode-select::after {
  content: '▼';
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: white;
  pointer-events: none;
}

/* 修改选项样式 */
select option {
  background-color: #1a1a1a;
  color: white;
  padding: 12px;
}

/* 添加悬停和焦点效果 */
select:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #00ff00;
}

select:focus {
  outline: none;
  border-color: #00ff00;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

/* 确保选项在下拉时可见 */
select:not(:checked) option {
  background-color: #1a1a1a;
  color: white;
}

/* 选中选项的样式 */
select option:checked {
  background-color: #00ff00;
  color: black;
}

/* 悬停选项的样式 */
select option:hover {
  background-color: rgba(0, 255, 0, 0.2);
}

@media (max-width: 768px) {
  .game-header,
  .puzzle-board {
    width: 100% !important;
    height: auto !important;
    aspect-ratio: 1;
  }
}

/* 添加新的样式 */
.game-mode-select {
  margin: 20px 0;
  text-align: left;
}

.game-controls {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: center;
}

.piece-number {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}

.rotation-indicator {
  position: absolute;
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
  color: #00ff00;
  font-size: 20px;
  text-shadow: 0 0 3px black;
}

.rotatable {
  cursor: move;
}

.rotatable:hover::after {
  content: '右键旋转';
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
}

.rotating {
  transition: transform 0.3s ease;
}

.final-score {
  font-size: 24px;
  color: #00ff00;
  margin: 20px 0;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.difficulty {
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 20px;
  border-radius: 6px;
}

/* 添加更多动画效果 */
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.puzzle-piece.rotating {
  animation: rotate 0.3s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>