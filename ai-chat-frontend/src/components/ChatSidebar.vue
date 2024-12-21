<template>
  <div class="chat-sidebar">
    <div class="sidebar-header">
      <h2>聊天记录</h2>
    </div>
    <div class="chat-history">
      <div v-for="(chat, index) in chatHistory"
           :key="index"
           class="chat-item"
           :class="{ active: currentChat === index }"
           @click="selectChat(index)">
        <div class="chat-item-content">
          <div class="chat-time">{{ formatTime(chat.time) }}</div>
          <div class="chat-preview">{{ chat.preview }}</div>
        </div>
      </div>
    </div>
    <div class="sidebar-footer">
      <button class="new-chat-btn" @click="startNewChat">
        <i class="fas fa-plus"></i>
        新对话
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineExpose } from 'vue'

const emit = defineEmits(['newChat', 'selectChat'])

// 初始化聊天历史，包含一个默认对话
const chatHistory = ref([{
  time: new Date(),
  preview: '你好，我是你的AI助手，有什么问题可以问我。',
  messages: [{
    role: 'assistant',
    content: '你好，我是你的AI助手，有什么问题可以问我。'
  }]
}])

const currentChat = ref(0)

const formatTime = (date) => {
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else if (days === 1) {
    return '昨天'
  } else if (days === 2) {
    return '前天'
  } else {
    return date.toLocaleDateString('zh-CN')
  }
}

const selectChat = (index) => {
  currentChat.value = index
  emit('selectChat', chatHistory.value[index])
}

const startNewChat = () => {
  chatHistory.value.unshift({
    time: new Date(),
    preview: '新对话',
    messages: []
  })
  currentChat.value = 0
  emit('newChat')
}

// 修改更新对话的方法
const updateCurrentChat = (chatData) => {
  if (chatHistory.value[currentChat.value]) {
    chatHistory.value[currentChat.value].messages = chatData.messages
    chatHistory.value[currentChat.value].preview = chatData.preview
    chatHistory.value[currentChat.value].time = new Date()
  } else {
    // 如果当前没有对话，创建一个新的
    chatHistory.value.unshift({
      time: new Date(),
      preview: chatData.preview,
      messages: chatData.messages
    })
    currentChat.value = 0
  }
}

defineExpose({
  updateCurrentChat
})
</script>

<style scoped>
.chat-sidebar {
  width: 450px;
  height: 850px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  margin-right: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.chat-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 8px;
}

.chat-item:hover {
  background: rgba(42, 122, 243, 0.1);
}

.chat-item.active {
  background: rgba(42, 122, 243, 0.15);
}

.chat-item-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-time {
  font-size: 14px;
  color: #666;
}

.chat-preview {
  font-size: 16px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.new-chat-btn {
  width: 100%;
  padding: 12px;
  background: #2a7af3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  background: #1a6ae3;
  transform: translateY(-1px);
}

/* 滚动条样式 */
.chat-history::-webkit-scrollbar {
  width: 4px;
}

.chat-history::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-history::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.chat-history::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>