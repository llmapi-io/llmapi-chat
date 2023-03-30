import { useStorage } from '@vueuse/core'


type Setting = {
  app_key: string,
  model: string,
}

const setting = useStorage<Setting>('setting', {
  app_key: '',
  model: 'chatgpt',
})

const useSetting = () => setting

export default useSetting
