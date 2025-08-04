from fastapi import FastAPI
from pydantic import BaseModel
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi.middleware.cors import CORSMiddleware
import os

# Load token from environment
token = os.getenv("AZURE_INFERENCE_API_KEY")  # set in Railway environment variable
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

# Initialize Azure inference client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

app = FastAPI()

# Enable CORS if accessing from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body format
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(chat_req: ChatRequest):
    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful assistant."),
                UserMessage(chat_req.message)
            ],
            temperature=1,
            top_p=1,
            model=model
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
