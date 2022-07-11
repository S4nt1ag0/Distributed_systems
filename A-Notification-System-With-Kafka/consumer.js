const { Kafka } = require('kafkajs')
const bodyParser = require('body-parser')
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['ec2-54-234-169-250.compute-1.amazonaws.com:9092'],
})

const consumer = kafka.consumer({ groupId: 'test-group' })

const express = require('express');
const app = express();
var cors = require('cors')
const http = require('http');
app.use(cors())
const server = http.createServer(app);
const io = require("socket.io")(server, {
  cors: {
    origins: ['*']
  }
})

const jsonParser = bodyParser.json()

app.get('/', (req, res) => {
  res.send('Hello World!')
})

server.listen(9005, async ()=>{
  await consumer.connect()
  await consumer.subscribe({ topic: 'investimentos', fromBeginning: true })
  
  io.on('connection', async (socket)=>{

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        socket.emit('message',message.value.toString())
      },
    })
  });

})

