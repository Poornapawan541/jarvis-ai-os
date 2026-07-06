import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from core.audio.vad import VoiceActivityDetector

vad = VoiceActivityDetector()

speech = np.random.uniform(-0.5, 0.5, 1024)
silence = np.zeros(1024)

print("Speech detected:", vad.is_speaking(speech))
print("Silence detected:", vad.is_speaking(silence))