"""
=========================================
JARVIS CORE
=========================================
"""

from core.voice.piper import tts
from core.audio.recorder import record_audio
from core.voice.whisper import stt
from core.conversation.engine import engine


class Jarvis:

    def __init__(self):
        self.running = True

    def greet(self):
        print("=" * 50)
        print("      JARVIS AI STARTED")
        print("=" * 50)

        tts.speak(
            "Hello Pawan. I am Jarvis. How can I help you today?"
        )

    def listen(self):
        print("\n🎤 Listening...")

        audio = record_audio()

        return stt.transcribe(audio)

    def think(self, text):
        return engine.reply(text)

    def speak(self, text):
        tts.speak(text)

    def should_exit(self, text):
        return text.lower() in [
            "exit",
            "quit",
            "bye",
            "goodbye",
            "stop",
        ]

    def run(self):

        self.greet()

        while self.running:

            user_text = self.listen()

            if user_text.strip() == "":
                print("⚠️ I didn't hear anything.")
                continue

            print(f"\n🧑 You: {user_text}")

            if self.should_exit(user_text):
                self.speak("Goodbye Pawan.")
                engine.close()
                break

            print("\n🧠 Thinking...")

            answer = self.think(user_text)

            print(f"\n🤖 Jarvis:\n{answer}")

            self.speak(answer)