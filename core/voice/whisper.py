"""
=========================================
JARVIS AI - Speech To Text Module
=========================================
"""

import os
import sys
from pathlib import Path
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE

# Ensure bundled NVIDIA DLLs are found by ctranslate2 on Windows
if sys.platform == "win32":
    venv_site = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    for sub in ["cublas", "cudnn", "cuda_nvrtc"]:
        dll_dir = venv_site / sub / "bin"
        if dll_dir.is_dir():
            dll_dir_str = str(dll_dir)
            if dll_dir_str not in os.environ.get("PATH", ""):
                os.environ["PATH"] = dll_dir_str + os.pathsep + os.environ.get("PATH", "")
            if hasattr(os, "add_dll_directory"):
                try:
                    os.add_dll_directory(dll_dir_str)
                except Exception:
                    pass


class SpeechToText:

    def __init__(self):

        print("🧠 Loading Whisper model...")

        self.model = WhisperModel(
            WHISPER_MODEL,
            device=getattr(self, "device", WHISPER_DEVICE),
            compute_type=getattr(self, "compute_type", WHISPER_COMPUTE_TYPE)
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