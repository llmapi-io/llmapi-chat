import os

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, validator
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import api

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'web/dist')
ASSETS_DIR = os.path.join(DIST_DIR, 'assets')
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
templates = Jinja2Templates(directory=DIST_DIR)


class MessageStart(BaseModel):
    apikey:str
    bot_type:str
    setting:dict = None

class MessageEnd(BaseModel):
    apikey:str
    session:str

class MessageAsk(BaseModel):
    apikey:str
    session:str
    content:str
    timeout:int


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse(content={"code": 500, "error": {"message": f"{type(exc)} {exc}"}})


app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/start")
async def start(request: Request, message: MessageStart):
    print(f"stat:{message.apikey[:6]}***,{message.bot_type}")
    res = await api.llmapi_chat_start(message)
    print("res:",res)
    return res

@app.get("/end")
async def end(request: Request, message: MessageEnd):
    res = await api.llmapi_chat_end(message)
    return res

@app.post("/ask")
async def ask(request: Request, message: MessageAsk):
    res = await api.llmapi_chat_ask(message)
    return res

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8081)
