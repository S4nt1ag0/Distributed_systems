const { Kafka } = require('kafkajs')
const express = require('express')
const bodyParser = require('body-parser')
const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['ipv4-amazon:9092'],
})

const producer = kafka.producer()


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
})