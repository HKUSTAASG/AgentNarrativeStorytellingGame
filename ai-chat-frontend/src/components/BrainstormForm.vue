<template>
  <div class="brainstorm-layout">
    <div class="unified-container">
      <div class="section-header">
        <h2 class="section-title">Interactive Story Analysis</h2>
      </div>

      <div class="content-grid">
        <!-- 左侧表单部分 -->
        <div class="form-section">
          <h3 class="subsection-title">Brainstorm Your Decision Points</h3>
          <!-- 故事概要 -->
          <div class="form-group">
            <label>Summarize your story in one sentence</label>
            <input
              type="text"
              v-model="storyOneSentence"
              class="form-input"
              placeholder="Enter your story summary..."
            >
          </div>

          <!-- 场景描述 -->
          <div class="form-group">
            <label>Please firstly describe your specific scenario</label>
            <textarea
              v-model="scenarioDescription"
              class="form-textarea"
              placeholder="Describe your scenario in detail..."
              rows="4"
            ></textarea>
          </div>

          <!-- 角色定义 -->
          <div class="form-group">
            <label>Which role do you want the audience to play in your scenario?</label>
            <div class="audience-roles-container">
              <div class="roles-control">
                <button @click="decreaseRoles" class="control-btn" :disabled="audienceRoles.length <= 1">
                  -
                </button>
                <span>{{ audienceRoles.length }} roles</span>
                <button @click="increaseRoles" class="control-btn" :disabled="audienceRoles.length >= 5">
                  +
                </button>
              </div>
              <div class="roles-list">
                <div v-for="(role, index) in audienceRoles" :key="index" class="role-input-group">
                  <div class="role-header">
                    <span class="role-number">Role {{ index + 1 }}</span>
                    <button @click="removeRole(index)" class="remove-btn" v-if="audienceRoles.length > 1">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                  <textarea
                    v-model="role.description"
                    class="form-textarea"
                    :placeholder="`Describe role ${index + 1}...`"
                    rows="3"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- 目标受众描述 -->
          <div class="form-group">
            <label>Then describe your target audience:</label>
            <textarea
              v-model="targetAudience"
              class="form-textarea"
              placeholder="Describe your target audience..."
              rows="3"
            ></textarea>
          </div>

          <!-- 年龄段分类 -->
          <div class="form-group">
            <label>Do you want me to classify your audience by age?</label>
            <div class="radio-group">
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="classifyByAge"
                  :value="true"
                > Yes
              </label>
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="classifyByAge"
                  :value="false"
                > No
              </label>
            </div>

            <!-- 年龄段选择（条件渲染） -->
            <div v-if="classifyByAge" class="age-range-selector">
              <div class="age-inputs">
                <input
                  type="number"
                  v-model="minAge"
                  class="age-input"
                  placeholder="Min age"
                  min="0"
                >
                <span>to</span>
                <input
                  type="number"
                  v-model="maxAge"
                  class="age-input"
                  placeholder="Max age"
                  min="0"
                >
              </div>
            </div>
          </div>

          <!-- 添加提交按钮 -->
          <div class="form-group">
            <button @click="submitForm" class="submit-button" :disabled="isSubmitting">
              {{ isSubmitting ? 'Analyzing...' : 'Submit' }}
            </button>
          </div>
        </div>

        <!-- 中间结果部分 -->
        <div class="results-section">
          <h3 class="subsection-title">Analysis Results</h3>
          <!-- 等待动画 -->
          <div v-if="isSubmitting" class="loading-animation">
            <div class="loading-spinner"></div>
            <p>Analyzing your story...</p>
          </div>

          <!-- 结果显示 -->
          <div v-else-if="analysis" class="results-content">
            <div class="results-scroll" v-html="formattedAnalysis"></div>
          </div>

          <!-- 空状态提示 -->
          <div v-else class="empty-state">
            <i class="fas fa-lightbulb empty-icon"></i>
            <p>Submit your story details to get AI analysis</p>
          </div>
        </div>

        <!-- 测试表单部分 -->
        <div class="test-section">
          <h3 class="subsection-title">Test Decision Points</h3>
          <!-- 复制左侧的表单结构，使用新的数据绑定 -->
          <div class="form-group">
            <label>Summarize your story in one sentence</label>
            <input
              type="text"
              v-model="testStoryOneSentence"
              class="form-input"
              placeholder="Enter your story summary..."
            >
          </div>

          <div class="form-group">
            <label>Please firstly describe your specific scenario</label>
            <textarea
              v-model="testScenarioDescription"
              class="form-textarea"
              placeholder="Describe your scenario in detail..."
              rows="4"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Which role do you want the audience to play in your scenario?</label>
            <div class="audience-roles-container">
              <div class="roles-control">
                <button @click="decreaseTestRoles" class="control-btn" :disabled="testAudienceRoles.length <= 1">
                  -
                </button>
                <span>{{ testAudienceRoles.length }} roles</span>
                <button @click="increaseTestRoles" class="control-btn" :disabled="testAudienceRoles.length >= 5">
                  +
                </button>
              </div>
              <div class="roles-list">
                <div v-for="(role, index) in testAudienceRoles" :key="index" class="role-input-group">
                  <div class="role-header">
                    <span class="role-number">Role {{ index + 1 }}</span>
                    <button @click="removeTestRole(index)" class="remove-btn" v-if="testAudienceRoles.length > 1">
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                  <textarea
                    v-model="role.description"
                    class="form-textarea"
                    :placeholder="`Describe role ${index + 1}...`"
                    rows="3"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Then describe your target audience:</label>
            <textarea
              v-model="testTargetAudience"
              class="form-textarea"
              placeholder="Describe your target audience..."
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Do you want me to classify your audience by age?</label>
            <div class="radio-group">
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="testClassifyByAge"
                  :value="true"
                > Yes
              </label>
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="testClassifyByAge"
                  :value="false"
                > No
              </label>
            </div>

            <div v-if="testClassifyByAge" class="age-range-selector">
              <div class="age-inputs">
                <input
                  type="number"
                  v-model="testMinAge"
                  class="age-input"
                  placeholder="Min age"
                  min="0"
                >
                <span>to</span>
                <input
                  type="number"
                  v-model="testMaxAge"
                  class="age-input"
                  placeholder="Max age"
                  min="0"
                >
              </div>
            </div>
          </div>

          <div class="form-group">
            <button @click="submitTestForm" class="submit-button" :disabled="isTestSubmitting">
              {{ isTestSubmitting ? 'Testing...' : 'Test' }}
            </button>
          </div>
        </div>

        <!-- 新增的测试结果部分 -->
        <div class="test-results-section">
          <h3 class="subsection-title">Test Analysis Results</h3>
          <!-- 等待动画 -->
          <div v-if="isTestSubmitting" class="loading-animation">
            <div class="loading-spinner"></div>
            <p>Analyzing test results...</p>
          </div>

          <!-- 测试结果显示 -->
          <div v-else-if="testAnalysis" class="results-content">
            <div class="results-scroll" v-html="formattedTestAnalysis"></div>
          </div>

          <!-- 空状态提示 -->
          <div v-else class="empty-state">
            <i class="fas fa-lightbulb empty-icon"></i>
            <p>Submit your test to get analysis</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const storyOneSentence = ref('')
const scenarioDescription = ref('')
const audienceRoles = ref([
  { description: '' }
])
const targetAudience = ref('')
const classifyByAge = ref(false)
const minAge = ref(null)
const maxAge = ref(null)

const isSubmitting = ref(false)
const analysis = ref('')

const increaseRoles = () => {
  if (audienceRoles.value.length < 5) {
    audienceRoles.value.push({ description: '' })
  }
}

const decreaseRoles = () => {
  if (audienceRoles.value.length > 1) {
    audienceRoles.value.pop()
  }
}

const removeRole = (index) => {
  audienceRoles.value.splice(index, 1)
}

const submitForm = async () => {
  try {
    isSubmitting.value = true

    const formData = {
      story_summary: storyOneSentence.value,
      scenario_description: scenarioDescription.value,
      audience_roles: audienceRoles.value.map((role, index) => ({
        description: role.description,
        order: index + 1
      })),
      target_audience: targetAudience.value,
      classify_by_age: classifyByAge.value,
      min_age: minAge.value,
      max_age: maxAge.value
    }

    const response = await axios.post('/api/brainstorm/submit/', formData)
    analysis.value = response.data.analysis

  } catch (error) {
    console.error('Error submitting form:', error)
    // 这里可以添加错误提示
  } finally {
    isSubmitting.value = false
  }
}

const formattedAnalysis = computed(() => {
  if (!analysis.value) return ''
  return analysis.value.replace(/\n/g, '<br>')
})

// 添加测试表单的响应式数据
const testStoryOneSentence = ref('')
const testScenarioDescription = ref('')
const testAudienceRoles = ref([{ description: '' }])
const testTargetAudience = ref('')
const testClassifyByAge = ref(false)
const testMinAge = ref(null)
const testMaxAge = ref(null)
const isTestSubmitting = ref(false)
const testAnalysis = ref('')

// 添加测试表单的方法
const increaseTestRoles = () => {
  if (testAudienceRoles.value.length < 5) {
    testAudienceRoles.value.push({ description: '' })
  }
}

const decreaseTestRoles = () => {
  if (testAudienceRoles.value.length > 1) {
    testAudienceRoles.value.pop()
  }
}

const removeTestRole = (index) => {
  testAudienceRoles.value.splice(index, 1)
}

const submitTestForm = async () => {
  try {
    isTestSubmitting.value = true

    const formData = {
      story_summary: testStoryOneSentence.value,
      scenario_description: testScenarioDescription.value,
      audience_roles: testAudienceRoles.value.map((role, index) => ({
        description: role.description,
        order: index + 1
      })),
      target_audience: testTargetAudience.value,
      classify_by_age: testClassifyByAge.value,
      min_age: testMinAge.value,
      max_age: testMaxAge.value
    }

    const response = await axios.post('/api/brainstorm/test/', formData)
    testAnalysis.value = response.data.analysis

  } catch (error) {
    console.error('Error testing form:', error)
  } finally {
    isTestSubmitting.value = false
  }
}

// 添加测试结果的计算属性
const formattedTestAnalysis = computed(() => {
  if (!testAnalysis.value) return ''
  return testAnalysis.value.replace(/\n/g, '<br>')
})
</script>

<style scoped>
/* 修改布局样式 */
.brainstorm-layout {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr)); /* 确保两列等宽 */
  gap: 2rem;
  max-width: 2000px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

/* 修改左侧表单容器样式 */
.brainstorm-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  height: 100%; /* 确保高度与右侧一致 */
  min-height: 800px; /* 设置最小高度 */
}

/* 修改右侧结果容器样式 */
.results-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  height: 100%; /* 确保高度与左侧一致 */
  min-height: 800px; /* 设置最小高度 */
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 6rem;
}

/* 确保内容区域可以滚动 */
.results-content {
  flex-grow: 1;
  overflow: hidden;
  height: calc(100% - 4rem); /* 减去标题的高度 */
}

.results-scroll {
  height: 100%;
  overflow-y: auto;
  padding-right: 1rem;
  padding: 1rem;
}

/* 响应式设计调整 */
@media (max-width: 1200px) {
  .brainstorm-layout {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .brainstorm-container,
  .results-container {
    min-height: auto; /* 在移动端取消最小高度限制 */
  }

  .results-container {
    position: static;
    height: 600px; /* 在移动端设置固定高度 */
  }
}

.results-title {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
}

.results-content {
  flex-grow: 1;
  overflow: hidden;
}

.results-scroll {
  height: 100%;
  overflow-y: auto;
  padding-right: 1rem;
  line-height: 1.6;
  color: #4a5568;
}

/* 等待动画 */
.loading-animation {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #4a5568;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 空状态样式 */
.empty-state {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #a0aec0;
  text-align: center;
  padding: 2rem;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #4299e1;
}

/* 滚动条样式 */
.results-scroll::-webkit-scrollbar {
  width: 6px;
}

.results-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.results-scroll::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.results-scroll::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* 结果内容样式 */
.results-content :deep(h3) {
  color: #2d3748;
  font-size: 1.25rem;
  margin: 1.5rem 0 1rem;
  font-weight: 600;
}

.results-content :deep(ul) {
  padding-left: 1.5rem;
  margin: 1rem 0;
}

.results-content :deep(li) {
  margin-bottom: 0.5rem;
}

.brainstorm-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 2rem auto;
}

.section-title {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus, .form-textarea:focus {
  border-color: #4299e1;
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.custom-rows-input {
  margin-top: 0.5rem;
}

.rows-control {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.row-btn {
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s ease;
}

.row-btn:hover {
  background: #3182ce;
}

.radio-group {
  display: flex;
  gap: 2rem;
  margin-top: 0.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.age-range-selector {
  margin-top: 1rem;
}

.age-inputs {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.age-input {
  width: 100px;
  padding: 0.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  text-align: center;
}

/* 动画效果 */
.form-group {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 为每个表单组加延迟动画 */
.form-group:nth-child(1) { animation-delay: 0.1s; }
.form-group:nth-child(2) { animation-delay: 0.2s; }
.form-group:nth-child(3) { animation-delay: 0.3s; }
.form-group:nth-child(4) { animation-delay: 0.4s; }
.form-group:nth-child(5) { animation-delay: 0.5s; }

.audience-roles-container {
  margin-top: 1rem;
}

.roles-control {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.control-btn {
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 24px;
  font-weight: bold;
  line-height: 1;
  padding-bottom: 4px;
}

.control-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.control-btn:not(:disabled):hover {
  background: #3182ce;
  transform: translateY(-2px);
}

.roles-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.role-input-group {
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  padding: 1rem;
  position: relative;
}

.role-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.role-number {
  font-weight: 500;
  color: #4299e1;
}

.remove-btn {
  background: none;
  border: none;
  color: #e53e3e;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: rgba(229, 62, 62, 0.1);
}

/* 添加动画效果 */
.role-input-group {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.submit-button {
  background: #4299e1;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  margin-top: 20px;
}

.submit-button:hover:not(:disabled) {
  background: #3182ce;
  transform: translateY(-2px);
}

.submit-button:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.analysis-section {
  margin-top: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.analysis-section h3 {
  color: #2d3748;
  margin-bottom: 15px;
}

.analysis-content {
  white-space: pre-line;
  line-height: 1.6;
  color: #4a5568;
}

/* 添加标题容器样式 */
.section-header {
  height: 60px; /* 固定标题区域高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

.section-title {
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0; /* 移除标题默认边距 */
}

/* 修改容器样式 */
.unified-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 100%; /* 修改最大宽度 */
  margin: 0 auto;
  height: calc(100vh - 8rem); /* 设置高度为视窗高度减去顶部和底部间距 */
  overflow-y: auto; /* 添加垂直滚动 */
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem; /* 减小间距 */
  height: 100%; /* 设置高度为100% */
}

/* 调整各部分容器的样式 */
.form-section,
.results-section,
.test-section,
.test-results-section {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  padding: 1.5rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  height: calc(100vh - 12rem); /* 调整高度 */
  overflow-y: auto; /* 添加滚动条 */
  display: flex;
  flex-direction: column;
}

/* 调整标题样式 */
.section-header {
  height: 50px; /* 减小标题区域高度 */
  margin-bottom: 1.5rem;
}

/* 调整表单组样式 */
.form-group {
  margin-bottom: 1rem; /* 减小底部间距 */
}

/* 调整文本框高度 */
.form-textarea {
  min-height: 80px; /* 设置最小高度 */
  max-height: 200px; /* 设置最大高度 */
}

/* 响应式设计调整 */
@media (max-width: 1800px) {
  .content-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-section,
  .results-section,
  .test-section,
  .test-results-section {
    height: calc(100vh - 14rem);
  }
}

@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .unified-container {
    height: auto;
    padding: 1.5rem;
  }

  .form-section,
  .results-section,
  .test-section,
  .test-results-section {
    height: auto;
    min-height: 500px;
  }
}

/* 添加滚动条样式 */
.form-section::-webkit-scrollbar,
.results-section::-webkit-scrollbar,
.test-section::-webkit-scrollbar,
.test-results-section::-webkit-scrollbar,
.unified-container::-webkit-scrollbar {
  width: 6px;
}

.form-section::-webkit-scrollbar-track,
.results-section::-webkit-scrollbar-track,
.test-section::-webkit-scrollbar-track,
.test-results-section::-webkit-scrollbar-track,
.unified-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

.form-section::-webkit-scrollbar-thumb,
.results-section::-webkit-scrollbar-thumb,
.test-section::-webkit-scrollbar-thumb,
.test-results-section::-webkit-scrollbar-thumb,
.unified-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.form-section::-webkit-scrollbar-thumb:hover,
.results-section::-webkit-scrollbar-thumb:hover,
.test-section::-webkit-scrollbar-thumb:hover,
.test-results-section::-webkit-scrollbar-thumb:hover,
.unified-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 调整内容间距 */
.brainstorm-layout {
  padding: 1rem;
  width: 100%;
  height: 100%;
}
</style>