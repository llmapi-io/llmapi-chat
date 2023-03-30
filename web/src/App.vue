<script setup lang="ts">
import dayjs from 'dayjs'
import { ClearOutlined, LoadingOutlined, RedoOutlined, SettingOutlined, GithubOutlined } from '@ant-design/icons-vue'
import { chatstart, chatend, chatask} from '@/api'
import Message from './components/message.vue'
import SettingModal from './components/setting.vue'
import useSetting from '@/composables/setting'
import useMessages from '@/composables/messages'

const setting = useSetting()

const state = reactive({
  message: '',
  loadding: false,
  visible: false,
  session: '',
  session_ok: false,
})
const createdAt = dayjs().format('YYYY-MM-DD HH:mm:ss')

const messages = useMessages()

const inputHint ="当前使用的模型是:"+setting.value.model+"，请输入消息，Enter换行 ..." 

function updated(): void {
	let chatBox= document.getElementById('chatlog');
	if (chatBox) {
		chatBox.scrollIntoView({ behavior: "smooth", block: "end", inline: "end" });
	}
}

const addmsg = () => {
  var n = dayjs().format('YYYY-MM-DD HH:mm:ss')
  messages.addMessage({
    username: "user",
    msg: state.message,
	time: n,
    type: 1,
  })
  updated()
}

const sendMessage = async (event: { preventDefault: () => void }) => {
  event.preventDefault()
  state.loadding = true

  addmsg()

  let question = ""
  question = state.message
  state.message = ""
  const data:any = await chatask(question, state.session)
  const replyMessage = data?.reply ? (data.reply) : data?.msg
  var n = dayjs().format('YYYY-MM-DD HH:mm:ss')
  messages.addMessage({
    username: setting.value.model,
    msg: replyMessage,
	time: n,
    type: 0,
  })
  await new Promise(f => setTimeout(f, 1000));
  updated()
  state.loadding = false
}

const clearMessages = () => {
  messages.clearMessages()
}

const startSession = async () => {
  state.loadding = true
  const data:any = await chatstart()
  state.session = data?.session ? (data.session) : "" 
  state.session_ok = data?.session ? (true) : false 
  updated()
  state.loadding = false
}

const endSession = async () => {
  state.loadding = true
  await chatend(state.session)
  state.session = "" 
  state.session_ok = false
  state.loadding = false
}

const handleToGithub = () => {
  window.open('https://github.com/llmapi-io/')
}

onMounted(async () => {
  await startSession()
})


</script>

<template>
  <div id="layout">
    <header id="header" class="bg-dark-50 text-white h-10 select-none">
      <span class="text-size-5 pl-5">LLMApi</span>
      <a-tooltip>
        <template #title>清除聊天记录</template>
        <a-popconfirm title="确定清除本地所有聊天记录吗?" ok-text="确定" cancel-text="取消" @confirm="clearMessages">
          <ClearOutlined class="pl-3 cursor-pointer" />
        </a-popconfirm>
      </a-tooltip>

      <a-tooltip>
        <template #title>开源地址</template>
        <GithubOutlined class="pl-3 cursor-pointer" @click="handleToGithub" />
      </a-tooltip>
      <LoadingOutlined v-if="state.loadding" class="pl-3 cursor-pointer" />

	  <span class="float-right pr-3 pt-2">
      <a-tooltip>
        <template #title>设置</template>
        <SettingOutlined class="pl-3 cursor-pointer" @click="state.visible = true" />
      </a-tooltip>
	  </span>

    </header>
    <div id="layout-body">
      <main id="main">
        <div class="flex-1 relative flex flex-col">
          <!-- header -->
          <!-- content -->
          <div  id="chatlog" class="flex-1 inset-0 overflow-hidden bg-transparent bg-bottom bg-cover flex flex-col">
            <!-- dialog -->
            <div class="flex-1 w-full self-center">
              <div class="relative px-3 py-1 m-auto flex flex-col">
                <div class="mx-0 my-1 self-center text-xs text-gray-400">
                  {{ createdAt }}
                </div>
                <div v-if='state.session_ok' class="mx-0 my-1 self-center text-xs text-gray-400">
                  当前使用的模型是:{{ setting.model }}
		</div>
                <div v-else class="mx-0 my-1 self-center text-xs text-gray-400">
                  会话还未创建，请先在右上角设置中配置API KEY和使用的模型
		</div>
                <Message :message=msg v-for="msg in messages.messages.value"
                  :class="msg.type === 1 ? 'send' : 'replay'" />
      		<div v-if='state.loadding'>
                  {{ updated() }}
		</div>
              </div>
            </div>
          </div>
        </div>
      </main>

    </div>
    <footer id="footer">
      <div class="relative p-4 w-full overflow-hidden text-gray-600 focus-within:text-gray-400 flex items-center">
        <a-textarea v-model:value="state.message" :auto-size="{ minRows: 3, maxRows: 5 }" :placeholder="inputHint" 
          class="appearance-none pl-10 py-2 w-full bg-white border border-gray-300 rounded-full text-sm placeholder-gray-800 focus:outline-none focus:border-blue-500 focus:border-blue-500 focus:shadow-outline-blue" />
        <span class="absolute inset-y-0 right-0 bottom-6 pr-6 flex items-end">
          <a-button v-model:disabled="state.loadding" shape="round" type="primary" @click="sendMessage($event)">发送</a-button>
        </span>
      </div>

    </footer>
    <setting-modal v-model:visible="state.visible" />
  </div>
</template>

<style scoped>

#layout {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background-color: #f0f2f5;
}

#header {
  box-shadow: 2px 5px 5px 0px rgba(102, 102, 102, 0.5);
  flex-shrink: 0;
}

#layout-body {
  flex-grow: 2;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

#footer {
  border-top: 1px rgb(228, 228, 228) solid;
  width: 100%;
  height: 100px;
  flex-shrink: 0;
}

#main {
  flex-grow: 2;
}

.replay {
  float: left;
  clear: both;
}

.send {
  float: right;
  clear: both;
}

#chatlog {
	height: 300px;
}

</style>
