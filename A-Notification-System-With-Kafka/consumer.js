const { Kafka } = require('kafkajs')
const express = require('express')
const bodyParser = require('body-parser')
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['ec2-18-208-190-1.compute-1.amazonaws.com:9092'],
})

const consumer = kafka.consumer({ groupId: 'test-group' })

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


app.listen(9000, async ()=>{
  await consumer.connect()
  await consumer.subscribe({ topic: 'quickstart-event', fromBeginning: true })
  await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    console.log({
      value: message.value.toString(),
    })
  },
})
})


