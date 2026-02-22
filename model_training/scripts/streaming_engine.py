import json
import asyncio
import re
import traceback
import random
import os
from typing import AsyncGenerator
import router
import order_db
import hardcode_rules as rules
from rag_engine import RAGEngine
from phi_handler import PhiHandler
from llama_handler import LlamaHandler
from memory_manager import MemoryManager

class StreamingEngine:
    def __init__(self, rag: RAGEngine, memory: MemoryManager, phi: PhiHandler, llama: LlamaHandler):
        self.rag = rag
        self.memory = memory
        self.phi = phi
        self.llama = llama
        self.ingredients = ""
        self.rest_info = ""

    async def generate_response(self, user_id: str, message: str) -> AsyncGenerator[str, None]:
        # 1. CLASSIFY INTENT
        intent = router.classify_intent(message)
        print(f"Routing to: {intent}", flush=True)
        
        # 2. GET SESSION MEMORY (Read only for context)
        session = self.memory.get_session(user_id)
        history = session.get_history()
        
        full_response = ""

        # 3. HANDLE SPECIFIC INTENTS
        if intent == "HARDCODED_GREETING":
            full_response = rules.RESP_GREETING
        elif intent == "HARDCODED_IDENTITY":
            full_response = rules.RESP_IDENTITY
        elif intent == "HARDCODED_LOCATION":
            full_response = rules.RESP_LOCATION
        elif intent == "HARDCODED_RESERVATION":
            full_response = rules.RESP_RESERVATION
        elif intent == "HARDCODED_MENU_FULL":
            full_response = rules.RESP_FULL_MENU
        elif intent == "HARDCODED_MENU_STARTER":
            full_response = rules.RESP_STARTER_MENU
        elif intent == "HARDCODED_MENU_MAIN":
            full_response = rules.RESP_MAIN_MENU
        elif intent == "HARDCODED_MENU_DRINKS":
            full_response = rules.RESP_DRINKS_MENU
        elif intent == "HARDCODED_MENU_DESSERT":
            full_response = rules.RESP_DESSERTS_MENU
        elif intent == "HARDCODED_MENU_SEARCH":
            keywords = ["lamb", "chicken", "beef", "prawn", "vegetarian", "veg", "vegan"]
            target = next((k for k in keywords if k in message.lower()), "food")
            matches = [item for item in self.phi.menu_data if target in item['name'].lower() or target in item.get('description', '').lower()]
            if matches:
                resp = f"Here are our {target.capitalize()} options from across the menu:\n\n"
                cats = {}
                for m in matches:
                    c = m.get('category', 'Others')
                    if c not in cats: cats[c] = []
                    cats[c].append(m)
                for cat, items in cats.items():
                    resp += f"{cat.upper()}\n"
                    for i in items:
                        price = "94.99" if "baked meat" in i['name'].lower() else i['price']
                        resp += f"• {i['name']} (£{price})\n"
                    resp += "\n"
                resp += "Would you like to try any of these?"
                full_response = resp
            else:
                full_response = f"I'm sorry, I couldn't find any specific {target} options right now. Would you like to see our full menu instead?"
        elif intent == "HARDCODED_REMOVE_CART":
             item_matches = self.phi.find_items_fuzzy(message)
             if item_matches:
                 item = item_matches[0]
                 price = "94.99" if "baked meat" in item['name'].lower() else item['price']
                 wp_id = item.get('wp_id', item.get('id', ''))
                 # Format: [REMOVE: Name | Price | WP_ID]
                 full_response = rules.RESP_REMOVE_FROM_CART_SUCCESS.format(name=item['name'], price=price) + f" [REMOVE: {item['name']} | {price} | {wp_id}]"
             else:
                 full_response = "I'm not sure which item you want to remove. Could you say the name exactly as it appears on the menu?"
        elif intent == "HARDCODED_CART":
            if any(k in message.lower() for k in ["checkout", "pay", "buy now"]):
                 full_response = rules.RESP_CHECKOUT
            else:
                item_matches = self.phi.find_items_fuzzy(message)
                if item_matches:
                    item = item_matches[0]
                    order_db.save_order(user_id, [item['name']])
                    price = "94.99" if "baked meat" in item['name'].lower() else item['price']
                    wp_id = item.get('wp_id', item.get('id', ''))
                    # Format: [ORDER: Name | Price | WP_ID]
                    full_response = rules.RESP_ADD_TO_CART_SUCCESS.format(name=item['name'], price=price) + f" [ORDER: {item['name']} | {price} | {wp_id}]"
                else:
                    full_response = rules.RESP_ADD_TO_CART_FAIL

        if full_response:
            yield full_response
            return

        # --- DEFAULT / RAG / FOOD REASONING (LLAMA) ---
        if intent in ["LLAMA_RAG", "LLAMA_INTERACTIVE_GADGET"]:
            is_gadget = (intent == "LLAMA_INTERACTIVE_GADGET")
            menu_context = []
            style_example = ""
            
            # 1. Detect if it's a full menu request
            msg_lc = message.lower()
            is_full_menu = any(re.search(rf"\b{re.escape(x)}\b", msg_lc) for x in rules.MENU_QUERY_KEYWORDS)
            
            try:
                if is_full_menu:
                    menu_context = self.phi.menu_data 
                else:
                    detected_cats = []
                    for key, cats in rules.CATEGORY_MAP.items():
                        if re.search(rf"\b{re.escape(key)}\b", msg_lc):
                            detected_cats.extend(cats)
                    if detected_cats:
                        menu_context = [it for it in self.phi.menu_data if it.get('category') in detected_cats]
                    if not menu_context:
                        menu_context, style_example = await asyncio.gather(
                            self.rag.search_menu(message, k=10),
                            self.rag.search_examples(message)
                        )
            except Exception as e:
                print(f"RAG Error: {e}")
            
            direct_matches = self.phi.find_items_fuzzy(message)
            if direct_matches:
                dm = direct_matches[0]
                menu_context = [item for item in menu_context if item['name'] != dm['name']]
                menu_context.insert(0, dm)

            last_order = order_db.get_last_order(user_id)
            order_history_context = ""
            if last_order and len(history) < 2:
                order_history_context = f"THE USER PREVIOUSLY ORDERED: {last_order}. Mention this warmly in your greeting."

            if len(menu_context) < 3:
                for cat_name in ["Drinks", "Desserts", "Lamb/ Beef"]:
                    extra_items = [it for it in self.phi.menu_data if it.get('category') == cat_name]
                    if extra_items: menu_context.append(random.choice(extra_items))

            full_rest_context = (
                f"RESTAURANT KNOWLEDGE (IYI Dining):\n{getattr(self, 'rest_info', '')}\n\n"
                f"INGREDIENTS/ALLERGIES:\n{getattr(self, 'ingredients', '')}\n\n"
                f"{order_history_context}"
            )

            try:
                has_content = False
                async for chunk in self.llama.handle(
                    message, history, menu_context, style_example, full_rest_context, is_gadget_query=is_gadget
                ):
                    yield chunk
                    has_content = True
            
                if not has_content:
                    yield rules.RESP_FALLBACK_RECOMMENDATION

            except Exception as e:
                print(f"Llama Stream Failed: {e}")
                yield rules.RESP_FALLBACK_RECOMMENDATION
            return

    async def refresh_data(self):
        print("Refreshing all data layers...")
        try:
            await self.rag.init_menu() # Re-embed everything
        except Exception as e:
            print(f"Refresh Error: {e}")
        self.phi.menu_data = self.rag.menu_data
        self.llama.menu_data = self.rag.menu_data
        print("All layers refreshed (partial or full).")

    def save_to_memory(self, user_id: str, user_q: str, ai_a: str):
        session = self.memory.get_session(user_id)
        session.add_user_message(user_q)
        session.add_ai_message(ai_a)
