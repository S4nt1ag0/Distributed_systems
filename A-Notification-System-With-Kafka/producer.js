const { Kafka } = require('kafkajs')
const express = require('express')
const bodyParser = require('body-parser')
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['ec2-18-208-190-1.compute-1.amazonaws.com:9092'],
})

const producer = kafka.producer(
  allowAutoTopicCreation: true
)


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
  console.log(data)
  res.send(data);
  enviaNotificacao(data)
})


app.listen(9000, async ()=>{
  console.log('foi zeze')
  await producer.connect()
  enviaNotificacao(
    {
    "topic":"quickstart-events",
    "message":"enviando por outra maquina"
    }
    )
})
