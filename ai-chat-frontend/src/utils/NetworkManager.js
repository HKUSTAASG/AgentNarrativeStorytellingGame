import { soundManager } from './SoundManager'

class NetworkManager {
  constructor() {
    this.socket = null
    this.players = new Map()
    this.onPlayerJoin = null
    this.onPlayerLeave = null
    this.onPlayerUpdate = null
    this.onChatMessage = null
  }

  connect(url) {
    this.socket = new WebSocket(url)

    this.socket.onopen = () => {
      console.log('已连接到服务器')
      soundManager.playSound('connect')
    }

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.handleMessage(data)
    }

    this.socket.onclose = () => {
      console.log('与服务器断开连接')
      soundManager.playSound('disconnect')
      setTimeout(() => this.connect(url), 5000)
    }
  }

  handleMessage(data) {
    switch (data.type) {
      case 'playerJoin':
        if (this.onPlayerJoin) {
          this.onPlayerJoin(data.player)
        }
        this.players.set(data.player.id, data.player)
        soundManager.playSound('playerJoin')
        break

      case 'playerLeave':
        if (this.onPlayerLeave) {
          this.onPlayerLeave(data.playerId)
        }
        this.players.delete(data.playerId)
        soundManager.playSound('playerLeave')
        break

      case 'playerUpdate':
        if (this.onPlayerUpdate) {
          this.onPlayerUpdate(data.player)
        }
        this.players.set(data.player.id, data.player)
        break

      case 'chat':
        if (this.onChatMessage) {
          this.onChatMessage(data.message)
        }
        soundManager.playSound('chat')
        break
    }
  }

  sendUpdate(playerData) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({
        type: 'playerUpdate',
        player: playerData
      }))
    }
  }

  sendChat(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({
        type: 'chat',
        message
      }))
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close()
    }
  }
}

export const networkManager = new NetworkManager()