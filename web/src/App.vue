<script setup lang="ts">
import { message as messageTip } from 'ant-design-vue'
import dayjs from 'dayjs'
import { SendOutlined, ClearOutlined, LoadingOutlined, RedoOutlined, SettingOutlined, GithubOutlined } from '@ant-design/icons-vue'
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
  inputHint:"当前会话无效，请先在右上角的设置中配置API KEY和使用的模型"
})

const messages = useMessages()

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

const msgfeed = async () => {
    state.message += '\n'
}

const sendMessage = async (event: { preventDefault: () => void }) => {
 	if(state.message == ""){
		messageTip.warning("消息不可以为空")
  		return
 	}
 	if(state.session_ok == false){
		messageTip.warning("会话还未成功创建，请先在右上角设置中配置API KEY和使用的模型")
  		return
 	}
 	if(state.loadding == true){
		messageTip.warning("正在处理上一条消息，请勿重复发送")
  		return
 	}

  	event.preventDefault()
  	state.loadding = true

	var pre_hint = state.inputHint
	state.inputHint = "正在努力处理您的问题，请耐心等待 ..."

  	addmsg()

  	let question = ""
  	question = state.message
  	state.message = ""
  	const data:any = await chatask(question, state.session)
 	var replyMessage = data?.reply ? (data.reply) : data?.msg
  	if (setting.value.model == "dall-e"){
		replyMessage = '<img width="256px" src="' + replyMessage +'"></img>'
	}
  	var n = dayjs().format('YYYY-MM-DD HH:mm:ss')
  	messages.addMessage({
    		username: setting.value.model,
    		msg: replyMessage,
		time: n,
    		type: 0,
  	})
  	await new Promise(f => setTimeout(f, 1000));
  	updated()
  	state.inputHint = pre_hint
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
  window.open('https://github.com/llmapi-io/llmapi-chat')
}

onMounted(async () => {
  	await startSession()
	messageTip.config({                 
  		getContainer: () => document.getElementById('msgtip')!,
  		duration: 2,                      
  		maxCount: 3,                      
		});                                 
	state.inputHint = state.session_ok ? ("正在与"+setting.value.model+"对话，Ctrl+Enter换行，Enter或点击按钮发送") : ("会话无效，请先在右上角设置中配置API KEY和使用的模型")
})

</script>

<template>
  <div id="layout">
    <setting-modal v-model:visible="state.visible" />
    <header id="header" style="background-color:#220730; height:2.2rem" class="text-white select-none">
      <span class="text-size-5 pl-5 "><a href="https://llmapi.io" target="_blank" style="color:white" >LLMApi</a></span>
      <a-tooltip>
        <template #title>清除聊天记录</template>
        <a-popconfirm title="确定清除本地所有聊天记录吗?" ok-text="确定" cancel-text="取消" @confirm="clearMessages">
          <ClearOutlined class="pl-4 cursor-pointer" />
        </a-popconfirm>
      </a-tooltip>

      <a-tooltip>
        <template #title>开源地址</template>
        <GithubOutlined class="pl-3 cursor-pointer" @click="handleToGithub" />
      </a-tooltip>
      <LoadingOutlined v-if="state.loadding" class="pl-3 cursor-pointer" />

      <span class="float-right pr-5" style="padding-top:0.4rem">
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

    <div id="msgtip" style="float:left background-color:#073069"></div>

    <footer id="footer">
      <div class="relative p-4 w-full overflow-hidden text-gray-600 focus-within:text-gray-400 flex items-center">
        <a-textarea shape="round" v-model:value="state.message" :auto-size="{ minRows: 3, maxRows: 5 }" :placeholder="state.inputHint" @keydown.enter.prevent.exact="sendMessage($event)" @keydown.ctrl.enter="msgfeed()" class="appearance-none pl-10 py-2 w-full bg-white border border-gray-300 text-sm placeholder-gray-800 focus:outline-none focus:border-blue-500 focus:shadow-outline-blue" />
        <span class="absolute inset-y-0 right-0 bottom-10 pr-6 flex items-end">
          <a-button v-model:disabled="state.loadding" shape="round" type="primary" @click="sendMessage($event)"><SendOutlined v-if="state.loadding==false" class="pl-3 cursor-pointer" /><LoadingOutlined v-if="state.loadding" class="pl-3 cursor-pointer" /></a-button>
          
        </span>
      </div>
    </footer>

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
  scrollbar-width: none; /* Firefox */
}
::-webkit-scrollbar {
  display: none; /* Chrome Safari */
}

#footer {
  width: 100%;
  height: auto;
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
