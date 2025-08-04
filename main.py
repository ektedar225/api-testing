from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os, requests

app = FastAPI()

# CORS (adjust origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set in environment")

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
            {"role": "system", "content": ""},    # empty system prompt
            {"role": "user",   "content": req.message}
        ],
        "temperature": 1,
        "top_p": 1
    }

    try:
        r = requests.post(
            f"{ENDPOINT}/chat/completions",
            json=payload,
            headers=headers,
            timeout=15
        )
        r.raise_for_status()
    except requests.RequestException as e:
        # bubble up a 502 with the underlying message
        raise HTTPException(status_code=502, detail=str(e))

    data = r.json()
    # unwrap and return
    return {"response": data["choices"][0]["message"]["content"]}
