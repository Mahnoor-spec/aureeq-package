import re
import hardcode_rules as rules

msg = "Why is it slow-cooked?".lower()

print(f"Testing message: {msg}")

# 1. 0.4 check
adv_list = ["ignore", "forget", "pretend", "act like", "as a ", "system prompt", "internal rules"]
for x in adv_list:
    if x in msg:
        print(f"Hit adversarial: {x}")

# 2. Stop Topics check
for x in rules.STOP_TOPICS:
    if re.search(r'\b' + re.escape(x) + r'\b', msg):
        print(f"Hit Stop Topic: {x}")

# 3. Blocked Food
for x in rules.BLOCKED_FOOD:
    if x in msg:
        print(f"Hit Blocked Food: {x}")
