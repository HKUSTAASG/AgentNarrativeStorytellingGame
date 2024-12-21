class SoundManager {
  constructor() {
    this.sounds = new Map()
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)()
    this.masterVolume = this.audioContext.createGain()
    this.masterVolume.connect(this.audioContext.destination)
    this.isMuted = false
  }

  async loadSound(name, url) {
    try {
      const response = await fetch(url)
      const arrayBuffer = await response.blob()
      const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer)
      this.sounds.set(name, audioBuffer)
    } catch (error) {
      console.error('加载音效失败:', error)
    }
  }

  playSound(name, options = {}) {
    if (this.isMuted) return

    const buffer = this.sounds.get(name)
    if (!buffer) return

    const source = this.audioContext.createBufferSource()
    const gainNode = this.audioContext.createGain()

    source.buffer = buffer
    source.connect(gainNode)
    gainNode.connect(this.masterVolume)

    if (options.loop) {
      source.loop = true
    }

    if (options.volume) {
      gainNode.gain.value = options.volume
    }

    if (options.spatialPosition) {
      const panner = this.audioContext.createPanner()
      panner.setPosition(...options.spatialPosition)
      gainNode.connect(panner)
      panner.connect(this.masterVolume)
    }

    source.start(0)
    return source
  }

  setMasterVolume(value) {
    this.masterVolume.gain.value = value
  }

  toggleMute() {
    this.isMuted = !this.isMuted
    this.masterVolume.gain.value = this.isMuted ? 0 : 1
  }

  stopAll() {
    this.audioContext.close()
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)()
  }
}

export const soundManager = new SoundManager()