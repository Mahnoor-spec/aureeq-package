import requests
import json
import time

def send_msg(msg, user_id="test_routing"):
    url = "http://localhost:8001/chat"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json={"message": msg, "user_id": user_id}, headers=headers, stream=True, timeout=30)
        full_resp = ""
        for line in response.iter_lines():
            if line:
                try:
                    decoded = line.decode('utf-8')
                except:
                    decoded = str(line)
                full_resp += decoded
        return full_resp
    except Exception as e:
        return f"ERROR: {e}"

def verify_routing():
    print("--- STARTING ROUTING VERIFICATION ---")
    
    tests = [
        # 1. Hardcoded
        ("Who is Aureeq?", "AUREEQ", "Identity"),
        ("Where are you located?", "Hardcoded Address", "Location"),
        ("Contact number", "01234 5678", "Reservation/Contact"),
        ("Show me the full menu", "Available IYI Menu Items", "Menu Display"),
        ("Remove items from cart", "remove", "Remove Cart"),
        
        # 2. Phi-3 Specialist
        ("I am allergic to nuts", "Caution", "Allergy Check"),
        ("Describe the Baked Meat", "94.99", "Dish Description (Price Check)"),
        ("What is in the Turkish Tea", "black tea", "Ingredient/Desc Check"),
        
        # 3. Llama Generalist
        ("I am hungry", "lamb kebab", "General Recs (Soft Match)"),
        ("Suggest something spicy", "spicy", "Flavor Recs"),
        ("Who is the president?", "food selections", "Out of Scope (Blocked)")
    ]
    
    for query, expected_keyword, category in tests:
        print(f"\nTEST: [{category}] Query: '{query}'")
        resp = send_msg(query)
        # Check snippet for debug
        print(f"RESPONSE SNIPPET: {resp[:150]}...")
        
        if expected_keyword.lower() in resp.lower():
            print(f"[PASS] Found keyword '{expected_keyword}'")
        else:
            print(f"[FAIL] Expected '{expected_keyword}' not found.")
            
    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    print("Waiting 5s for server to settle...")
    time.sleep(5)
    verify_routing()
