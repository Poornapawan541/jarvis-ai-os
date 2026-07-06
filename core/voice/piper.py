"""
=========================================
JARVIS AI - Piper Text To Speech Module
=========================================
"""

import subprocess
from pathlib import Path
import simpleaudio as sa


class TextToSpeech:

    def __init__(self):
        # Project root
        self.root = Path(__file__).resolve().parent.parent.parent

        # Piper executable
        self.piper = self.root / "piper" / "piper.exe"

        # Voice model
        self.model = (
            self.root
            / "models"
            / "voices"
            / "en_US-lessac-medium.onnx"
        )

        # Output audio
        self.output = self.root / "output.wav"

    def speak(self, text: str):

        print(f"\n🤖 Jarvis: {text}\n")

        command = [
            str(self.piper),
            "-m",
            str(self.model),
            "-f",
            str(self.output),
        ]

        subprocess.run(
            command,
            input=text,
            text=True,
            capture_output=True
        )

        wave = sa.WaveObject.from_wave_file(str(self.output))
        play = wave.play()
        play.wait_done()


tts = TextToSpeech()