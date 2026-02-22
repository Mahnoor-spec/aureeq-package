import requests
import json

def test_strictness():
    url = "http://localhost:8001/api/chat"
    
    # Test 1: Out of menu item
    print("\n--- Test 1: Out of menu item (Sushi) ---")
    payload = {"message": "Do you have sushi?", "user_id": "test_user"}
    resp = requests.post(url, json=payload, stream=True)
    full_resp = ""
    for chunk in resp.iter_lines():
        if chunk:
            full_resp += chunk.decode('utf-8')
    print(f"Response: {full_resp}")
    # Sushi is definitely not in the menu
    assert "sushi" not in full_resp.lower()
    
    # Test 2: General attribute search (Spicy)
    print("\n--- Test 2: General attribute search (Spicy) ---")
    payload = {"message": "Suggest some spicy food", "user_id": "test_user"}
    resp = requests.post(url, json=payload, stream=True)
    full_resp = ""
    for chunk in resp.iter_lines():
        if chunk:
            full_resp += chunk.decode('utf-8')
    print(f"Response: {full_resp}")
    # Verify it mentions real items like "Adana Kebab" and not made up ones
    # (Adana Kebab is in menu.json and is spicy)
    # Check for hallucination of "spicy prawn" or "wings" which are not there
    forbidden_hallucinations = ["prawn", "wings", "shrimp", "sushi", "tikka masala", "vindaloo"]
    for item in forbidden_hallucinations:
        assert item not in full_resp.lower()

if __name__ == "__main__":
    try:
        test_strictness()
        print("\nVerification SUCCESS: No hallucinations found!")
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
