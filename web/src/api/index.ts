import { getRequest, postRequest } from "./api";
import useSetting from "@/composables/setting";

const setting = useSetting()

export const chatstart= async () => {
  const res = await postRequest({
    url: '/start',
    data: {
      apikey: setting.value.app_key,
      bot_type: setting.value.model,
    }
  })
  return res
}

export const chatend= async (sess: string) => {
  const res = await postRequest({
    url: '/end',
    data: {
      apikey: setting.value.app_key,
      session: sess,
    }
  })
  return res
}

export const chatask= async (text: string, sess: string) => {
  const res = await postRequest({
    url: '/ask',
    data: {
      apikey: setting.value.app_key,
      session: sess,
      content: text,
      timeout: 60
    }
  })
  return res
}

