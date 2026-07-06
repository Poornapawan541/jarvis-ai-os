"""
=========================================
JARVIS AI
=========================================
"""

from core.voice.piper import tts
from core.audio.recorder import record_audio
from core.voice.whisper import stt
from core.brain.llm import llm


def main():

    print("=" * 50)
    print("      JARVIS AI STARTED")
    print("=" * 50)

    tts.speak("Hello Pawan. I am Jarvis. How can I help you today?")

    while True:

        print("\n🎤 Listening...")

        audio = record_audio()

        user_text = stt.transcribe(audio)

        if user_text.strip() == "":
            print("⚠️ I didn't hear anything.")
            continue

        print(f"\n🧑 You: {user_text}")

        if user_text.lower() in [
            "exit",
            "quit",
            "stop",
            "goodbye",
            "bye",
        ]:
            tts.speak("Goodbye Pawan.")
            break

        print("\n🧠 Thinking...")

        answer = llm.ask(user_text)

        print(f"\n🤖 Jarvis:\n{answer}")

        tts.speak(answer)


if __name__ == "__main__":
    main()