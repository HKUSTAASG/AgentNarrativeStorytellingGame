<template>
  <div class="story-structure">
    <div class="unified-container">
      <div class="section-header">
        <h2 class="section-title">Story Structure Analysis</h2>
      </div>

      <div class="form-section">
        <div class="form-group">
          <label>Story Timeline</label>
          <input
            type="text"
            v-model="storyTimeline"
            class="form-input"
            placeholder="Enter your story timeline..."
          >
        </div>

        <div class="form-group">
          <label>Key Story Elements</label>
          <textarea
            v-model="storyElements"
            class="form-textarea"
            placeholder="Describe key elements..."
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label>Character Relationships</label>
          <div class="audience-roles-container">
            <div class="roles-control">
              <button @click="decreaseCharacters" class="control-btn" :disabled="characterRelations.length <= 1">
                -
              </button>
              <span>{{ characterRelations.length }} characters</span>
              <button @click="increaseCharacters" class="control-btn" :disabled="characterRelations.length >= 5">
                +
              </button>
            </div>
            <div class="roles-list">
              <div v-for="(char, index) in characterRelations" :key="index" class="role-input-group">
                <div class="role-header">
                  <span class="role-number">Character {{ index + 1 }}</span>
                  <button @click="removeCharacter(index)" class="remove-btn" v-if="characterRelations.length > 1">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <textarea
                  v-model="char.description"
                  class="form-textarea"
                  :placeholder="`Describe character ${index + 1}...`"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <button @click="analyzeStructure" class="submit-button" :disabled="isAnalyzing">
            {{ isAnalyzing ? 'Analyzing...' : 'Analyze Structure' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const storyTimeline = ref('')
const storyElements = ref('')
const characterRelations = ref([{ description: '' }])
const isAnalyzing = ref(false)

const increaseCharacters = () => {
  if (characterRelations.value.length < 5) {
    characterRelations.value.push({ description: '' })
  }
}

const decreaseCharacters = () => {
  if (characterRelations.value.length > 1) {
    characterRelations.value.pop()
  }
}

const removeCharacter = (index) => {
  characterRelations.value.splice(index, 1)
}

const analyzeStructure = async () => {
  try {
    isAnalyzing.value = true
    // 这里添加结构分析的逻辑
    await new Promise(resolve => setTimeout(resolve, 2000)) // 模拟API调用
  } catch (error) {
    console.error('Error analyzing structure:', error)
  } finally {
    isAnalyzing.value = false
  }
}
</script>

<style scoped>
/* 复用 BrainstormForm 的样式 */
.story-structure {
  width: 100%;
  height: 100%;
}

/* ... 其他样式与 BrainstormForm 相同 ... */
</style>