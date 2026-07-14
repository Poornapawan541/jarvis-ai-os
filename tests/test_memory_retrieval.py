import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.memory.manager import MemoryManager

memory = MemoryManager()

print("=" * 50)
print("JARVIS MEMORIES")
print("=" * 50)

for item in memory.get_memories():
    print("-", item)

memory.close()