<template>
  <div id="app">
    <header class="header">
      <div class="header-container">
        <div class="logo-section">
          <img src="@/assets/logo1.jpg" alt="Logo" class="logo">
          <h1 class="site-title">44-3 Meta Campus</h1>
        </div>
        <nav class="navigation">
          <router-link to="/" class="nav-link">
            <i class="fa fa-home"></i>
            Overview
          </router-link>
          <router-link to="/about" class="nav-link">
            <i class="fa fa-comments"></i>
            Chat
          </router-link>
          <router-link to="/chart" class="nav-link">
            <i class="fa fa-database"></i>
            Data Visualization
          </router-link>
          <router-link to="/game" class="nav-link">
            <i class="fa fa-gamepad"></i>
            Game
          </router-link>
          <router-link to="/metaverse" class="nav-link">
            <i class="fa fa-globe"></i>
            Storytelling
          </router-link>
          <router-link to="/multi-ai" class="nav-link">
            <i class="fa fa-star"></i>
            Multi-AI Chat
          </router-link>
        </nav>
      </div>
    </header>
    <main class="main-content">
      <router-view/>
    </main>
  </div>
</template>

<style lang="less">
#app {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.8rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-right: auto;
}

.logo {
  height: 2.5rem;
  transition: transform 0.3s ease;
  &:hover {
    transform: scale(1.1);
  }
}

.site-title {
  font-size: 1.0rem;
  font-weight: 600;
  background: linear-gradient(45deg, #2196F3, #4CAF50);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  white-space: nowrap;
}

.navigation {
  display: flex;
  gap: 1.5rem;
  margin-left: auto;
}

.nav-link {
  text-decoration: none;
  color: #666;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  i {
    font-size: 1.1rem;
  }
  &:hover {
    color: #2196F3;
    background: rgba(33, 150, 243, 0.1);
  }
  &.router-link-active {
    color: #2196F3;
    background: rgba(33, 150, 243, 0.15);
    font-weight: 500;
  }
}

.main-content {
  padding-top: 5rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    padding: 0.8rem 1rem;
  }
  .site-title {
    font-size: 0.8rem;
  }
  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}

/* 全局动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
