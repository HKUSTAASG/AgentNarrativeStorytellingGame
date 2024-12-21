<template>
  <div class="multi-ai-container" :style="{
    backgroundImage: `linear-gradient(
      to bottom,
      rgba(28, 32, 34, 0.85),
      rgba(28, 32, 34, 0.95)
    ), url(${skyBg})`
  }">
    <div class="background-layer"></div>
    <ParticleBackground />

    <!-- 横向布局的AI代理和对话区域 -->
    <div class="main-layout">
      <!-- AI代理区域 -->
      <div class="agents-row">
        <div v-for="(agent, index) in agents"
             :key="index"
             :class="['agent-node', { 'active': currentAiIndex === index }]">
          <div class="agent-avatar" :style="{ backgroundColor: agent.color }">
            {{ agent.avatar }}
          </div>
          <div class="agent-info">
            <div class="agent-name">{{ agent.name }}</div>
            <div class="agent-role">{{ agent.role }}</div>
          </div>
          <div class="agent-status"
               :class="{ 'typing': currentAiIndex === index && isLoading }">
            {{ currentAiIndex === index && isLoading ? '思考中...' : '等待中' }}
          </div>
        </div>
      </div>

      <!-- 对话区域 -->
      <div class="conversation-area">
        <!-- 回复展示区 -->
        <div class="responses-area" ref="responsesContainer">
          <div v-if="userMessage" class="user-message">
            <div class="message-header">你的问题：</div>
            <div class="message-content">{{ userMessage }}</div>
          </div>

          <div v-for="(response, index) in responses"
               :key="index"
               :class="['ai-response', { 'active': currentAiIndex === response.aiIndex }]">
            <div class="response-header">
              <div class="agent-avatar small"
                   :style="{ backgroundColor: agents[response.aiIndex].color }">
                {{ agents[response.aiIndex].avatar }}
              </div>
              <div class="agent-name">{{ agents[response.aiIndex].name }}</div>
            </div>
            <div class="response-content">{{ response.content }}</div>
          </div>
        </div>

        <!-- 用户输入 -->
        <div class="input-section">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="输入你的问题..."
            :disabled="isLoading"
          />
          <button
            @click="sendMessage"
            :disabled="isLoading"
            :class="{'loading': isLoading}"
          >
            {{ isLoading ? '对话中...' : '发送' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import ParticleBackground from './ParticleBackground.vue'
import skyBg from '@/assets/sky.png'

const agents = [
  {
    name: 'John',
    role: 'Keywords Extractor',
    color: '#2196F3',
    avatar: '👨‍💼'
  },
  {
    name: 'Lisa',
    role: 'Memory Retriever',
    color: '#FF4081',
    avatar: '👩‍🎨'
  },
  {
    name: 'Maha',
    role: 'Answer Generator',
    color: '#4CAF50',
    avatar: '🧠'
  }
]

const userInput = ref('')
const userMessage = ref('')
const isLoading = ref(false)
const currentAiIndex = ref(null)
const responses = ref([])
const responsesContainer = ref(null)

const scrollToBottom = () => {
  if (responsesContainer.value) {
    nextTick(() => {
      responsesContainer.value.scrollTop = responsesContainer.value.scrollHeight
    })
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  userMessage.value = userInput.value
  userInput.value = ''
  isLoading.value = true
  responses.value = []
  currentAiIndex.value = null

  try {
    const response = await fetch('http://127.0.0.1:9000/api/mulchat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userMessage.value
      })
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let done = false

    while (!done) {
      const { value, done: streamDone } = await reader.read()
      done = streamDone
      if (done) break

      const text = decoder.decode(value, { stream: true })
      const lines = text.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            switch (data.type) {
              case 'start': {
                currentAiIndex.value = data.aiIndex
                responses.value.push({
                  aiIndex: data.aiIndex,
                  content: ''
                })
                await nextTick()
                scrollToBottom()
                break
              }
              case 'token': {
                const currentResponse = responses.value.find(
                  r => r.aiIndex === data.aiIndex
                )
                if (currentResponse) {
                  currentResponse.content += data.token
                  await nextTick()
                  scrollToBottom()
                }
                break
              }
              case 'end': {
                currentAiIndex.value = null
                break
              }
            }
          } catch (error) {
            console.error('解析错误:', error)
          }
        }
      }
    }
  } catch (error) {
    console.error('错误:', error)
  } finally {
    isLoading.value = false
  }
}

watch(responses, () => {
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.multi-ai-container {
  height: 90vh;
  width: 90vw;
  max-width: 1600px;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 32px rgba(45, 51, 171, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.main-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 32px;
  gap: 32px;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.05),
    rgba(255, 255, 255, 0.02)
  );
}

.agents-row {
  display: flex;
  justify-content: space-around;
  padding: 32px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
}

.agent-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-radius: 16px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.08);
  min-width: 280px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
}

.agent-node:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.1);
}

.agent-node.active {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.agent-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.agent-avatar.small {
  width: 40px;
  height: 40px;
  font-size: 24px;
}

.agent-info {
  text-align: center;
  color: white;
}

.agent-name {
  font-size: 24px;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.agent-role {
  font-size: 16px;
  opacity: 0.8;
  margin-top: 4px;
}

.agent-status {
  font-size: 12px;
  color: #666;
}

.agent-status.typing {
  color: #4CAF50;
  animation: pulse 1s infinite;
}

.conversation-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 32px;
  height: calc(100vh - 300px);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.input-section {
  display: flex;
  gap: 10px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

input {
  flex: 1;
  padding: 15px;
  border: none;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 16px;
}

input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
}
input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  color: white;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
}

input:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(33, 150, 243, 0.5);
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.25);
  transform: translateY(-2px);
  animation: glow 1.5s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    box-shadow: 0 0 5px rgba(33, 150, 243, 0.2),
                0 0 10px rgba(33, 150, 243, 0.2),
                0 0 15px rgba(33, 150, 243, 0.2);
  }
  to {
    box-shadow: 0 0 10px rgba(33, 150, 243, 0.3),
                0 0 20px rgba(33, 150, 243, 0.3),
                0 0 30px rgba(33, 150, 243, 0.3);
  }
}

button {
  padding: 15px 30px;
  border: none;
  border-radius: 4px;
  background: #2196F3;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  background: #1976D2;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.responses-area {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
  padding-right: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  max-height: calc(100vh - 400px);
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) rgba(255, 255, 255, 0.05);
  scroll-behavior: smooth;
}

.user-message {
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
}

.message-header {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 5px;
}

.message-content {
  font-size: 16px;
}

.ai-response {
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  transition: all 0.3s ease;
}

.ai-response.active {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.02);
}

.response-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.response-content {
  font-size: 16px;
  line-height: 1.5;
  white-space: pre-wrap;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* 滚动条样式 */
.responses-area::-webkit-scrollbar {
  width: 6px;
}

.responses-area::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.responses-area::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  transition: all 0.3s ease;
}

.responses-area::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
