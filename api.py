import httpx

async def llmapi_chat_start(message):
    url = "https://api.llmapi.io/v1/chat/start"
    print(message)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=message.dict(),
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        return response.json()

async def llmapi_chat_end(message):
    url = "https://api.llmapi.io/v1/chat/end"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=message.dict(),
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        return response.json()

async def llmapi_chat_ask(message):
    url = "https://api.llmapi.io/v1/chat/ask"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=message.dict(),
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        return response.json()
