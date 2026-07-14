import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.memory.manager import MemoryManager

memory = MemoryManager()

tests = [
    "My name is Pawan.",
    "I like Python.",
    "Open Chrome.",
    "What's the weather today?",
    "Remember that I have an interview on Friday.",
]

for text in tests:
    print(f"\n{text}")
    memory.remember(text)

memory.close()