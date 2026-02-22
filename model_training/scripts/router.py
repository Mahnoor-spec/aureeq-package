import re
from typing import List, Tuple
import hardcode_rules as rules

def get_single_intent(msg: str) -> str:
    msg_lower = msg.lower()
    
    # ==============================================================================
    # 1. HARDCODED LOGISTICS & CART (Highest Priority)
    # ==============================================================================
    
    # Priority 1: Cart Actions (Must catch "add baklava" before it hits dessert)
    remove_patterns = [r"remove.*cart", r"delete.*cart", r"cancel.*order", r"take.*out"]
    if any(re.search(p, msg_lower) for p in remove_patterns) or any(k in msg_lower for k in rules.REMOVE_FROM_CART_KEYWORDS):
        return "HARDCODED_REMOVE_CART"

    add_patterns = [
        r"add\s+.*", r"order\s+.*", r"buy\s+.*", r"put\s+.*\s+in.*cart", 
        r"add.*this", r"order.*this", r"checkout", r"pay.*now"
    ]
    if any(re.search(p, msg_lower) for p in add_patterns) or any(k in msg_lower for k in rules.ADD_TO_CART_KEYWORDS):
        return "HARDCODED_CART"

    # Priority 2: Logistics (Greeting, Identity, Location, Reservation)
    if any(re.search(rf"\b{re.escape(x)}\b", msg_lower) for x in ["hi", "hello", "greeting", "hey", "how are you"]):
        return "HARDCODED_GREETING"
    
    if any(re.search(rf"\b{re.escape(x)}\b", msg_lower) for x in rules.IDENTITY_KEYWORDS):
        return "HARDCODED_IDENTITY"

    if any(re.search(rf"\b{re.escape(x)}\b", msg_lower) for x in rules.LOCATION_KEYWORDS):
        return "HARDCODED_LOCATION"
        
    if any(k in msg_lower for k in ["reserv", "book", "table", "contact", "call", "timing", "frontdesk"]):
        return "HARDCODED_RESERVATION"
    
    if re.search(rf"\bphone\b", msg_lower) or any(re.search(rf"\b{re.escape(x)}\b", msg_lower) for x in rules.RESERVATION_KEYWORDS):
        return "HARDCODED_RESERVATION"

    # Priority 3: Menu Displays (Slices and full menu)
    if any(k in msg_lower for k in ["lamb", "chicken", "beef", "prawn", "vegetarian", "veg", "vegan", "baklava", "chai"]):
        if any(m in msg_lower for m in ["option", "dish", "menu", "item", "food", "selection"]):
            return "HARDCODED_MENU_SEARCH"

    if any(re.search(rf"\b{re.escape(x)}\b", msg_lower) for x in ["full menu", "whole menu", "complete menu", "entire menu"]):
        return "HARDCODED_MENU_FULL"

    if any(k in msg_lower for k in ["starter", "appetizer", "mezze", "soup", "salad"]):
        return "HARDCODED_MENU_STARTER"
    if any(k in msg_lower for k in ["main", "grill", "special", "baked", "curry"]):
        return "HARDCODED_MENU_MAIN"
    if any(k in msg_lower for k in ["drink", "beverage", "tea", "chai", "mocktail", "lemonade"]):
        return "HARDCODED_MENU_DRINKS"
    if any(k in msg_lower for k in ["dessert", "sweet", "baklava", "kunefe"]):
        return "HARDCODED_MENU_DESSERT"

    if any(re.search(rf"\b{re.escape(x)}\b", msg_lower) for x in rules.MENU_QUERY_KEYWORDS):
        return "HARDCODED_MENU_FULL"

    # ==============================================================================
    # 2. LLAMA 3.1 NARRATIVE SALES (Fallthrough)
    # ==============================================================================
    print(f"DEBUG ROUTER: Falling back to LLAMA_RAG for: {msg_lower}", flush=True)
    return "LLAMA_RAG"

def classify_intent(msg: str) -> str:
    return get_single_intent(msg)
