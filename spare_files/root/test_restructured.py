import requests
import json
import time

def test_chat(message, user_id="test_user"):
    import sys
    url = "http://localhost:8001/api/chat"
    payload = {"message": message, "user_id": user_id}
    print(f"\nUSER: {message}")
    resp = requests.post(url, json=payload, stream=True)
    full_resp = ""
    for chunk in resp.iter_lines():
        if chunk:
            text = chunk.decode('utf-8')
            try:
                print(text, end="", flush=True)
            except UnicodeEncodeError:
                print(text.encode('ascii', 'ignore').decode('ascii'), end="", flush=True)
            full_resp += text
    print()
    return full_resp

def verify():
    # TEST 1: Greeting
    test_chat("Hello!", user_id="user_123")
    
    # TEST 2: Factual (Phi3)
    test_chat("Tell me about the Chapli Kebab", user_id="user_123")
    
    # TEST 3: Reasoning (Llama RAG) + Recommendation
    test_chat("I want something spicy for dinner", user_id="user_123")
    
    # TEST 4: Add to cart
    test_chat("add to cart the Chapli Kebab", user_id="user_123")
    
    # TEST 5: Order Persistence (Personalization)
    print("\n--- Testing Personalization (New Session) ---")
    test_chat("Hi!", user_id="user_123")
    
    # TEST 7: Location
    test_chat("Where are you located?", user_id="user_123")
    
    # TEST 8: Reservation
    test_chat("I want to book a table for tomorrow", user_id="user_123")
    
    # TEST 9: Hallucination Check (Off-menu)
    test_chat("Do you have any sushi or pizza?", user_id="user_123")
    
    # TEST 10: Identity
    test_chat("how are you ?", user_id="user_123")
    test_chat("what is your name?", user_id="user_123")
    
    # TEST 11: Menu
    test_chat("show me your menu", user_id="user_123")
    
    # TEST 12: Category Filtering
    test_chat("i only want chicken items", user_id="user_123")
    test_chat("show me your starters", user_id="user_123")
    test_chat("do you have any desserts?", user_id="user_123")

if __name__ == "__main__":
    verify()
