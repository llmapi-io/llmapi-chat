<p align="center">
  <img width="180" src="https://avatars.githubusercontent.com/u/127706964?s=200&v=4" alt="LLMApi Chat">
  <h1 align="center">LLMApi Chat</h1>
  <p align="center">可私有化部署的ChatGPT WEB聊天服务端</p>
</p>


# 介绍

[English](README.en.md)

llmapi-chat 基于llmapi.io服务提供了简单的聊天服务器后端，可以直接和`ChatGPT` `GPT-3` `llama`等大模型聊天交互

## 已经支持的能力

- 连续对话: 使用`ChatGPT`进行多轮连续对话
- 文字补全: 使用`GPT-3`或`welm`模型进行文字补全
- 文字嵌入: 使用openai的`Embedding`模型，将语句转为向量，可以用来做分类、搜索等任务
- 文字生图: 使用`dall-e`模型，将文字转为图片
- 实时搜索: 使用`NewBing`接口，体验Bing搜索（基于ChatGPT,非官方接口）

## 安装和运行

1. 本地安装运行
``` shell
./build.sh
./start.sh
```

2. 使用docker运行

``` shell
docker build -t llmapi-chat:0.1.0 .
docker run --name webchat -d -p 8081:8081 llmapi-chat:0.1.0
```

## 访问

> 在浏览器打开:`http://127.0.0.1:8081`即可访问webchat页面

你可以在[llmapi.io](https://llmapi.io)上注册账号即可获得`apikey`，按照以下示例，完成配置后即可与`ChatGPT` `GPT-3`以及其他流行的LLM进行聊天:

<p align="center">
  <img src="demo/demo.png" alt="Chat demo">
</p>

### 致谢
本项目基于[chatGPT-web](https://github.com/mic1on/chatGPT-web)开发
