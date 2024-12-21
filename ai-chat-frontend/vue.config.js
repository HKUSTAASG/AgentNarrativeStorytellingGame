const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: [
      'localhost',
      '.ngrok.io',
      '.idcfengye.com',
      '.natapp.cn',
      '.vaiwan.com',
      'your-custom-domain.com'
    ],
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws',
    },
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:9000',
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map'
  }
})
