from core.agents.router import router


tests = [
    "open github",
    "open gmail",
    "search python decorators",
    "google machine learning",
    "hello jarvis",
    "explain artificial intelligence",
]


print("=" * 50)
print("JARVIS AGENT ROUTER TEST")
print("=" * 50)

for text in tests:

    agent = router.route(text)

    if agent:
        print(f"✅ {text:<35} -> {agent.name}")
    else:
        print(f"❌ {text:<35} -> LLM")