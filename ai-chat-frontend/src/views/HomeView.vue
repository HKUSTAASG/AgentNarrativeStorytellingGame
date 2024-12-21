<template>
  <div class="home">
    <div class="story-container">
      <!-- 语言切换按钮移到 story-container 内部顶部 -->
      <div class="header-section">
        <button class="language-toggle" @click="toggleLanguage">
          {{ currentLanguage === 'zh' ? 'EN' : '中文' }}
        </button>
      </div>

      <!-- 背景故事部分 -->
      <div class="story-section world-background">
        <h2>{{ t('worldBackground') }}</h2>
        <div class="story-content">
          <p>{{ t('worldYear') }}</p>
          <p>{{ t('worldHistory') }}</p>
          <p>{{ t('worldSystem') }}</p>
        </div>
      </div>

      <div class="story-section school-background">
        <h2>{{ t('schoolBackground') }}</h2>
        <div class="story-content">
          <p>{{ t('schoolPurpose') }}</p>
          <p>{{ t('schoolDescription') }}</p>
          <p>{{ t('schoolSecret') }}</p>
        </div>
      </div>

      <div class="story-section character-background">
        <h2>{{ t('characterBackground') }}</h2>
        <div class="story-content">
          <div class="characters-grid">
            <div class="character">
              <div class="character-portrait player">
                <img src="@/assets/portraits/player.png" alt="Player Portrait">
              </div>
              <h3>{{ t('playerTitle') }}</h3>
              <p>{{ t('playerDescription') }}</p>
              <p>{{ t('playerSurfaceGoal') }}</p>
              <p>{{ t('playerRealGoal') }}</p>
            </div>

            <div class="character">
              <div class="character-portrait joey">
                <img src="@/assets/portraits/joey.png" alt="Joey Portrait">
              </div>
              <h3>{{ t('joeyTitle') }}</h3>
              <p>{{ t('joeyDescription') }}</p>
            </div>

            <div class="character">
              <div class="character-portrait robert">
                <img src="@/assets/portraits/robert.png" alt="Robert Portrait">
              </div>
              <h3>{{ t('robertTitle') }}</h3>
              <p>{{ t('robertDescription') }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 开始游戏按钮 -->
      <div class="start-section">
        <a href="http://localhost:5173/" class="start-button">{{ t('startGame') }}</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentLanguage = ref('zh')

const translations = {
  zh: {
    worldBackground: '世界背景',
    worldYear: '现在是精英计划的第24年（E24）。',
    worldHistory: '24年前，为了应对AI逐渐取代人类工作岗位而导致的失业潮和经济危机，全球各国联合创建了为期50年的精英联盟计划。',
    worldSystem: '这个"精英计划"将剩余的人类劳动力分为两个阶层：精英阶层和劳工阶层。所有其他劳动任务都由庞大的AI网络执行。精英阶层负责管理和开发所有AI，而劳工阶层则执行全球联盟分配的标准化机械任务，只能获得最低保障工资。',

    schoolBackground: '学校背景',
    schoolPurpose: '精英计划的关键在于人才培养。每年，全球联盟都会进行统一考试来选拔精英群体的候选人。',
    schoolDescription: '夏普学校专门为这次考试准备学生，每年进行初步筛选测试，从各地招收有天赋的年轻人，通过四年培训使他们成为优秀的精英候选人。20多年来，夏普学校的毕业生在统一考试中保持100%的通过率。',
    schoolSecret: '然而，夏普学校隐藏着一个秘密：它的建立是为了确保精英阶层的世代统治。所谓的初步筛选测试实际上是一种阶级过滤手段，只允许精英的后代成功获得入学资格。',

    characterBackground: '角色背景',
    playerTitle: '玩家',
    playerDescription: '你，20岁，来自劳工家庭，希望通过考试进入夏普学校来改变世界。',
    playerSurfaceGoal: '表面目标：通过考试，进入夏普学校。',
    playerRealGoal: '真实目标：拯救朱一（未来的你），揭露夏普学校的秘密，逃出时间循环。',

    joeyTitle: '朱一（Joey）',
    joeyDescription: '24岁，女性，夏普学校的高年级学生。',

    robertTitle: '罗勃特（Robert）',
    robertDescription: '48岁，男性，夏普学校校长。',

    startGame: '开始游戏'
  },
  en: {
    worldBackground: 'World Background',
    worldYear: 'The year is E24, marking the 24th year of the Elite Plan.',
    worldHistory: '24 years ago, in response to unemployment and economic crises caused by AI replacing human jobs, nations worldwide united to create the 50-year Elite Alliance Plan.',
    worldSystem: 'The "Elite Plan" divides the remaining human workforce into two classes: the Elite and Labor classes. All other tasks are performed by AI networks. The Elite class manages and develops AI, while the Labor class performs standardized tasks for minimal wages.',

    schoolBackground: 'School Background',
    schoolPurpose: 'Talent cultivation is crucial to the Elite Plan. Each year, the Global Union conducts unified exams to select elite candidates.',
    schoolDescription: 'Sharp School prepares students for this exam, conducting preliminary screening tests to recruit talented youth for four years of training. For over two decades, Sharp School graduates have maintained a 100% pass rate.',
    schoolSecret: 'However, Sharp School harbors a secret: it was established to ensure Elite class dominance. The screening test is actually a class filter, allowing only Elite descendants to gain admission.',

    characterBackground: 'Character Background',
    playerTitle: 'Player',
    playerDescription: 'You, age 20, from a Labor family, hoping to change the world by passing the exam and entering Sharp School.',
    playerSurfaceGoal: 'Apparent Goal: Pass the exam and enroll in Sharp School.',
    playerRealGoal: 'Real Goal: Save Joey (your future self), uncover Sharp School\'s secrets, and escape the time loop.',

    joeyTitle: 'Joey',
    joeyDescription: 'Age 24, female, a senior student at Sharp School.',

    robertTitle: 'Robert',
    robertDescription: 'Age 48, male, principal of Sharp School.',

    startGame: 'Start Game'
  }
}

const t = (key) => translations[currentLanguage.value][key]

const toggleLanguage = () => {
  currentLanguage.value = currentLanguage.value === 'zh' ? 'en' : 'zh'
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a2e 0%, #1a1a3e 100%);
  color: white;
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* 添加背景动画效果 */
.home::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(0, 255, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255, 0, 255, 0.05) 0%, transparent 50%);
  animation: backgroundPulse 10s infinite alternate;
}

@keyframes backgroundPulse {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}

.story-container {
  max-width: 1200px;
  width: 100%;
  background: rgba(10, 12, 32, 0.8);
  border-radius: 20px;
  padding: 40px;
  backdrop-filter: blur(10px);
  box-shadow:
    0 0 30px rgba(0, 255, 255, 0.1),
    inset 0 0 20px rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.story-section {
  margin-bottom: 40px;
  padding: 25px;
  background: rgba(20, 25, 50, 0.5);
  border-radius: 15px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
}

.story-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(0, 255, 255, 0.2) 50%,
    transparent 100%
  );
  animation: scanline 2s linear infinite;
}

@keyframes scanline {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.story-section:hover {
  transform: translateY(-5px) scale(1.02);
  background: rgba(30, 35, 60, 0.6);
  box-shadow:
    0 10px 30px rgba(0, 255, 255, 0.1),
    inset 0 0 20px rgba(0, 255, 255, 0.05);
}

h2 {
  color: #00ffff;
  font-size: 28px;
  margin-bottom: 20px;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  letter-spacing: 2px;
  position: relative;
  display: inline-block;
}

h2::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg,
    transparent 0%,
    #00ffff 50%,
    transparent 100%
  );
}

.story-content {
  font-size: 18px;
  line-height: 1.6;
  color: #cccccc;
}

.story-content p {
  margin-bottom: 15px;
}

.character {
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
}

.start-section {
  text-align: center;
  margin-top: 40px;
}

.start-button {
  display: inline-block;
  padding: 15px 40px;
  font-size: 24px;
  background: linear-gradient(45deg, #00ffff, #00ccff);
  color: #000;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-shadow: none;
  position: relative;
  overflow: hidden;
  letter-spacing: 1px;
  font-weight: bold;
  text-transform: uppercase;
}

.start-button::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  z-index: -1;
  border-radius: 10px;
  animation: borderGlow 2s linear infinite;
}

@keyframes borderGlow {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

.start-button:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow:
    0 10px 30px rgba(0, 255, 255, 0.3),
    0 0 20px rgba(0, 255, 255, 0.2);
  background: linear-gradient(45deg, #00ccff, #00ffff);
}

/* 添加滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 255, 0, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 255, 0, 0.5);
}

/* 添加语言切换按钮样式 */
.header-section {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.language-toggle {
  padding: 12px 24px;
  font-size: 16px;
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(0, 255, 255, 0.1));
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  letter-spacing: 1px;
}

.language-toggle:hover {
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.3), rgba(0, 255, 255, 0.2));
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.2);
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-top: 20px;
}

.character {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 30px;
  background: rgba(20, 25, 50, 0.7);
  border-radius: 15px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 255, 255, 0.1);
  position: relative;
}

.character::before {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  background: linear-gradient(45deg,
    rgba(0, 255, 255, 0.1),
    rgba(255, 0, 255, 0.1)
  );
  border-radius: 15px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.character:hover::before {
  opacity: 1;
}

.character-portrait {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 20px;
  border: 3px solid rgba(0, 255, 255, 0.3);
  box-shadow:
    0 0 20px rgba(0, 255, 255, 0.2),
    inset 0 0 20px rgba(0, 255, 255, 0.1);
  position: relative;
}

.character-portrait::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(0, 255, 255, 0.2) 0%,
    transparent 50%
  );
}

.character-portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.character:hover .character-portrait img {
  transform: scale(1.1) rotate(5deg);
}

.character h3 {
  margin: 15px 0;
  color: #00ff00;
  font-size: 24px;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

.character p {
  color: #cccccc;
  line-height: 1.6;
  margin-bottom: 10px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .characters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .characters-grid {
    grid-template-columns: 1fr;
  }
}
</style>
