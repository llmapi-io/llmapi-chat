<p align="center">
  <img width="180" src="https://avatars.githubusercontent.com/u/127706964?s=200&v=4" alt="LLMApi Chat">
  <h1 align="center">LLMApi Chat</h1>
  <p align="center">Self-host llmapi web chat for ChatGPT and others</p>
</p>

# Introdution

llmapi-chat is a simple `web-chat-server` backend that can chat with a variety of large language models (LLM, such as ChatGPT, GPT-3, GPT-4, etc.)

## Supportted ability

- Continuous Dialogue: Use `ChatGPT` for multiple rounds of continuous dialogue
- Text completion: use `GPT-3` or `welm` model for text completion
- Text embedding: use openai's `Embedding` model to convert sentences into vectors, which can be used for classification, search and other tasks
- Text to image: use `dall-e` model to convert text to image
- Real-time search: Use `NewBing` interface to experience Bing search (based on ChatGPT, unofficial interface)

## Install & Run

1. build and run locally
``` shell
./build.sh
./start.sh
```

2. run with docker

``` shell
docker build -t llmapi-chat:0.1.0 .
docker run --name webchat -d -p 8081:8081 llmapi-chat:0.1.0
```

## Visit
> Open `http://127.0.0.1:8081` in the browser to visit the webchat page.

You can sign up on [llmapi.io](https://llmapi.io) to get `apikey`, setup as below to chat with LLMs like `ChatGPT` `GPT3` and so on.

<p align="center">
  <img src="demo/demo.png" alt="Chat demo">
</p>

### Acknowledgements
This project developed based on [chatGPT-web](https://github.com/mic1on/chatGPT-web)
