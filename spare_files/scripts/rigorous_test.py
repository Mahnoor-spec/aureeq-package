import requests
import json
import time

BASE_URL = "http://localhost:8001/api/chat"
USER_ID = "rigorous_test_user_001"

prompts = [
    # --- PATH A: HARDCODED & GREETINGS ---
    "Hello",
    "What are your opening timings?",
    "I want to book a table for 4",
    "What is your cancellation policy?",
    "Hi again", # Test Order Intelligence after some orders
    
    # --- PATH A: CART ACTIONS ---
    "Add one Chicken Tikka to my cart",
    "Add a Baklava to my cart",
    "Add traditional humous to my cart",
    
    # --- PATH B1: FACTUAL (PHI3) ---
    "What is the price of Lamb Chops?",
    "What are the ingredients in Ranjha Gosht?",
    "Is the Chicken Karahi spicy?",
    "How large is the Mixed Grill portion?",
    "Where is IYI Dining located?",
    "What is in the Falafel?",
    "How much does the Prawns Tikka cost?",
    
    # --- PATH B2: REASONING & RAG (LLAMA) ---
    "What should I try for a romantic dinner?",
    "I'm feeling very hungry, suggest something heavy.",
    "What is the difference between Achar Gosht and Ranjha Gosht?",
    "Recommend a dessert that isn't too sweet.",
    "Give me something popular from the menu.",
    "I like spicy food, what's your best recommendation?",
    "Suggest a pairing for the Lamb Ribs.",
    
    # --- MULTI-INTENT & MEMORY ---
    "Hi, suggest a starter and then add it to my cart.",
    "Tell me more about the Mixed Grill.",
    "How much was that again?",
    "Add it to my cart please.",
]

def run_tests():
    print(f"Starting Rigorous Testing with {len(prompts)} prompts...\n")
    for i, prompt in enumerate(prompts):
        print(f"[{i+1}/{len(prompts)}] User: {prompt}")
        start_time = time.time()
        try:
            response = requests.post(
                BASE_URL,
                json={"message": prompt, "user_id": USER_ID},
                stream=True,
                timeout=45
            )
            
            full_response = ""
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        text = chunk.decode('utf-8')
                        full_response += text
                
                duration = time.time() - start_time
                print(f"Aureeq: {full_response.strip()[:150]}...") # Truncated for log
                print(f"Time: {duration:.2f}s")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception: {e}")
        
        print("-" * 50)
        time.sleep(1) # Small delay between requests

if __name__ == "__main__":
    run_tests()
