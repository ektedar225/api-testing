from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Hardcoded token — avoid in production
token = "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"
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

# Create client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# Call the model
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("What is the capital of France?")
    ],
    temperature=1,
    top_p=1,
    model=model
)

# Print the result
print(response.choices[0].message.content)
