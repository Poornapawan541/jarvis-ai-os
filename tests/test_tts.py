import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.voice.piper import tts

print("========== TTS TEST ==========")

tts.speak("Hello Pawan.")

tts.speak("I am Jarvis.")

tts.speak("Your artificial intelligence assistant is now online.")

print("========== TEST COMPLETED ==========")