<template>
  <div class="metaverse-scroll-container">
    <div class="metaverse-container">
      <!-- 导航栏 -->
      <header class="header">
        <nav class="navbar navbar-expand-lg navbar-light py-4 index-forward bg-white">
          <div class="container d-flex justify-content-center">
            <a class="navbar-brand" href="#">
              <img src="/html/img/logo1.svg" alt="..." width="200" style="display: block; margin: 0 auto;">
            </a>
          </div>
        </nav>
      </header>

      <!-- 主要内容区 -->
      <section class="bg-white pb-5">
        <div class="hero-image-container">
          <img class="hero-image" src="/html/img/8.jpg" alt="">
        </div>
        <div class="content-container">
          <ul class="list-inline d-flex justify-content-center flex-row">
            <li class="list-inline-item mx-3"><a class="category-link fw-normal" href="#!">Storytelling</a></li>
            <li class="list-inline-item mx-3"><a class="meta-link fw-normal" href="#!">Audience</a></li>
            <li class="list-inline-item mx-3"><a class="meta-link fw-normal" href="#!">Septemper 2024</a></li>
          </ul>
          <h1 class="title">Interactive Story System & Storytelling</h1>
          <p class="description">This is a system for helping you with creating decision points from audience' views in interactive storytelling. You can choose two modes, brainstormming your decision points or testing your decision points.</p>
        </div>
      </section>

      <!-- 分类区域 -->
      <section class="categories-section">
        <div class="categories-container">
          <div class="category-grid">
            <a class="category-block"
               href="https://udify.app/workflow/uSKEDBOj8x21K66y"
               style="background-image: url(/html/img/category-bg-1.jpg)">
              <span class="category-block-title">Brainstorm your decision points</span>
            </a>
            <a class="category-block center-image"
               style="background-image: url(/html/img/11.png)">
            </a>
            <a class="category-block"
               href="https://udify.app/workflow/ctrFJjeSfrHBDnQq"
               style="background-image: url(/html/img/category-bg-3.jpg)">
              <span class="category-block-title">Test your decision points</span>
            </a>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// 在这里可以添加需要的逻辑
</script>

<style scoped>
/* 滚动容器样式 */
.metaverse-scroll-container {
  width: 100%;
  height: calc(100vh - 5rem);
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: 5rem;
}

/* 主容器样式 */
.metaverse-container {
  background: white;
  min-height: 100%;
  width: 100%;
}

/* 英雄图片区域 */
.hero-image-container {
  width: 100%;
  height: 60vh;
  overflow: hidden;
  position: relative;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s ease;
}

.hero-image:hover {
  transform: scale(1.05);
}

/* 内容区域 */
.content-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  margin: 1.5rem 0;
  color: #333;
  font-weight: bold;
}

.description {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #666;
  margin: 0 auto;
  max-width: 700px;
}

/* 分类区域 */
.categories-section {
  background: #f8f9fa;
  padding: 60px 0;
}

.categories-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.category-block {
  height: 500px;
  border-radius: 15px;
  overflow: hidden;
  position: relative;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.category-block:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

.center-image {
  background-size: contain;
  background-color: #f8f9fa;
}

.category-block-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: white;
  font-size: 1.5rem;
  text-align: center;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.category-block:hover .category-block-title {
  transform: translateY(0);
}

/* 导航链接样式 */
.list-inline {
  margin: 2rem 0;
}

.category-link, .meta-link {
  color: #666;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s ease;
}

.category-link:hover, .meta-link:hover {
  color: #333;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .category-block {
    height: 400px;
  }
}

@media (max-width: 992px) {
  .category-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .hero-image-container {
    height: 50vh;
  }

  .title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .category-grid {
    grid-template-columns: 1fr;
  }

  .category-block {
    height: 300px;
  }

  .hero-image-container {
    height: 40vh;
  }

  .title {
    font-size: 1.8rem;
  }

  .description {
    font-size: 1rem;
  }
}

/* 滚动条样式 */
.metaverse-scroll-container::-webkit-scrollbar {
  width: 8px;
}

.metaverse-scroll-container::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.1);
}

.metaverse-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.2);
  border-radius: 4px;
}

.metaverse-scroll-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0,0,0,0.3);
}
</style>
