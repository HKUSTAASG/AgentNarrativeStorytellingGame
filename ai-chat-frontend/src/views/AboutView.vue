<template>
  <div class="all_view">
    <div class="about-container" ref="container">
      <div class="chat-layout">
        <ChatSidebar
          ref="sidebar"
          @new-chat="handleNewChat"
          @select-chat="handleSelectChat"
        />
        <AIChatBox
          ref="chatBox"
          :key="chatKey"
          @update-chat="handleChatUpdate"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AIChatBox from '@/components/AIChatBox.vue'
import ChatSidebar from '@/components/ChatSidebar.vue'
import { createBubble } from '@/utils/animations'
import '@/assets/animations.css'

const container = ref(null)
const chatBox = ref(null)
const sidebar = ref(null)
const chatKey = ref(0)
let bubbleInterval

const handleNewChat = () => {
  chatKey.value++
  if (chatBox.value) {
    chatBox.value.clearMessages()
  }
}

const handleSelectChat = (chat) => {
  if (chatBox.value) {
    chatBox.value.loadMessages(chat.messages)
  }
}

const handleChatUpdate = (chatData) => {
  if (sidebar.value) {
    sidebar.value.updateCurrentChat(chatData)
  }
}

onMounted(() => {
  bubbleInterval = setInterval(() => {
    if (container.value) {
      createBubble(container.value)
    }
  }, 2000)
})

onUnmounted(() => {
  clearInterval(bubbleInterval)
})
</script>

<style scoped>
.all_view {
  min-height: 100vh;
  background-color: #f5f5f5;
  position: relative;
  overflow: hidden;
}

.about-container {
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px);
}

.chat-layout {
  display: flex;
  align-items: flex-start;
  gap: 40px;
  max-width: 2000px;
  margin: 0 auto;
}
</style>
