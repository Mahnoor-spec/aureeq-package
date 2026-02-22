import httpx
import asyncio

async def test_tts():
    url = "http://127.0.0.1:8880/generate"
    payload = {"text": "Hello, this is a test.", "voice": "am_adam"}
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(url, json=payload, timeout=20.0)
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                print(f"Success! Received {len(r.content)} bytes.")
            else:
                print(f"Error: {r.text}")
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_tts())
