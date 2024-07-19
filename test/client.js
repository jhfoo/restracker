const WebsocketClient = require('websocket').client

const client = new WebsocketClient()

client.on('connectFailed', (error) => {
  console.log('Connect Error: ' + error.toString())
})

client.on('connect', (connection) => {
  console.log('WebSocket Client Connected')
  connection.on('message', (message) => {
    if (message.type === 'utf8') {
      console.log("Received: '" + message.utf8Data + "'")
    }
  })
  connection.send ('Hello, I am a client.')
  console.log('Message sent')
})

client.connect('ws://localhost:8000/api/ws')