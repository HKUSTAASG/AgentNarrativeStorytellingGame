<template>
    <div class="chat-container">
      <!-- 头部 -->
      <div class="chat-header">
        <h1>AI 智能助手</h1>
      </div>

      <!-- 聊天消息列表 -->
      <div class="messages" ref="messageContainer">
        <div v-for="(message, index) in messages"
             :key="index"
             :class="['message', message.role]">
          <div class="avatar">
            {{ message.role === 'user' ? '你' : 'AI' }}
          </div>
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-container">
        <div class="input-area">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="输入消息..."
            :disabled="isLoading"
          />
          <button
            @click="sendMessage"
            :disabled="isLoading"
            :class="{'loading': isLoading}"
          >
            {{ isLoading ? '回复中...' : '发送' }}
          </button>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

  const messages = ref([])
  const userInput = ref('')
  const isLoading = ref(false)
  const messageContainer = ref(null)
  let eventSource = null

  const sendMessage = async () => {
    if (!userInput.value.trim() || isLoading.value) return

    const userMessage = userInput.value
    messages.value.push({
      role: 'user',
      content: userMessage
    })

    userInput.value = ''
    isLoading.value = true

    try {
      if (eventSource) {
        eventSource.close()
      }

      const params = new URLSearchParams({ message: userMessage }).toString()
      eventSource = new EventSource(`http://localhost:9000/api/chat/?${params}`)

      const assistantMessageIndex = messages.value.length
      messages.value.push({
        role: 'assistant',
        content: ''
      })

      eventSource.onopen = (event) => {
        console.log('SSE 连接已建立:', event)
      }

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          switch (data.type) {
            case 'connected':
              console.log('SSE 连接成功:', data.message)
              break
            case 'message':
              messages.value[assistantMessageIndex].content = data.response
              break
            case 'done':
              console.log('响应完成:', data.message)
              eventSource.close()
              isLoading.value = false
              break
            case 'error':
              console.error('服务器错误:', data.message)
              messages.value[assistantMessageIndex].content = '发生错误：' + data.message
              eventSource.close()
              isLoading.value = false
              break
          }
        } catch (error) {
          console.error('解析错误:', error)
        }
      }

      eventSource.onerror = (error) => {
        console.error('SSE 错误:', error)
        eventSource.close()
        isLoading.value = false
        if (messages.value[assistantMessageIndex].content === '') {
          messages.value[assistantMessageIndex].content = '连接错误，请重试'
        }
      }
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
  })

  onUnmounted(() => {
    if (eventSource) {
      eventSource.close()
    }
  })
  </script>

  <style scoped>
  .chat-container {
    height: 500px;
    width: 600px;
    display: flex;
    flex-direction: column;
    background-color: #f0f2f5;
    background-image: url('@/assets/sky.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    margin: 0 auto;
    position: relative;
  }

  .chat-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.4);
    z-index: 0;
  }

  .chat-header {
    background-color: #2a7af3;
    color: white;
    padding: 16px 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 1;
  }

  .chat-header h1 {
    margin: 0;
    font-size: 18px;
    font-weight: 500;
  }

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
    width: 40px;
    height: 40px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: white;
  }

  .user .avatar {
    background-color: #2a7af3;
  }

  .assistant .avatar {
    background-color: #00c362;
  }

  .message-content {
    max-width: 60%;
    padding: 12px 16px;
    border-radius: 4px;
    position: relative;
  }

  .user .message-content {
    background-color: #2a7af3;
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
    font-size: 14px;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .input-container {
    background-color: white;
    border-top: 1px solid #e6e6e6;
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
    padding: 12px 16px;
    border: 1px solid #e6e6e6;
    border-radius: 4px;
    font-size: 14px;
    transition: all 0.3s;
  }

  input:focus {
    outline: none;
    border-color: #2a7af3;
    box-shadow: 0 0 0 2px rgba(42, 122, 243, 0.2);
  }

  input:disabled {
    background-color: #f5f5f5;
  }

  button {
    padding: 12px 24px;
    background-color: #2a7af3;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    min-width: 100px;
    box-shadow: 0 2px 4px rgba(42, 122, 243, 0.3),
                0 4px 8px rgba(42, 122, 243, 0.2);
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
    transform: translateY(0);
  }

  button:hover:not(:disabled) {
    background-color: #1a6ae3;
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
  </style>
