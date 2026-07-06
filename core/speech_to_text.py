"""
=========================================
JARVIS AI - Speech To Text Module
=========================================
"""

from faster_whisper import WhisperModel
from config import WHISPER_MODEL


class SpeechToText:

    def __init__(self):

        print("🧠 Loading Whisper model...")

        self.model = WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )

        print("✅ Whisper Loaded Successfully!")

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            language="en",
            vad_filter=True
        )

        text = " ".join(segment.text.strip() for segment in segments)

        return text


stt = SpeechToText()