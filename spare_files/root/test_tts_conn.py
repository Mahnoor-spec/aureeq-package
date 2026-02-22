import httpx
import asyncio

async def test():
    urls = ["http://127.0.0.1:8880", "http://localhost:8880"]
    for url in urls:
        print(f"Testing {url}...")
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url)
                print(f"Success! Status: {resp.status_code}, Content: {resp.text[:50]}")
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
