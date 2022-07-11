<template>
    <div>
        <h1>Notificações Recebidas:</h1>
        <p v-for="(message,index) in messages" :key="index">
            {{message}}
        </p>
    </div>
</template>

<script>
import { io } from 'socket.io-client'
export default {
    data(){
        return{
            messages:[],
            connection: io('http://localhost:8000')
        }
    },
  mounted(){
    this.connection.on('message', (message) => {
      this.messages.push(message)
      console.log(message)
    })
    }
}
</script>