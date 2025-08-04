# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

# CORS for any origin (lock down in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pull in your GitHub token from Railway’s env variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

ENDPOINT = "https://models.github.ai/inference"
MODEL    = "openai/gpt-4.1"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", content:= ""},
            {"role": "user",   "content": req.message}
        ],
        "temperature": 1,
        "top_p": 1
    }

    r = requests.post(f"{ENDPOINT}/chat/completions", json=payload, headers=headers, timeout=15)
    r.raise_for_status()  # will raise HTTPError on 4xx/5xx
    data = r.json()
    # unwrap to match your old FastAPI response
    return {"response": data["choices"][0]["message"]["content"]}
