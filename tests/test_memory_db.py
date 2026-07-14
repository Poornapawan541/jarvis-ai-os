import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.memory.database import MemoryDatabase

db = MemoryDatabase()

db.save_memory("Pawan likes Python.")

print("✅ Memory Saved!")

db.close()