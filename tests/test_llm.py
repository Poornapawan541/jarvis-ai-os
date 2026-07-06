import sys
from pathlib import Path

# Add project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.brain.llm import llm

print("=" * 50)
print("JARVIS LLM TEST")
print("=" * 50)

question = input("You: ")

print("\n🤖 Jarvis is thinking...\n")

answer = llm.ask(question)

print("Jarvis:")
print(answer)