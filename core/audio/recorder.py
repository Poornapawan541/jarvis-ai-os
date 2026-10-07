"""
=========================================
JARVIS AI - Audio Utilities
=========================================
"""

import sounddevice as sd
import soundfile as sf
import numpy as np

from config import SAMPLE_RATE, CHANNELS, RECORD_SECONDS, SILENCE_TIMEOUT, MAX_RECORD_SECONDS
from core.audio.vad import VoiceActivityDetector


# =========================================
# AUDIO LEVEL SETTINGS
# =========================================

# These are dBFS thresholds, NOT calibrated dB SPL.
MIN_AUDIO_DB = -45.0
MAX_AUDIO_DB = -3.0

# Number of consecutive silent chunks before stopping
MAX_SILENCE_CHUNKS = 12


def calculate_db(audio):
    """
    Calculate RMS audio level in dBFS.
    """

    audio = np.asarray(audio, dtype=np.float32)

    if audio.size == 0:
        return -100.0

    rms = np.sqrt(np.mean(np.square(audio)))

    if rms <= 1e-10:
        return -100.0

    db = 20 * np.log10(rms)

    return float(db)


def record_audio(output_file="recording.wav"):
    """
    Record audio with automatic voice detection:
    STARTS -> detects speech -> continues while speaking -> STOPS after short silence.
    Preserves 16 kHz mono WAV output and returns output_file path.
    """
    return record_until_silence(output_file=output_file)


def record_until_silence(output_file="recording.wav"):
    """
    Record speech using VAD and audio-level filtering.

    Speech is accepted only when the microphone signal
    is above the configured minimum level.
    """

    vad = VoiceActivityDetector(
        silence_duration=SILENCE_TIMEOUT,
        sample_rate=SAMPLE_RATE,
        chunk_size=1024,
    )

    print("\n🎤 Listening...")
    print("🔊 Speak when ready...")

    frames = []

    started = False
    silence_chunks = 0
    max_chunks = int((MAX_RECORD_SECONDS * SAMPLE_RATE) / vad.chunk_size)
    total_chunks = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        blocksize=vad.chunk_size,
    ) as stream:

        while True:

            audio_chunk, overflowed = stream.read(
                vad.chunk_size
            )

            audio_chunk = audio_chunk.flatten()
            total_chunks += 1

            # ---------------------------------
            # Calculate microphone level
            # ---------------------------------

            db_level = calculate_db(audio_chunk)

            # ---------------------------------
            # Voice Activity Detection
            # ---------------------------------

            speaking = vad.is_speaking(audio_chunk)

            # ---------------------------------
            # BEFORE SPEECH STARTS
            # ---------------------------------

            if not started:

                if (
                    speaking
                    and db_level >= MIN_AUDIO_DB
                    and db_level <= MAX_AUDIO_DB
                ):

                    print(
                        f"🗣️ Speech detected "
                        f"({db_level:.1f} dBFS)"
                    )

                    started = True
                    frames.append(audio_chunk)

                # Avoid waiting indefinitely if max duration reached without speech
                if total_chunks >= max_chunks:
                    print("🛑 Recording timeout reached.")
                    break

                continue

            # ---------------------------------
            # AFTER SPEECH STARTS
            # ---------------------------------

            frames.append(audio_chunk)

            # ---------------------------------
            # Silence detection
            # ---------------------------------

            if (
                not speaking
                or db_level < MIN_AUDIO_DB
            ):

                silence_chunks += 1

            else:

                silence_chunks = 0

            # ---------------------------------
            # Stop after enough silence or max recording duration
            # ---------------------------------

            if silence_chunks >= vad.required_silent_chunks or total_chunks >= max_chunks:

                print("🛑 Silence detected.")

                break

    # =========================================
    # NO SPEECH DETECTED
    # =========================================

    if not frames:

        print("⚠️ No valid speech detected.")

        return None
    # =========================================
    # SAVE AUDIO
    # =========================================

    audio = np.concatenate(frames)

    sf.write(
        output_file,
        audio,
        SAMPLE_RATE
    )

    print(
        f"✅ Recording saved: {output_file}"
    )

    return output_file