from core.planner.intent_expander import intent_expander

tests = [

    "open chrome and github",

    "open chrome and github and vscode",

    "search python and langchain",

    "search ai and machine learning and deep learning",

    "open chrome and search python and github",

    "open chrome and github and search ai and youtube",

]

print("=" * 60)
print("INTENT EXPANDER TEST")
print("=" * 60)

for t in tests:

    print("\nINPUT")
    print(t)

    print("\nOUTPUT")

    for cmd in intent_expander.expand(t):
        print(" ", cmd)

    print("-" * 60)