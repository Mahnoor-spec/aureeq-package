
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv("d:/AI sales agent/model_training/.env")
api_key = os.getenv("GOOGLE_API_KEY")

print(f"Configuring with key: {api_key[:5]}...")

try:
    genai.configure(api_key=api_key)
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except ImportError:
    print("google.generativeai not found. Trying google.genai...")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        # Testing simple generation logic for new SDK (v0.1+)
        # It's different.
        print("Using google-genai SDK. Attempting generate on gemini-1.5-flash...")
        response = client.models.generate_content(
            model='gemini-1.5-flash', contents='Hello'
        )
        print("Success:", response.text)
    except Exception as e2:
         print(f"SDK Error: {e2}")

except Exception as e:
    print(f"Error listing models: {e}")
