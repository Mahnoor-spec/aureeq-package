import requests
import json
import time
import traceback

def test_system():
    url = "http://localhost:8001/chat"
    headers = {"Content-Type": "application/json"}
    
    # Test 1: Fallback / Recommendation (Hunger)
    print("\n--- Testing 'I am hungry' (Fallback/RAG Check) ---")
    data = {"message": "i am hungry", "user_id": "test_verification"}
    
    try:
        response = requests.post(url, json=data, stream=True, timeout=30)
        full_resp = ""
        for line in response.iter_lines():
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                except:
                     decoded_line = str(line)
                full_resp += decoded_line
        
        print(f"Response: {full_resp[:300]}...")
        
        if "Lamb Kebab Barg" in full_resp:
            print("[PASS] Recommendations provided (Signature or RAG).")
        else:
            print("[FAIL] No relevant recommendations found.")
            
        if "I apologize, but I couldn't find a matching dish in our menu" in full_resp:
            print("[FAIL] Old fallback message detected!")
        elif "I apologize, but I couldn't find an exact match" in full_resp:
            print("[INFO] New fallback message used.")

    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Pricing
    print("\n--- Testing 'Baked Meat' Pricing ---")
    data = {"message": "tell me about baked meat", "user_id": "test_verification"}
    try:
        response = requests.post(url, json=data, stream=True, timeout=30)
        full_resp = ""
        for line in response.iter_lines():
             if line:
                try:
                    decoded_line = line.decode('utf-8')
                except:
                     decoded_line = str(line)
                full_resp += decoded_line
                
        if "94.99" in full_resp:
            print("[PASS] Correct Price 94.99 found.")
        else:
            print("[FAIL] Incorrect price or item not found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Waiting for server...")
    time.sleep(5)
    test_system()
