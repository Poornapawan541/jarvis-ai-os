"""
=========================================
TEST - COMMAND NORMALIZER
=========================================
"""

from core.planner.normalizer import normalizer


tests = [

    "Open Chrome",

    "Open Chrome then GitHub",

    "Launch VS Code",

    "Start Calculator",

    "Run Notepad",

    "Find Python tutorials",

    "Look up Artificial Intelligence",

    "Open Chrome, then GitHub afterwards search AI finally open VS Code.",

    "Open Chrome and then YouTube",

    "Open Chrome after that search LangChain",

    "Launch Chrome, afterwards launch GitHub",

]


print("=" * 60)
print("JARVIS COMMAND NORMALIZER TEST")
print("=" * 60)

for command in tests:

    normalized = normalizer.normalize(command)

    print(f"\nINPUT : {command}")
    print(f"OUTPUT: {normalized}")