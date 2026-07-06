import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.audio.recorder import record_until_silence

print("=" * 50)
print("JARVIS VAD RECORDER TEST")
print("=" * 50)

record_until_silence()

print("\n✅ Test completed!")