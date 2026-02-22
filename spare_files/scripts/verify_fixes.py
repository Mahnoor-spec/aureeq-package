import asyncio
import httpx
import json

async def test_fixes():
    url = "http://localhost:8001/chat"
    user_id = "test_user_fixes"
    
    test_cases = [
        ("what is your restaurant name", "IYI Dining", "Identity/Restaurant Name"),
        ("i want to do investmnet", "Sorry, I am only able to help you with your food selections.", "Topic Filter (Typo)"),
        ("what is the price of baked meat", "£94.99", "Baked Meat Price (Factual)"),
        ("tell me about computer equipment", "Sorry, I am only able to help you with your food selections.", "Topic Filter (Tech)"),
        ("suggest me something for dinner", "£94.99", "Baked Meat Price (Reasoning/RAG Check)")
    ]
    
    for query, expected, label in test_cases:
        print(f"\nTesting {label}: '{query}'")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                full_resp = ""
                async with client.stream("POST", url, json={"user_id": user_id, "message": query}) as response:
                    async for line in response.aiter_lines():
                        if line:
                            full_resp += line
                
                print(f"Response: {full_resp}")
                if expected in full_resp:
                    print(f"✅ PASSED")
                else:
                    print(f"❌ FAILED: Expected '{expected}' to be in response.")
        except Exception as e:
            print(f"Error testing {label}: {e}")

if __name__ == "__main__":
    asyncio.run(test_fixes())
