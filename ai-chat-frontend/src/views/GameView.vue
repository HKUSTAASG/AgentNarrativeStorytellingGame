<template>
  <div class="game-view">
    <div class="game-container">
      <!-- 游戏选择菜单 -->
      <div v-if="!selectedGame" class="game-menu">
        <h1>选择游戏</h1>
        <div class="game-grid-container">
          <div class="game-grid">
            <div v-for="game in games"
                 :key="game.id"
                 class="game-card"
                 @click="selectGame(game.id)">
              <div class="game-icon">
                <i :class="game.icon"></i>
              </div>
              <h2>{{ game.name }}</h2>
              <p>{{ game.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 游戏组件 -->
      <component
        v-else
        :is="currentGameComponent"
        @back-to-menu="backToMenu"
      ></component>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Game3D from '@/components/Game3D.vue'
import GameTetris from '@/components/GameTetris.vue'
import GameSnake from '@/components/GameSnake.vue'
import GamePuzzle from '@/components/GamePuzzle.vue'

const selectedGame = ref(null)

const games = [
  {
    id: 'space',
    name: '太空探索',
    description: '3D太空飞行游戏',
    icon: 'fas fa-rocket',
    component: Game3D
  },
  {
    id: 'tetris',
    name: '俄罗斯方块',
    description: '经典俄罗斯方块游戏',
    icon: 'fas fa-th-large',
    component: GameTetris
  },
  {
    id: 'snake',
    name: '贪吃蛇',
    description: '经典贪吃蛇游戏',
    icon: 'fas fa-square',
    component: GameSnake
  },
  {
    id: 'puzzle',
    name: '拼图游戏',
    description: '图片拼图游戏',
    icon: 'fas fa-puzzle-piece',
    component: GamePuzzle
  }
]

const currentGameComponent = computed(() => {
  const game = games.find(g => g.id === selectedGame.value)
  return game ? game.component : null
})

const selectGame = (gameId) => {
  selectedGame.value = gameId
}

const backToMenu = () => {
  selectedGame.value = null
}
</script>

<style scoped>
.game-view {
  min-height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, #1a1a1a 0%, #363636 100%);
  position: relative;
  overflow: hidden;
}

.game-container {
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

.game-menu {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: white;
}

.game-menu h1 {
  font-size: 3rem;
  margin-bottom: 40px;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.game-grid-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.game-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(250px, 300px));
  gap: 30px;
  width: fit-content;
  margin: 0 auto;
}

.game-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 250px;
}

.game-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.game-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.game-card h2 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #fff;
}

.game-card p {
  color: #ccc;
  font-size: 1rem;
  line-height: 1.4;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .game-grid {
    grid-template-columns: repeat(2, minmax(250px, 350px));
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .game-grid {
    grid-template-columns: minmax(250px, 350px);
    gap: 20px;
  }

  .game-menu h1 {
    font-size: 2rem;
  }

  .game-card {
    min-height: 250px;
  }
}
</style>