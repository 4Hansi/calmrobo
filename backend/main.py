# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .auth import router as auth_router
from .chatbot import chatbot_instance

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------- Chat Request Model --------
class ChatRequest(BaseModel):
    message: str


# -------- Authentication Routes --------
app.include_router(auth_router, prefix="/auth")


# -------- Chat Route --------
@app.post("/chat")
def chat(data: ChatRequest):
    """Accepts JSON body: { "message": "..." }"""
    return chatbot_instance.chat(data.message)


@app.get("/")
def home():
    return {"status": "ok"}
