import { useStorage } from '@vueuse/core'


type Setting = {
  api_key: string,
  model: string,
  system: string,
}

const setting = useStorage<Setting>('setting', {
  api_key: '',
  model: 'chatgpt',
  system: 'You are a helpful assistant',
})

const useSetting = () => setting

export default useSetting
