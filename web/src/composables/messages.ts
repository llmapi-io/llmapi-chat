import { useStorage } from '@vueuse/core'
import { TMessage } from '@/types'
import dayjs from 'dayjs'


const messages = useStorage<TMessage[]>('messages', [
  {
    username: "llmapi",
    msg: "你好，我是llmapi，在这里你可以和流行的语言大模型进行交流，初次使用请在右上角的配置中填入api key，并选择你想要对话的模型",
    time: dayjs().format('HH:mm'),
    type: 0,
  },
])



export default function useMessages() {
  const addMessage = (message: TMessage) => {
    messages.value.push({
      username: message.username,
      msg: message.msg,
      time: message.time || dayjs().format('HH:mm'),
      type: message.type,
    })
  }

  const clearMessages = () => {
    messages.value = []
  }

  const getLastMessages = (num: number = 10) => {
    return messages.value.slice(-num)
  }

  return {
    messages,
    addMessage,
    clearMessages,
    getLastMessages
  }
}
