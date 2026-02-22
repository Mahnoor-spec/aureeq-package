import json
import httpx
import traceback
import re
from typing import List, Dict, Optional, AsyncGenerator

class PhiHandler:
    def __init__(self, ollama_url: str, model: str, menu_data: List[Dict]):
        self.ollama_url = ollama_url
        self.model = model
        self.menu_data = menu_data
        # Disable proxies to avoid localhost connection issues
        self.http_client = httpx.AsyncClient(timeout=30.0, trust_env=False)

    def find_items_fuzzy(self, query: str) -> List[Dict]:
        """Finds all items that match words in the query."""
        import re
        query_clean = re.sub(r'[^\w\s]', '', query.lower())
        filler_words = {"offer", "serve", "available", "recommend", "dish", "items", "menu", "description", "price", "ingredients", "what", "have"}
        words = [w for w in query_clean.split() if len(w) > 3 and w not in filler_words]
        
        matches = []
        for item in self.menu_data:
            score = 0
            item_str = (item['name'] + " " + item.get('description', '')).lower()
            
            # Name match (high score)
            if item['name'].lower() in query_clean:
                score += 5
            
            # Word match
            for w in words:
                if w in item_str:
                    score += 1
            
            if score > 0:
                matches.append((score, item))
        
        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches]

    def check_allergy(self, query: str) -> str:
        """
        Parses query for allergens and returns advice.
        """
        query_lower = query.lower()
        allergens = {
            "nut": ["nut", "almond", "pistachio", "walnut", "cashew", "peanut"],
            "dairy": ["milk", "cheese", "cream", "yogurt", "butter"],
            "gluten": ["bread", "flour", "wheat", "pasta"],
            "seafood": ["fish", "prawn", "shrimp", "salmon", "seabass", "calamari"],
            "egg": ["egg", "mayo"]
        }
        
        detected_allergen = None
        for key, synonyms in allergens.items():
            if any(syn in query_lower for syn in synonyms):
                detected_allergen = key
                break
        
        if not detected_allergen:
            return "" 
            
        # Find which dish user is interested in?
        relevant_dishes = self.find_items_fuzzy(query)
        
        # Case 1: Specific Dish Query ("Is the Baklava nut-free?")
        if relevant_dishes:
            dish = relevant_dishes[0]
            desc_lower = dish.get('description', '').lower()
            
            is_unsafe = False
            synonyms = allergens[detected_allergen]
            if any(syn in desc_lower for syn in synonyms) or any(syn in dish['name'].lower() for syn in synonyms):
                is_unsafe = True
                
            if is_unsafe:
                safe_alts = []
                for item in self.menu_data:
                    if item['category'] == dish['category'] and item['id'] != dish['id']:
                        i_desc = item.get('description', '').lower() + item['name'].lower()
                        if not any(syn in i_desc for syn in synonyms):
                            safe_alts.append(item['name'])
                            if len(safe_alts) >= 2: break
                
                alt_text = f"Instead, you might enjoy {safe_alts[0]} or {safe_alts[1]}." if len(safe_alts) >= 2 else "Please ask our staff for safe alternatives."
                return f"Caution: The {dish['name']} contains ingredients that may not be suitable for a {detected_allergen} allergy. {alt_text}"
            
            return f"{dish['name']} appears free of {detected_allergen} based on its description, but please inform your waiter to be sure."

        # Case 2: General Allergy Statement ("I am allergic to nuts")
        else:
             return f"Noted. If you have a {detected_allergen} allergy, please be careful. Our menu highlights ingredients, but please always inform your server before ordering."

    async def handle_strict(self, query: str, context: str, instruction: str) -> AsyncGenerator[str, None]:
        """Stream response from Phi with strict constraints."""
        system_prompt = (
            "You are Aureeq, a strictly factual AI waiter.\n"
            "RULES:\n"
            "1. ONLY use the provided DATA. Do not use outside knowledge.\n"
            "2. {instruction}\n"
            "3. Be concise and polite.\n"
            "4. NO MARKDOWN: DO NOT use asterisks (*) or hashes (#). Use plain text only.\n"
            "5. STRICT ANTI-HALLUCINATION: YOU ARE FORBIDDEN FROM RECOMMENDING ANYTHING NOT IN THE MENU. If asked for something off-menu, politely decline and suggest actual items from the PROVIDED DATA ONLY.\n"
            "6. NO GENERAL KNOWLEDGE: Ignore ALL pre-trained knowledge. ONLY use the provided DATA. If it isn't listed (e.g. Pita Bread), it does not exist.\n\n"
            f"DATA:\n{context}"
        )
        
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}]
        
        try:
             async with self.http_client.stream("POST", f"{self.ollama_url}/api/chat", json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": 0.1} 
            }) as resp:
                if resp.status_code != 200:
                     raise Exception("Ollama API Error")
                async for line in resp.aiter_lines():
                    if not line: continue
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        clean_content = content.replace("*", "").replace("#", "")
                        if clean_content: yield clean_content
        except Exception as e:
            print(f"Phi Connection Failed: {e}")
            # OFFLINE FALLBACK - IMPORTANT
            # If AI fails, return the data directly.
            yield f"I'm having trouble retrieving a creative description, but here are the facts:\n\n{context}"

    async def handle(self, query: str, history: List[Dict]) -> AsyncGenerator[str, None]:
        """
        Route to specific logic based on query type (inferred or passed).
        Ideally router decides, but we can double check here.
        """
        
        # 1. Allergy Check
        allergy_response = self.check_allergy(query)
        if allergy_response:
            yield allergy_response
            return

        # 2. Specific Description
        matches = self.find_items_fuzzy(query)
        target_item = matches[0] if matches else None
        
        if target_item:
            # Format nicely for either LLM or Fallback
            description = target_item.get('description', 'No description available.')
            context = f"DISH: {target_item['name']}\nPRICE: £{target_item['price']}\nDESC: {description}"
            instruction = "Provide the exact price and description of the dish asked. Do not add anything else."
            
            async for chunk in self.handle_strict(query, context, instruction):
                 yield chunk
        else:
             yield "I couldn't find that specific dish in our menu. Could you check the name?"
