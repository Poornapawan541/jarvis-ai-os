"""
=========================================
JARVIS AI - Audio Utilities
=========================================
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
from config import SAMPLE_RATE, CHANNELS, RECORD_SECONDS
from core.audio.vad import VoiceActivityDetector


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
def record_until_silence(output_file="recording.wav"):
    """
    Record audio until the user stops speaking.
    """

    vad = VoiceActivityDetector()

    print("\n🎤 Listening... (Start speaking)")

    frames = []
    started = False

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        blocksize=vad.chunk_size,
    ) as stream:

        while True:

            audio_chunk, overflowed = stream.read(vad.chunk_size)

            audio_chunk = audio_chunk.flatten()

            if not started:

                if vad.is_speaking(audio_chunk):
                    print("🗣️ Speech detected...")
                    started = True
                    frames.append(audio_chunk)

            else:

                frames.append(audio_chunk)

                if vad.should_stop(audio_chunk):
                    print("🛑 Silence detected.")
                    break

    audio = np.concatenate(frames)

    sf.write(output_file, audio, SAMPLE_RATE)

    print("✅ Recording saved:", output_file)

    return output_file