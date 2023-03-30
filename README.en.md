<p align="center">
  <img width="180" src="https://avatars.githubusercontent.com/u/127706964?s=200&v=4" alt="LLMApi Chat">
  <h1 align="center">LLMApi Chat</h1>
  <p align="center">Self-host llmapi web chat for ChatGPT and others</p>
</p>

# Introdution

llmapi-chat is a simple `web-chat-server` backend that can chat with a variety of large language models (LLM, such as ChatGPT, GPT-3, GPT-4, etc.)

## Install & Run

1. build and run locally
``` shell
./build.sh
./start.sh
# visit http://127.0.0.1:8081
```

2. run with docker

``` shell
docker build -t llmapi-chat:0.1.0 .
docker run --name webchat -d -p 8081:8081 llmapi-chat:0.1.0
# visit http://127.0.0.1:8081
```
### Acknowledgements
This project developed based on [chatGPT-web](https://github.com/mic1on/chatGPT-web)
