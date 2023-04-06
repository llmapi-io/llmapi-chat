<script setup lang="ts">
import useSetting from '@/composables/setting'
import { SettingOutlined } from '@ant-design/icons-vue'

const setting = useSetting()
const models = ref(['chatgpt', 'gpt3', 'newbing', 'welm', 'gpt-embedding', 'dall-e'])

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['update:visible'])

const visible = computed({
  get: () => props.visible,
  set: value => emit('update:visible', value)
})

const handleOk = () => {
  visible.value = false
  window.location.reload()
}


</script>

<template>
  <div>
    <a-modal v-model:visible="visible" @ok="handleOk" okText="确定" cancelText="关闭">
      <template #title>
        <SettingOutlined />
        <span class="ml-2">设置</span>
      </template>

      <a-form :model="setting">
        <a-form-item label="api key">
          <a-input v-model:value="setting.api_key" placeholder="Register on https://llmapi.io to get the api key" />
        </a-form-item>
        <a-form-item label="bot">
          <a-select ref="select" v-model:value="setting.model" style="width: 180px">
            <a-select-option :value="model" v-for="model in models">{{ model }}</a-select-option>
          </a-select>
        </a-form-item>

	<a-form-item v-if="setting.model=='chatgpt'" label="system">
          <a-input v-model:value="setting.system" placeholder="default:You are a helpful assistant" />
        </a-form-item>
      </a-form>

      <div class="mt-2"></div>

    </a-modal>
  </div>
</template>
