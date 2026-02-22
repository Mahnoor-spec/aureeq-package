import httpx
import asyncio

async def test_fixes():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Test Typo tolerance (Reservaton)
        print("--- Testing Typo: 'i want to make a reservaton' ---")
        res = await client.post("http://127.0.0.1:8001/chat", json={"message": "i want to make a reservaton", "user_id": "test_user"})
        full_text = ""
        async for chunk in res.aiter_text():
            full_text += chunk
        print(f"Full Text: {full_text}")
        if "reserve" in full_text.lower() or "table" in full_text.lower():
            print(">>> SUCCESS: Typo caught!")
        else:
            print(">>> FAILURE: Typo NOT caught!")

        # 2. Test Multi-keyword Filtering (Chicken starters)
        print("\n--- Testing Multi-keyword: 'chicken dishes from starters' ---")
        res = await client.post("http://127.0.0.1:8001/chat", json={"message": "chicken dishes from starters", "user_id": "test_user"})
        full_text = ""
        async for chunk in res.aiter_text():
            full_text += chunk
        print(f"Full Text: {full_text}")
        if "Chicken hummus" in full_text or "Chicken Avocado Hummus" in full_text:
            print(">>> SUCCESS: Chicken starters found!")
        else:
            print(">>> FAILURE: Chicken starters NOT found!")
        
        if "Chicken Kebab Barg" in full_text:
            print(">>> FAILURE: Main menu items leaked into starters!")
        else:
            print(">>> SUCCESS: Correctly filtered out main menu chicken!")

if __name__ == "__main__":
    asyncio.run(test_fixes())
