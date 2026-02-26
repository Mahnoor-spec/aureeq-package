import re

# ==================================================================================
# SYSTEM PROMPTS
# ==================================================================================

SYSTEM_PROMPT_OPENAI = """You are Aureeq, the professional Sales Agent for IYI Dining. 

### THE GOLDEN RULE OF TRUTH:
- **STRICT GROUNDING**: You are ONLY allowed to suggest dishes that are explicitly listed in the "AVAILABLE MENU" provided below.
- **NO HALLUCINATION**: If a dish name or price is not in the list, it does NOT exist. Do not invent "Platters", "Combos", or "Deals" unless they are in the menu.
- **EXACT PRICES**: You must use the exact price listed in the menu. Never round up, round down, or guess.
- **DENIAL**: If the user asks for something we don't have, or asks for a recommendation you can't satisfy with the menu, admit you don't have it and suggest the CLOSEST match from the ACTUAL menu.

Follow these 6 core rules:
1. RECOMMENDATION: Suggest items based on user input, but ONLY from the provided menu list.
2. OFF-MENU FOOD: Deny and pivot to a related menu item.
3. OUT OF CONTEXT: Deny politely and pivot to any menu item.
4. DIVERSITY: Suggest a mix of courses (Starter, Main, Drink, Dessert).
5. HIERARCHY: Mention the section (e.g., "From our BBQ section...").
6. STYLE: Precise, professional, welcoming. NO markdown (*, #, bullet points). Use £ for currency.

{global_context}
{style_example}
{context_item}
"""

# ==================================================================================
# INTENT CLASSIFICATION KEYWORDS & PATTERNS
# ==================================================================================

# 0. Add/Remove Cart keywords
ADD_TO_CART_KEYWORDS = ["add to cart", "add to my order"]
ADD_TO_CART_PAIRS = [("add", "cart"), ("buy", "order"), ("want", "order"), ("have", "order")]

REMOVE_FROM_CART_KEYWORDS = ["remove from cart", "delete from cart", "take out of cart", "cancel order", "remove item", "delete item"]
REMOVE_FROM_CART_PAIRS = [("remove", "cart"), ("delete", "cart"), ("cancel", "order"), ("take", "cart")]

# 0.5 Out-of-menu food request indicators
FOOD_REQUEST_INDICATORS = ["buy", "order", "can i get", "do you have", "pizza", "burger", "pasta"]
BYPASS_APOLOGY_KEYWORDS = ["spicy", "sweet", "flavor", "recommend", "suggestion", "best", "popular", "halal", "vegetarian", "vegan", "light", "heavy", "something", "anything", "quick"]

# 1. Greeting pattern
GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "good morning", "good evening", "how are you", "hi there", "hello there"]
GREETING_RE = r"\b(hi|hello|hey|greetings|good morning|good evening)\b"

# 1.5 Restaurant query keywords
IDENTITY_KEYWORDS = ["restaurant name", "who are you", "where am i", "what place is this", "your name", "place name", "shop name", "hotel name", "who is aureeq", "are you aureeq"]

# 1.8 Reservation/Location/Contact keywords
RESERVATION_KEYWORDS = ["reservation", "reserv", "reserve", "book", "table", "contact", "call", "email", "timing", "open", "close", "frontdesk", "front desk", "phone", "number"]
LOCATION_KEYWORDS = ["address", "location", "located", "where are you", "how can i find you", "map", "directions"]

# 1.9 Thank you / Goodbye
THANK_YOU_KEYWORDS = ["thank you", "thanks", "thx", "appreciate", "grateful"]
GOODBYE_KEYWORDS = ["bye", "goodbye", "see you", "later", "cya"]

# 2. Menu keyword checks
MENU_TYPO_KEYWORDS = ["meu", "mnue", "list"]
ADD_TO_CART_KEYWORDS = ["add", "order", "buy", "put in", "send to", "get me", "want to buy", "add to cart", "add to order"]
REMOVE_FROM_CART_KEYWORDS = ["remove", "delete", "take out", "cancel", "don't want", "remove from cart"]
# Updated: Removed generic terms like "eat", "hungry", "food", "selection", "choice", "anything" 
# to allow these to fall through to Llama for interactive, persuasive selling.
MENU_QUERY_KEYWORDS = ["menu", "list", "full menu", "part of the menu", "menu dish prices", "price list", "available dishes", "available"]

# 2.5 Non-food stop topics (Gadgets / Interactive Dashboard Trigger)
NON_FOOD_GADGETS = [
    "iphone", "samsung", "galaxy", "laptop", "computer", "macbook", "ipad", "tablet", "phone", "mobile", 
    "camera", "headphones", "watch", "smartwatch", "tv", "television", "console", "ps5", "xbox", "nintendo",
    "car", "bike", "cycle", "tesla", "bmw", "mercedes", "audi", "toyota", "honda"
]

STOP_TOPICS = [
    "politics", "crypto", "sports", "news", "coding", "programming", "code", "math", 
    "bitcoin", "money", "currency", "gold", "finance", "stock", "shares", "trading", "investment", "invest", "business",
    "science", "space", "history", "geography", "system prompt", "ignore instructions", "previous instructions", "hacker", "jailbreak",
    "president", "minister", "joke", "riddle", "story", "2+2", "sum", "calculate", "plus", "minus", "divided", "multiplied"
]

# 2.6 Out-of-menu blocked keywords
BLOCKED_FOOD = [
    "pizza", "burger", "pasta", "wine", "beer", "alcohol", "pita bread", "naan", "tikka masala", "butter chicken", "sushi", "tacos",
    "pepperoni", "steak", "burrito", "ramen", 
    "waffle", "fried chicken", "fish and chips", "coke", "coca cola", "fries", "hot dog", "pancake", "donut",
    "sandwich", "wrap", "curry", "noodle", "rice bowl", "dim sum", "dumpling", "tapas", "dimsum"
]

# --- EXTENDED FOOD DOMAIN KEYWORDS ---

CORE_FOOD_KEYWORDS = [
    "food", "dish", "meal", "eat", "eating", "dinner", "lunch", "breakfast", "brunch", 
    "starter", "main course", "dessert", "appetizer", "side", "snack", "plate", 
    "cuisine", "flavor", "taste", "savory", "sweet", "spicy", "mild", "crispy", 
    "grilled", "fried", "baked", "steamed", "roasted"
]

HUNGER_TRIGGERS = [
    "hungry", "starving", "famished", "craving", "really want", "in the mood for", 
    "feel like eating", "feel like something", "appetite", "urge", "longing for", 
    "dying for", "need food", "need something", "something tasty", "something spicy", 
    "comfort food", "cheat meal", "treat myself", "indulge"
]

RESTAURANT_RELATED_KEYWORDS = [
    "restaurant", "dine", "dining", "eat out", "table", "reservation", "book a table", 
    "order", "place order", "menu", "chef", "kitchen", "serve", "served", "special", 
    "today's special", "recommend", "suggest", "what do you have", "what's good", 
    "best seller", "popular", "signature dish"
]

PROTEIN_DISH_TYPE_TRIGGERS = [
    "chicken", "beef", "steak", "lamb", "fish", "salmon", "prawn", "shrimp", "seafood", 
    "pasta", "rice", "burger", "pizza", "curry", "noodles", "soup", "salad", "wrap", 
    "sandwich", "grill", "bbq"
]

TASTE_PREFERENCE_WORDS = [
    "spicy", "extra spicy", "mild", "not spicy", "sweet", "savory", "creamy", "smoky", 
    "juicy", "tender", "crispy", "crunchy", "rich", "light", "heavy", "fresh", "hot", "warm"
]

DRINK_RELATED_KEYWORDS = [
    "drink", "beverage", "juice", "mocktail", "cocktail", "soda", "water", 
    "tea", "coffee", "shake", "smoothie"
]

PRICE_MENU_TRIGGERS = [
    "price", "cost", "how much", "how much is", "ingredients", "what's in", 
    "made of", "calories", "portion", "size", "location", "address", "where are you"
]

SOFT_IMPLICIT_FOOD_SIGNALS = [
    "date night", "family dinner", "friends gathering", "celebration", "birthday dinner", 
    "romantic dinner", "quick bite", "late night food", "midnight craving", 
    "after gym", "cheat day", "movie night", "game night"
]

ALL_FOOD_KEYWORDS = list(set(
    CORE_FOOD_KEYWORDS + HUNGER_TRIGGERS + RESTAURANT_RELATED_KEYWORDS + 
    PROTEIN_DISH_TYPE_TRIGGERS + TASTE_PREFERENCE_WORDS + DRINK_RELATED_KEYWORDS + 
    PRICE_MENU_TRIGGERS + SOFT_IMPLICIT_FOOD_SIGNALS + FOOD_REQUEST_INDICATORS + MENU_QUERY_KEYWORDS
))

# 8. Category Mapping (User Query -> Menu Categories)
CATEGORY_MAP = {
    "starter": ["Cold Mezze", "Hot Mezze", "Salad"],
    "mezze": ["Cold Mezze", "Hot Mezze"],
    "salad": ["Salad"],
    "hot starter": ["Hot Mezze"],
    "cold starter": ["Cold Mezze"],
    "appetizer": ["Cold Mezze", "Hot Mezze", "Salad"],
    "main": ["Lamb/ Beef", "Chicken", "Seafood", "IYI Special", "Baked Meat"],
    "bbq": ["Lamb/ Beef", "Chicken", "Seafood"],
    "grill": ["Lamb/ Beef", "Chicken", "Seafood"],
    "special": ["IYI Special"],
    "baked": ["Baked Meat"],
    "dessert": ["Desserts"],
    "sweet": ["Desserts"],
    "apple": ["Drinks"],
    "vegetarian": ["Vegetarian"],
    "vegan": ["Vegetarian"],
    "meat-free": ["Vegetarian"]
}

# ==================================================================================
# DETERMINISTIC RESPONSES
# ==================================================================================

RESP_IDENTITY = "I am Aureeq, your dedicated professional Sales Agent for IYI Dining. I'm here to help you explore our exquisite menu and ensure you have an unforgettable dining experience. What can I suggest for you today?"
RESP_IDENTITY_AR = "أنا AUREEQ، وكيل المبيعات المحترف المخصص لك في IYI Dining. أنا هنا لمساعدتك في استكشاف قائمتنا الرائعة وضمان حصولك على تجربة طعام لا تُنسى. ماذا يمكنني أن أقترح لك اليوم؟"

RESP_GREETING = "Hello! Welcome to IYI Dining. I'm Aureeq, your dedicated Sales Agent. How can I delight you today?"
RESP_GREETING_AR = "مرحباً! أهلاً بك في IYI Dining. أنا AUREEQ، وكيل المبيعات المخصص لك. كيف يمكنني إسعادك اليوم؟"

RESP_RESERVATION = (
    "I can assist you with making a reservation at our restaurant. For reservations, "
    "please call +44 20 1234 5678 or email info@iyirestaurant.co.uk.\n\n"
    "[Follow @iyi_dining on Instagram](https://www.instagram.com/iyi_dining) to stay updated."
)
RESP_RESERVATION_AR = (
    "يمكنني مساعدتك في إجراء حجز في مطعمنا. للحجوزات، "
    "يرجى الاتصال على +44 20 1234 5678 أو إرسال بريد إلكتروني إلى info@iyirestaurant.co.uk.\n\n"
    "[تابع @iyi_dining على انستغرام](https://www.instagram.com/iyi_dining) لتبقى على اطلاع."
)

RESP_LOCATION = (
    "We are located at 123 IYI Street, London, W1 2AB.\n\n"
    "[Follow @iyi_dining on Instagram](https://www.instagram.com/iyi_dining) to stay updated."
)
RESP_LOCATION_AR = (
    "نحن موجودون في 123 شارع IYI، لندن، W1 2AB.\n\n"
    "[تابع @iyi_dining على انستغرام](https://www.instagram.com/iyi_dining) لتبقى على اطلاع."
)

RESP_THANK_YOU = "You are most welcome! It is my pleasure to assist you. Is there anything else from our menu I can tell you about?"
RESP_THANK_YOU_AR = "على الرحب والسعة! إنه لمن دواعي سروري مساعدتك. هل هناك أي شيء آخر من قائمتنا يمكنني إخبارك عنه؟"

RESP_GOODBYE = "Goodbye! It was a pleasure chatting with you. We hope to see you soon at IYI Dining. Have a wonderful day!"
RESP_GOODBYE_AR = "وداعاً! لقد كان من دواعي سروري الدردشة معك. نأمل أن نراك قريباً في IYI Dining. أتمنى لك يوماً رائعاً!"

RESP_NON_FOOD = "Sorry, I am only able to help you with your food selections."
RESP_NON_FOOD_AR = "عذراً، يمكنني فقط مساعدتك في اختيارات الطعام الخاصة بك."

# For Gadgets - This uses a placeholder that the Llama handler will need to fill
RESP_GADGET_TEMPLATE = "Sorry I don't offer this but you can enjoy our {dish_name} while using that {gadget_name}."

RESP_ADD_TO_CART_SUCCESS = "Excellent choice! I've added {name} to your cart. [ORDER: {name} | {price}]"
RESP_ADD_TO_CART_SUCCESS_AR = "اختيار رائع! لقد أضفت {name} إلى سلة التسوق الخاصة بك. [ORDER: {name} | {price}]"

RESP_REMOVE_FROM_CART_SUCCESS = "No problem at all. I've removed {name} from your cart. [REMOVE: {name} | {price}]"
RESP_REMOVE_FROM_CART_SUCCESS_AR = "لا توجد مشكلة على الإطلاق. لقد قمت بإزالة {name} من سلتك. [REMOVE: {name} | {price}]"

RESP_ADD_TO_CART_FAIL = "I'd love to add that for you, but I'm not sure which item you mean. Could you say the name exactly as it appears on the menu?"
RESP_ADD_TO_CART_FAIL_AR = "أود إضافة ذلك لك، لكني لست متأكداً من العنصر الذي تقصده. هل يمكنك قول الاسم تماماً كما يظهر في القائمة؟"

RESP_CHECKOUT = "Certainly! You can proceed to checkout by clicking the 'Checkout' button in your shopping cart. Would you like anything else before you go?"
RESP_CHECKOUT_AR = "بالتأكيد! يمكنك المتابعة إلى الدفع بالضغط على زر 'الدفع' في سلة التسوق الخاصة بك. هل تود أي شيء آخر قبل أن تذهب؟"

# Strict Menu Display Enforcer
RESP_MENU_HEADER = "Here is our full menu:" 

# Updated to look premium but use strict JSON data
RESP_DISH_DETAILS = "{name} (£{price}) is a customer favorite.\\n\\n{description}"
RESP_DISH_NOT_FOUND = "I couldn't find details for that specific dish. Please check the menu list."
RESP_OUT_OF_MENU_APOLOGY = "Sorry, we don't offer that at IYI Dining right now, but you can enjoy our other options. I highly recommend our {name} ({price}), which is a guest favorite!\\n\\n"

RESP_FALLBACK_RECOMMENDATION = (
    "I apologize, but I couldn't find an exact match for that in our menu. However, you can't go wrong with our guest favorites! "
    "I highly recommend our Lamb Kebab Barg (£19.99), Ranjha Gosht (£19.99), or our signature IYI Special Mix Grill (£34.99). "
    "Would you like to try one of these, or should I show you the full menu?"
)

RESP_SIGNATURE_OVERVIEW = (
    "I apologize, but I couldn't find a matching dish. Here are some of our highly recommended signature dishes that our guests love:\\n\\n"
    "• Lamb Kebab Barg (£19.99)\\n"
    "• Ranjha Gosht (£19.99)\\n"
    "• Grilled Sea Bass (£18.99)\\n"
    "• IYI Special Mix Grill (£34.99)\\n"
    "• Persian Saffron Rice (£4.99)\\n\\n"
    "Would you like to try one of these, or should I show you the full menu?"
)

RESP_CRITICAL_ERROR = "I apologize, but I encountered an internal error. Please try again."
RESP_TIMEOUT_FALLBACK = "I apologize, but I am momentarily distracted. Please ask again."

# --- FALLBACK SIGNATURE DISHES ---
SIGNATURE_DISH_NAMES = [
    "Lamb Kebab Barg",
    "Ranjha Gosht",
    "Grilled Sea Bass",
    "IYI Special Mix Grill",
    "Persian Saffron Rice"
]

# --- HARDCODED MENU DISPLAYS ---
RESP_FULL_MENU_AR = (
    "قائمة طعامنا الكاملة في IYI Dining هي مجموعة مختارة من النكهات الأصيلة:\n\n"
    "المقبلات الباردة\n"
    "• حمص بالدجاج (5.00 جنيه إسترليني) - حمص مع دجاج سوتيه.\n"
    "• حمص بالأفوكادو واللحم (8.99 جنيه إسترليني) - حمص بالأفوكادو مع لحم مطهو ببطء.\n"
    "• حمص بالأفوكادو والدجاج (7.00 جنيه إسترليني) - حمص بالأفوكادو مع دجاج متبل.\n"
    "• حمص بالأفوكادو سادة (7.00 جنيه إسترليني) - مهروس الحمص والأفوكادو الناعم.\n"
    "• حمص سادة (6.00 جنيه إسترليني) - مهروس الحمص والطحينة الناعم.\n"
    "• حمص باللحم (9.99 جنيه إسترليني) - حمص مع لحم عطري.\n\n"
    "المقبلات الساخنة\n"
    "• شوربة الفطر الكريمة (8.00 جنيه إسترليني) - فطر مخملي ناعم.\n"
    "• كبة (19.99 جنيه إسترليني) - لحم متبل وبرغل.\n"
    "• شوربة الدجاج (7.99 جنيه إسترليني) - مرق صافي ولذيذ.\n"
    "• شوربة العدس (9.99 جنيه إسترليني) - عدس أحمر مطهو ببطء على الطريقة التقليدية.\n"
    "• لحم بعجين (6.99 جنيه إسترليني) - خبز مفرود رقيق مع لحم مفروم وأعشاب.\n"
    "• أجنحة دجاج (15.99 جنيه إسترليني) - أجنحة متبلة ومشوية على الفحم.\n"
    "• فلافل (9.99 جنيه إسترليني) - كرات الحمص المقلية الذهبية.\n\n"
    "السلطات\n"
    "• تبولة (7.99 جنيه إسترليني) - سلطة البقدونس والنعناع والبرغل.\n"
    "• سلطة الزبادي والخيار (6.99 جنيه إسترليني) - زبادي منعش مع الثوم.\n"
    "• فتوش (9.99 جنيه إسترليني) - خضروات طازجة مع خبز محمص.\n\n"
    "الأطباق الرئيسية (المشاوي والكاتي)\n"
    "• ريش غنم (25.99 جنيه إسترليني) - ريش طرية مطهوة ببطء.\n"
    "• تيكا الروبيان (25.99 جنيه إسترليني) - روبيان متبل ومشوي.\n"
    "• كباب دجاج بارج (15.99 جنيه إسترليني) - صدر دجاج متبل.\n"
    "• كباب لحم بارج (19.99 جنيه إسترليني) - مكعبات لحم غنم مشوية ممتازة.\n"
    "• ريش غنم (25.99 جنيه إسترليني) - ريش غنم ممتازة متبلة ومشوية.\n"
    "• كباب أضنة دجاج (15.99 جنيه إسترليني) - دجاج مفروم مع بهارات.\n"
    "• كباب أضنة لحم (19.99 جنيه إسترليني) - لحم مفروم مع بهارات عطرية.\n"
    "• شيش كباب دجاج (15.99 جنيه إسترليني) - صدر دجاج بأسياخ مع الحمضيات والأعشاب.\n"
    "• شيش كباب لحم (19.99 جنيه إسترليني) - لحم مقطع يدوياً ببهارات عطرية.\n"
    "• تشابلي كباب (9.99 جنيه إسترليني) - قرص لحم مفروم بالأعشاب التقليدية.\n"
    "• رانجا جوشت (19.99 جنيه إسترليني) - كاري لحم متبل وعطري.\n"
    "• بانو بولاو (15.99 جنيه إسترليني) - أرز ولحم عطري.\n"
    "• لحم مخبوز (94.99 جنيه إسترليني) - لحم مخبوز ببطء مع نكهات عطرية.\n\n"
    "الحلويات\n"
    "• بقلاوة (6.99 جنيه إسترليني) - جلاش فاخر مع مكسرات وقطر.\n"
    "• كنافة (6.99 جنيه إسترليني) - عجينة كنافة مع جبنة ذائبة وقطر.\n\n"
    "المشروبات\n"
    "• شاي تركي (3.50 جنيه إسترليني)، شاي إنجليزي (3.50 جنيه إسترليني)\n"
    "• كرك (4.00 جنيه إسترليني)، كابوتشينو (4.50 جنيه إسترليني)\n"
    "• موكتيلات (6.99 جنيه إسترليني): كريستال بلو، تروبي كولادا، روبي مينت، ميلون تويست، ليموناضة.\n\n"
    "هل تود أن أضيف أي شيء إلى سلة التسوق الخاصة بك؟"
)

RESP_FULL_MENU = (
    "Our full menu at IYI Dining is a curated selection of authentic flavours:\n\n"
    "COLD MEZZE\n"
    "• Chicken Hummus (£5.00) - Hummus with sautéed chicken.\n"
    "• Lamb Avocado Hummus (£8.99) - Avocado hummus with slow-cooked lamb.\n"
    "• Chicken Avocado Hummus (£7.00) - Avocado hummus with spiced chicken.\n"
    "• Plain Avocado Hummus (£7.00) - Smooth avocado and chickpea purée.\n"
    "• Plain Hummus (£6.00) - Silken chickpea and tahini purée.\n"
    "• Lamb Hummus (£9.99) - Hummus with aromatic lamb.\n\n"
    "HOT MEZZE\n"
    "• Creamy Mushroom Soup (£8.00) - Silky mushroom velouté.\n"
    "• Kibbeh (£19.99) - Spiced meat and bulgur wheat.\n"
    "• Chicken Soup (£7.99) - Clear and flavourful broth.\n"
    "• Lentil Soup (£9.99) - Traditional slow-cooked red lentils.\n"
    "• Lahmacun (£6.99) - Thin flatbread with minced meat and herbs.\n"
    "• Chicken Wings (£15.99) - Charcoal-grilled marinated wings.\n"
    "• Falafel (£9.99) - Golden-fried chickpea fritters.\n\n"
    "SALADS\n"
    "• Tabbouleh (£7.99) - Parsley, mint, and bulgur salad.\n"
    "• Yogurt and Cucumber Salad (£6.99) - Refreshing yoghurt with garlic.\n"
    "• Fattoush (£9.99) - Crisp vegetables with toasted flatbread.\n"
    "• Lamb Ribs (£25.99) - Slow-cooked succulent ribs.\n"
    "• Prawns Tikka (£25.99) - Marinated and grilled prawns.\n"
    "• Chicken Kebab Barg (£15.99) - Marinated chicken breast.\n"
    "• Lamb Kebab Barg (£19.99) - Premium grilled lamb cubes.\n"
    "• Lamb Chops (£25.99) - Seasoned and grilled premium chops.\n"
    "• Chicken Adana Kebab (£15.99) - Minced chicken with spices.\n"
    "• Lamb Adana Kebab (£19.99) - Minced lamb with aromatic spices.\n"
    "• Chicken Shish Kebab (£15.99) - Skewered breast in citrus and herbs.\n"
    "• Lamb Shish Kebab (£19.99) - Hand-cut lamb in fragrant spices.\n"
    "• Chapli Kebab (£9.99) - Traditional herbal minced meat patty.\n"
    "• Ranjha Gosht (£19.99) - Rich and aromatic lamb curry.\n"
    "• Bannu Pulao (£15.99) - Fragrant meat and rice pulao.\n"
    "• Baked Meat (£94.99) - Tender slow-baked aromatics.\n\n"
    "DESSERTS\n"
    "• Baklava (£6.99) - Fine filo with nuts and syrup.\n"
    "• Künefe (£6.99) - Pastry with molten cheese and syrup.\n\n"
    "DRINKS\n"
    "• Turkish Tea (£3.50), English Tea (£3.50)\n"
    "• Karak Chai (£4.00), Cappuccino (£4.50)\n"
    "• Mocktails (£6.99): Crystal Blue, Tropi Colada, Ruby Mint, Melon Twist, Lemonade.\n\n"
    "Would you like me to add anything to your cart?"
)

RESP_STARTER_MENU_AR = (
    "مقبلاتنا مثالية للمشاركة. إليك القائمة الكاملة:\n\n"
    "المقبلات الباردة\n"
    "• حمص بالدجاج (5.00 جنيه إسترليني)، حمص بالأفوكادو واللحم (8.99 جنيه إسترليني)، حمص بالأفوكادو والدجاج (7.00 جنيه إسترليني)\n"
    "• حمص بالأفوكادو سادة (7.00 جنيه إسترليني)، حمص سادة (6.00 جنيه إسترليني)، حمص باللحم (9.99 جنيه إسترليني)\n\n"
    "المقبلات الساخنة\n"
    "• شوربة الفطر (8.00 جنيه إسترليني)، كبة (19.99 جنيه إسترليني)، شوربة الدجاج (7.99 جنيه إسترليني)، شوربة العدس (9.99 جنيه إسترليني)\n"
    "• لحم بعجين (6.99 جنيه إسترليني)، أجنحة دجاج (15.99 جنيه إسترليني)، فلافل (9.99 جنيه إسترليني)\n\n"
    "السلطات\n"
    "• تبولة (7.99 جنيه إسترليني)، سلطة الزبادي والخيار (6.99 جنيه إسترليني)، فتوش (9.99 جنيه إسترليني)\n\n"
    "هل أجهز لك أحد هذه الأطباق؟"
)

RESP_STARTER_MENU = (
    "Our Starters are perfect for sharing. Here is the complete list:\n\n"
    "COLD MEZZE\n"
    "• Chicken Hummus (£5.00), Lamb Avocado Hummus (£8.99), Chicken Avocado Hummus (£7.00)\n"
    "• Plain Avocado Hummus (£7.00), Plain Hummus (£6.00), Lamb Hummus (£9.99)\n\n"
    "HOT MEZZE\n"
    "• Mushroom Soup (£8.00), Kibbeh (£19.99), Chicken Soup (£7.99), Lentil Soup (£9.99)\n"
    "• Lahmacun (£6.99), Chicken Wings (£15.99), Falafel (£9.99)\n\n"
    "SALADS\n"
    "• Tabbouleh (£7.99), Yogurt and Cucumber Salad (£6.99), Fattoush (£9.99)\n\n"
    "Shall I prepare one of these for you?"
)

# (Mains, Drinks, Desserts sections simplified for logic flow but complete in data)
RESP_MAIN_MENU_AR = "تشمل تشكيلة الأطباق الرئيسية لدينا مشاوينا الشهيرة (ريش غنم، قطع لحم، شيش، أضنة، وشيش دجاج، أضنة، أجنحة) وإضافات IYI الخاصة مثل رانجا جوشت وبانو بولاو، ولحمنا المخبوز الممتاز. تتراوح الأسعار من 9.99 جنيه إسترليني إلى 94.99 جنيه إسترليني. أي منها تود أن أصفه لك؟"
RESP_MAIN_MENU = "Our main course selection includes our famous Grills (Lamb Ribs, Chops, Shish, Adana and Chicken Shish, Adana, Wings) and IYI Specials like Ranjha Gosht and Bannu Pulao, and our premium Baked Meat. Prices range from £9.99 to £94.99. Which one shall I describe for you?"

RESP_DRINKS_MENU_AR = "نقدم مجموعة متنوعة من المشروبات بما في ذلك الشاي التركي (3.50 جنيه إسترليني)، الشاي الإنجليزي (3.50 جنيه إسترليني)، شاي الكرك (4.00 جنيه إسترليني)، الكابوتشينو (4.50 جنيه إسترليني)، ومجموعة من الموكتيلات المنعشة مثل كريستال بلو وروبي مينت مقابل (6.99 جنيه إسترليني). هل يمكنني اقتراح مشروب؟"
RESP_DRINKS_MENU = "We offer a variety of beverages including Turkish Tea (£3.50), English Tea (£3.50), Karak Chai (£4.00), Cappuccino (£4.50), and a selection of refreshing Mocktails like Crystal Blue and Ruby Mint for (£6.99). Can I suggest a drink?"

RESP_DESSERTS_MENU_AR = "اختم وجبتك بحلوياتنا التقليدية: البقلاوة (6.99 جنيه إسترليني) أو الكنافة الدافئة بالجبنة (6.99 جنيه إسترليني). كلاهما لذيذ للغاية!"
RESP_DESSERTS_MENU = "Finish your meal with our traditional desserts: Baklava (£6.99) or the warm, cheesy Künefe (£6.99). They are both delightful!"
