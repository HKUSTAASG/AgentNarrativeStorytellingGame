import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ChartView from '../views/ChartView.vue'
import GameView from '../views/GameView.vue'
import MetaView from '../views/MetaView.vue'
import MultiAIView from '../views/MultiAIView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/chart',
    name: 'chart',
    component: ChartView
  },
  {
    path: '/game',
    name: 'game',
    component: GameView
  },
  {
    path: '/metaverse',
    name: 'metaverse',
    component: MetaView
  },
  {
    path: '/multi-ai',
    name: 'multi-ai',
    component: MultiAIView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
