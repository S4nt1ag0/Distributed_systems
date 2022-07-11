const { Kafka } = require('kafkajs')
const express = require('express')
const bodyParser = require('body-parser')
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['ec2-54-234-169-250.compute-1.amazonaws.com:9092'],
})

const producer = kafka.producer({
  allowAutoTopicCreation: true
})


const app = express()

const jsonParser = bodyParser.json()

app.get('/', (req, res) => {
  res.send('Hello World!')
})

async function enviaNotificacao(data) {
  await producer.send({
    topic: data.topic,
    messages: [
      { value: data.message},
    ],
  })
}

app.post('/notify', jsonParser, (req, res) => {
  let data = req.body
  res.send(data);
  enviaNotificacao(data)
})


app.listen(9000, async ()=>{
  await producer.connect()
})
