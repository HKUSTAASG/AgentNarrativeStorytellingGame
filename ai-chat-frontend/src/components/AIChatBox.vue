<template>
    <div class="chat-container">
      <!-- 添加背景图层 -->
      <div class="background-layer"></div>

      <!-- 添加粒子背景 -->
      <ParticleBackground />

      <!-- 聊天消息列表 -->
      <div class="messages" ref="messageContainer">
        <TransitionGroup name="message">
          <div v-for="(message, index) in messages"
               :key="index"
               :class="['message', message.role]">
            <div class="avatar">
              {{ message.role === 'user' ? '你' : 'AI' }}
            </div>
            <div class="message-content">
              <div class="message-text" ref="messageText">{{ message.content }}</div>
              <img v-if="message.image" :src="message.image" alt="Message image" />
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- 输入区域 -->
      <div class="input-container">
        <div class="button-group">
          <button
            class="clear-history"
            @click="clearHistory"
            :disabled="isLoading"
          >
            <i class="fas fa-trash"></i>
            清空历史
          </button>
        </div>
        <div class="input-area">
          <!-- 添加图片上传按钮 -->
          <div class="image-upload">
            <input
              type="file"
              ref="fileInput"
              @change="handleImageUpload"
              accept="image/*"
              class="file-input"
            />
            <button class="upload-btn" @click="triggerFileInput">
              <i class="fas fa-image"></i>
            </button>
          </div>

          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="输入消息..."
            :disabled="isLoading"
          />
          <button
            @click="handleButtonClick"
            :disabled="isLoading"
            :class="{'loading': isLoading}"
          >
            {{ isLoading ? '回复中...' : '发送' }}
          </button>
        </div>

        <!-- 图片预览 -->
        <div v-if="selectedImage" class="image-preview">
          <img :src="selectedImage" alt="Selected image" />
          <button class="remove-image" @click="removeImage">×</button>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, onMounted, onUnmounted, watch, nextTick, defineEmits, defineExpose } from 'vue'
  import { createRipple } from '@/utils/animations'
  import ParticleBackground from './ParticleBackground.vue'

  const emit = defineEmits(['updateChat'])

  const messages = ref([
    {
        role: 'assistant',
        content: '你好，我是你的AI助手，有什么问题可以问我。'
    }
  ])
  const userInput = ref('')
  const isLoading = ref(false)
  const messageContainer = ref(null)
  let eventSource = null
  const fileInput = ref(null)
  const selectedImage = ref(null)

  const triggerFileInput = () => {
    fileInput.value.click()
  }

  const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        selectedImage.value = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }

  const removeImage = () => {
    selectedImage.value = null
    fileInput.value.value = ''
  }

  const sendMessage = async () => {
    if ((!userInput.value.trim() && !selectedImage.value) || isLoading.value) return

    const userMessage = userInput.value
    messages.value.push({
      role: 'user',
      content: userMessage,
      image: selectedImage.value
    })

    userInput.value = ''
    const imageData = selectedImage.value
    selectedImage.value = null
    isLoading.value = true

    try {
      if (eventSource) {
        eventSource.close()
      }

      // 创建请求数据
      const requestData = {
        message: userMessage,
        image: imageData
      }

      // 修改为正确的 URL
      const response = await fetch('http://127.0.0.1:9000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      const assistantMessageIndex = messages.value.length
      messages.value.push({
        role: 'assistant',
        content: ''
      })

      let reading = true
      while (reading) {
        const { value, done } = await reader.read()
        if (done) {
          reading = false
          break
        }

        const text = decoder.decode(value)
        const lines = text.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              switch (data.type) {
                case 'connected':
                  console.log('连接成功:', data.message)
                  break
                case 'message':
                  messages.value[assistantMessageIndex].content = data.response
                  break
                case 'done':
                  console.log('响应完成:', data.message)
                  isLoading.value = false
                  break
                case 'error':
                  console.error('服务器错误:', data.message)
                  messages.value[assistantMessageIndex].content = '发生错误：' + data.message
                  isLoading.value = false
                  break
              }
            } catch (error) {
              console.error('解析错误:', error)
            }
          }
        }
      }

      // 在消息发送成功后更新侧边栏
      updateSidebar()
    } catch (error) {
      console.error('错误:', error)
      messages.value.push({
        role: 'assistant',
        content: '抱歉，发生了错误，请稍后重试。'
      })
      isLoading.value = false
    }
  }

  const scrollToBottom = () => {
    if (messageContainer.value) {
      nextTick(() => {
        messageContainer.value.scrollTop = messageContainer.value.scrollHeight
      })
    }
  }

  watch(messages, () => {
    scrollToBottom()
  }, { deep: true })

  onMounted(() => {
    scrollToBottom()
    updateSidebar()
  })

  onUnmounted(() => {
    if (eventSource) {
      eventSource.close()
    }
  })

  const handleButtonClick = (event) => {
    createRipple(event, event.currentTarget)
    sendMessage()
  }

  // 暴露给父组件的方法
  const clearMessages = () => {
    messages.value = [{
      role: 'assistant',
      content: '你好，我是你的AI助手，有什么问题可以问我。'
    }]
  }

  const loadMessages = (newMessages) => {
    if (newMessages && newMessages.length > 0) {
      messages.value = newMessages
    } else {
      clearMessages()
    }
  }

  // 在发送消息时更新侧边栏
  const updateSidebar = () => {
    const lastMessage = messages.value[messages.value.length - 1]
    emit('updateChat', {
      messages: [...messages.value],
      preview: lastMessage.content.slice(0, 30) + (lastMessage.content.length > 30 ? '...' : '')
    })
  }

  // 添加清空历史记录的函数
  const clearHistory = async () => {
    try {
      const response = await fetch('http://127.0.0.1:9000/api/chat/clear-history/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (response.ok) {
        // 清空前端显示的消息
        messages.value = []
        // 更新侧边栏
        updateSidebar()
        // 显示成功提示
        console.log('历史记录已清空')
      } else {
        throw new Error('清空历史记录失败')
      }
    } catch (error) {
      console.error('清空历史记录时出错:', error)
    }
  }

  // 暴露方法给父组件
  defineExpose({
    clearMessages,
    loadMessages
  })
  </script>

  <style scoped>
  .chat-container {
    height: 850px;
    width: 1000px;
    display: flex;
    flex-direction: column;
    background-color: rgba(240, 242, 245, 0.5);
    margin: 0 auto;
    background-image: linear-gradient(
      to bottom right,
      rgba(42, 122, 243, 0.1),
      rgba(0, 195, 98, 0.1)
    );
    backdrop-filter: blur(8px);
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  }

  /* 添加背景图层 */
  .background-layer {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/sky.png');  /* 替换为你的图片路径 */
    background-size: cover;
    background-position: center;
    opacity: 0.1;  /* 调整透明度 */
    pointer-events: none;  /* 确保不影响交互 */
    z-index: 0;  /* 确保在最底层 */
  }

  /* 确保其他内容在背景之上 */
  .messages,
  .input-container {
    position: relative;
    z-index: 1;
  }

  /* 添加玻璃态效果 */

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
  }

  .message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
    gap: 12px;
  }

  .message.user {
    flex-direction: row-reverse;
  }

  .avatar {
    width: 70px;
    height: 70px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: white;
    transition: all 0.3s ease;
  }

  .avatar:hover {
    transform: scale(1.1);
  }

  .user .avatar {
    background-color: #2a7af3;
  }

  .assistant .avatar {
    background-color: #00c362;
  }

  .message-content {
    max-width: 60%;
    padding: 20px 28px;
    border-radius: 4px;
    position: relative;
    transition: all 0.3s ease;
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
  }

  .message-content:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .user .message-content {
    background-color: rgba(42, 122, 243, 0.9);
    color: white;
    border-radius: 8px 2px 8px 8px;
  }

  .assistant .message-content {
    background-color: white;
    color: #333;
    border-radius: 2px 8px 8px 8px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .message-text {
    line-height: 1.5;
    font-size: 16px;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .input-container {
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 16px 20px;
  }

  .input-area {
    display: flex;
    gap: 12px;
    max-width: 1000px;
    margin: 0 auto;
  }

  input {
    flex: 1;
    padding: 10px 18px;
    border: 1px solid #e6e6e6;
    border-radius: 4px;
    font-size: 16px;
    transition: all 0.3s ease;
  }

  input:focus {
    outline: none;
    border-color: #2a7af3;
    box-shadow: 0 0 0 2px rgba(42, 122, 243, 0.2);
    transform: translateY(-1px);
  }

  input:disabled {
    background-color: #f5f5f5;
  }

  button {
    padding: 20px 40px;
    background-color: #2a7af3;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 180px;
    box-shadow: 0 2px 4px rgba(42, 122, 243, 0.3),
                0 4px 8px rgba(42, 122, 243, 0.2);
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
    transform: translateY(0);
  }

  button:hover:not(:disabled) {
    background-color: #1a6ae3;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(42, 122, 243, 0.4);
  }

  button:disabled {
    background-color: #b3b3b3;
    cursor: not-allowed;
  }

  button.loading {
    position: relative;
    padding-right: 40px;
  }

  button.loading::after {
    content: '';
    position: absolute;
    right: 12px;
    top: 50%;
    width: 16px;
    height: 16px;
    margin-top: -8px;
    border: 2px solid white;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* 滚动条样式 */
  .messages::-webkit-scrollbar {
    width: 6px;
  }

  .messages::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  .messages::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
  }

  .messages::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }

  /* 添加消息动画 */
  .message-enter-active,
  .message-leave-active {
    transition: all 0.3s ease;
  }

  .message-enter-from {
    opacity: 0;
    transform: translateY(20px);
  }

  .message-leave-to {
    opacity: 0;
    transform: translateY(-20px);
  }

  .image-upload {
    position: relative;
    margin-right: 8px;
  }

  .file-input {
    display: none;
  }

  .upload-btn {
    width: 40px;
    height: 40px;
    padding: 0;
    min-width: auto;
    background-color: #f0f2f5;
    color: #666;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .upload-btn:hover {
    background-color: #e4e6e9;
    color: #2a7af3;
  }

  .image-preview {
    margin-top: 8px;
    position: relative;
    display: inline-block;
  }

  .image-preview img {
    max-height: 100px;
    border-radius: 4px;
  }

  .remove-image {
    position: absolute;
    top: -8px;
    right: -8px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  .remove-image:hover {
    background-color: rgba(0, 0, 0, 0.7);
  }

  /* 消息中的图片样式 */
  .message-content img {
    max-width: 100%;
    border-radius: 4px;
    margin-top: 8px;
  }

  .button-group {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
  }

  .clear-history {
    padding: 8px 16px;
    background: #ff4d4f;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .clear-history:hover:not(:disabled) {
    background: #ff7875;
    transform: translateY(-1px);
  }

  .clear-history:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .clear-history i {
    font-size: 14px;
  }

  .input-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
  }
  </style>
