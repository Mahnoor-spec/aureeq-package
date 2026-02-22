import httpx
import asyncio

async def check():
    print("Testing 'i am hungry'...")
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            res = await client.post("http://127.0.0.1:8001/chat", json={"message": "i am hungry", "user_id": "test_persuasion"})
            full_text = ""
            async for chunk in res.aiter_text():
                full_text += chunk
            print(f"RESPONSE:\n{full_text}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(check())
