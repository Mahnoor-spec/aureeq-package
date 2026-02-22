import httpx
import json
import asyncio

async def test_chat():
    url = "http://localhost:8001/chat"
    payload = {
        "message": "Tell me about the Lamb Ribs, I am looking for something tender and flavorful.",
        "user_id": "test_user"
    }
    print(f"Sending request to {url}...")
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code == 200:
                    print("Response received:")
                    async for chunk in response.aiter_text():
                        print(chunk, end="", flush=True)
                    print("\nTest completed successfully.")
                else:
                    print(f"Error: {response.status_code}")
                    print(await response.aread())
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat())
