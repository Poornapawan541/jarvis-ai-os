import sys
from pathlib import Path

# Add project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.utils import record_audio
from core.voice.whisper import stt

print("=" * 50)
print("JARVIS SPEECH TO TEXT TEST")
print("=" * 50)

# Record voice
audio_file = record_audio()

print("\n🧠 Whisper is thinking...\n")

# Convert speech to text
text = stt.transcribe(audio_file)

print("=" * 50)
print("YOU SAID:")
print("=" * 50)
print(text)
print("=" * 50)