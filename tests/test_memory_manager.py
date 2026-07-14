import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.memory.manager import MemoryManager

memory = MemoryManager()

memory.remember("Pawan wants to build Jarvis OS.")

print("✅ Memory Manager works!")

memory.close()