"""
=========================================
JARVIS AI - Audio Utilities
=========================================
"""

import sounddevice as sd
import soundfile as sf
from config import SAMPLE_RATE, CHANNELS, RECORD_SECONDS


def record_audio(output_file="recording.wav"):
    """
    Record audio from the microphone and save it as a WAV file.
    """

    print("\n🎤 Speak now...")
    print(f"Recording for {RECORD_SECONDS} seconds...\n")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )

    sd.wait()

    sf.write(output_file, audio, SAMPLE_RATE)

    print("✅ Recording saved:", output_file)

    return output_file