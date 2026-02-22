
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Explicitly load .env from the model_training folder
load_dotenv("d:/AI sales agent/model_training/.env")

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")

if api_key:
    print(f"API Key starting with: {api_key[:4]}...")

try:
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7
    )
    print("Attempting to invoke model...")
    res = llm.invoke("Hello, are you working?")
    print("Response received:")
    print(res.content)
except Exception as e:
    print(f"Error: {e}")
