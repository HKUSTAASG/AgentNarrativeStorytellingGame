<template>
  <div class="game-3d" ref="gameContainer" tabindex="0" @keydown="handleKeyDown" @keyup="handleKeyUp">
    <button class="back-button" @click="$emit('back-to-menu')">返回菜单</button>
    <div class="game-overlay" v-if="!isPlaying">
      <div class="game-menu">
        <h2>太空探索</h2>
        <button @click="startGame">开始游戏</button>
        <div class="controls-info">
          <h3>控制说明：</h3>
          <p>W/S - 前进/后退</p>
          <p>A/D - 左右移动</p>
          <p>Space - 跳跃</p>
          <p>鼠标 - 视角控制</p>
        </div>
      </div>
    </div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const gameContainer = ref(null)
const canvas = ref(null)
const isPlaying = ref(false)

let scene, camera, renderer, controls
let spaceship
let stars = []
let planets = []
let animationFrameId
let moveSpeed = 0.1
let rotateSpeed = 0.02

// 添加键盘状态
const keys = {
  w: false,
  s: false,
  a: false,
  d: false,
  space: false
}

const handleKeyDown = (event) => {
  if (!isPlaying.value) return

  switch (event.key.toLowerCase()) {
    case 'w':
      keys.w = true
      break
    case 's':
      keys.s = true
      break
    case 'a':
      keys.a = true
      break
    case 'd':
      keys.d = true
      break
    case ' ':
      keys.space = true
      break
  }
}

const handleKeyUp = (event) => {
  switch (event.key.toLowerCase()) {
    case 'w':
      keys.w = false
      break
    case 's':
      keys.s = false
      break
    case 'a':
      keys.a = false
      break
    case 'd':
      keys.d = false
      break
    case ' ':
      keys.space = false
      break
  }
}

const updateSpaceshipPosition = () => {
  if (!spaceship) return

  // 创建一个向量来存储移动方向
  const moveVector = new THREE.Vector3()

  // 根据按键状态更新移动向量
  if (keys.w) moveVector.z -= moveSpeed
  if (keys.s) moveVector.z += moveSpeed
  if (keys.a) moveVector.x -= moveSpeed
  if (keys.d) moveVector.x += moveSpeed
  if (keys.space) moveVector.y += moveSpeed

  // 应用移动
  spaceship.position.add(moveVector)

  // 添加简单的旋转效果
  if (keys.a) spaceship.rotation.y += rotateSpeed
  if (keys.d) spaceship.rotation.y -= rotateSpeed

  // 限制飞船的移动范围
  spaceship.position.x = THREE.MathUtils.clamp(spaceship.position.x, -50, 50)
  spaceship.position.y = THREE.MathUtils.clamp(spaceship.position.y, -30, 30)
  spaceship.position.z = THREE.MathUtils.clamp(spaceship.position.z, -50, 50)

  // 更新相机位置以跟随飞船
  camera.position.copy(spaceship.position)
  camera.position.add(new THREE.Vector3(0, 5, 10)) // 相机位置偏移
  camera.lookAt(spaceship.position)
}

const init = () => {
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x000020) // 深蓝色背景

  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  )
  camera.position.z = 5

  renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true
  })
  renderer.setSize(gameContainer.value.clientWidth, gameContainer.value.clientHeight)
  renderer.setPixelRatio(window.devicePixelRatio)

  // 添加环境光和平行光
  const ambientLight = new THREE.AmbientLight(0x404040, 0.5)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.position.set(5, 5, 5)
  scene.add(directionalLight)

  // 创建控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.enabled = false // 初始禁用轨道控制器

  createSpaceship()
  createStars()
  createPlanets()
  animate()
}

const createSpaceship = () => {
  // 创建一个更复杂的飞船模型
  const geometry = new THREE.Group()

  // 飞船主体
  const bodyGeometry = new THREE.ConeGeometry(0.5, 2, 8)
  const bodyMaterial = new THREE.MeshPhongMaterial({
    color: 0x00ff00,
    shininess: 100
  })
  const body = new THREE.Mesh(bodyGeometry, bodyMaterial)

  // 飞船翅膀
  const wingGeometry = new THREE.BoxGeometry(2, 0.1, 0.5)
  const wingMaterial = new THREE.MeshPhongMaterial({
    color: 0x00aa00,
    shininess: 100
  })
  const leftWing = new THREE.Mesh(wingGeometry, wingMaterial)
  leftWing.position.set(-0.5, 0, 0)
  const rightWing = new THREE.Mesh(wingGeometry, wingMaterial)
  rightWing.position.set(0.5, 0, 0)

  geometry.add(body)
  geometry.add(leftWing)
  geometry.add(rightWing)

  spaceship = geometry
  scene.add(spaceship)
}

const createStars = () => {
  const starGeometry = new THREE.SphereGeometry(0.05, 8, 8)
  const starMaterial = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true
  })

  for (let i = 0; i < 1000; i++) {
    const star = new THREE.Mesh(starGeometry, starMaterial)
    star.position.set(
      Math.random() * 200 - 100,
      Math.random() * 200 - 100,
      Math.random() * 200 - 100
    )
    stars.push(star)
    scene.add(star)
  }
}

const createPlanets = () => {
  const planetColors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00]
  const planetTextures = [
    new THREE.TextureLoader().load('path/to/texture1.jpg'),
    new THREE.TextureLoader().load('path/to/texture2.jpg'),
    new THREE.TextureLoader().load('path/to/texture3.jpg'),
    new THREE.TextureLoader().load('path/to/texture4.jpg')
  ]

  for (let i = 0; i < 4; i++) {
    const radius = Math.random() * 3 + 2
    const geometry = new THREE.SphereGeometry(radius, 32, 32)
    const material = new THREE.MeshPhongMaterial({
      color: planetColors[i],
      map: planetTextures[i],
      shininess: 50
    })
    const planet = new THREE.Mesh(geometry, material)

    planet.position.set(
      Math.random() * 80 - 40,
      Math.random() * 80 - 40,
      Math.random() * 80 - 40
    )

    planets.push(planet)
    scene.add(planet)
  }
}

const animate = () => {
  animationFrameId = requestAnimationFrame(animate)

  if (isPlaying.value) {
    updateSpaceshipPosition()
  }

  // 旋转行星
  planets.forEach(planet => {
    planet.rotation.y += 0.005
    planet.rotation.x += 0.002
  })

  // 闪烁星星
  stars.forEach(star => {
    star.material.opacity = 0.5 + Math.random() * 0.5
  })

  controls.update()
  renderer.render(scene, camera)
}

const startGame = () => {
  isPlaying.value = true
  gameContainer.value.focus() // 确保游戏容器获得焦点以接收键盘事件
  controls.enabled = true // 启用轨道控制器
}

const handleResize = () => {
  if (camera && renderer && gameContainer.value) {
    camera.aspect = gameContainer.value.clientWidth / gameContainer.value.clientHeight
    camera.updateProjectionMatrix()
    renderer.setSize(gameContainer.value.clientWidth, gameContainer.value.clientHeight)
  }
}

onMounted(() => {
  init()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cancelAnimationFrame(animationFrameId)
  scene.traverse(object => {
    if (object.geometry) {
      object.geometry.dispose()
    }
    if (object.material) {
      if (Array.isArray(object.material)) {
        object.material.forEach(material => material.dispose())
      } else {
        object.material.dispose()
      }
    }
  })
  renderer.dispose()
})
</script>

<style scoped>
.game-3d {
  width: 100%;
  height: 100%;
  position: relative;
  outline: none; /* 移除焦点时的轮廓 */
}

canvas {
  width: 100%;
  height: 100%;
}

.game-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.game-menu {
  text-align: center;
  color: white;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  backdrop-filter: blur(10px);
}

.game-menu h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.game-menu button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background: #00ff00;
  border: none;
  border-radius: 0.5rem;
  color: black;
  cursor: pointer;
  transition: all 0.3s ease;
}

.game-menu button:hover {
  background: #00cc00;
  transform: scale(1.1);
}

.controls-info {
  margin-top: 2rem;
  text-align: left;
}

.controls-info h3 {
  color: #00ff00;
  margin-bottom: 1rem;
}

.controls-info p {
  margin: 0.5rem 0;
  color: #cccccc;
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
  z-index: 100; /* 确保按钮在最上层 */
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}
</style>