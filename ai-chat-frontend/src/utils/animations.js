// 打字机效果
export const typewriterEffect = (text, element, speed = 50) => {
  let i = 0
  const timer = setInterval(() => {
    if (i < text.length) {
      element.textContent += text.charAt(i)
      i++
    } else {
      clearInterval(timer)
    }
  }, speed)
}

// 渐入效果
export const fadeIn = (element, duration = 500) => {
  element.style.opacity = 0
  element.style.transition = `opacity ${duration}ms`
  setTimeout(() => {
    element.style.opacity = 1
  }, 10)
}

// 气泡效果
export const createBubble = (container) => {
  const bubble = document.createElement('div')
  bubble.className = 'chat-bubble'

  // 随机位置和大小
  const size = Math.random() * 30 + 10
  bubble.style.width = `${size}px`
  bubble.style.height = `${size}px`
  bubble.style.left = `${Math.random() * 100}%`

  // 添加动画
  bubble.style.animation = `float ${Math.random() * 3 + 2}s linear infinite`
  container.appendChild(bubble)

  // 自动移除
  setTimeout(() => {
    bubble.remove()
  }, 5000)
}

// 波纹效果
export const createRipple = (event, element) => {
  const ripple = document.createElement('div')
  ripple.className = 'ripple'

  const rect = element.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)

  ripple.style.width = ripple.style.height = `${size}px`
  ripple.style.left = `${event.clientX - rect.left - size/2}px`
  ripple.style.top = `${event.clientY - rect.top - size/2}px`

  element.appendChild(ripple)

  setTimeout(() => {
    ripple.remove()
  }, 600)
}