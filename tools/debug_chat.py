import httpx
import asyncio
import traceback

async def debug():
    url = "http://127.0.0.1:8002/chat"
    payload = {"message": "hi", "user_id": "debug_user"}
    
    print(f"Sending request to {url}...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                print(f"Status Code: {response.status_code}")
                if response.status_code != 200:
                    text = await response.aread()
                    print(f"Error Response Body: {text.decode()}")
                else:
                    print("Reading stream...")
                    async for chunk in response.aiter_text():
                        print(f"Chunk: {chunk}")
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug())
