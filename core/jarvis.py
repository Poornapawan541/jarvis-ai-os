"""
=========================================
JARVIS CORE
=========================================
"""

from core.voice.piper import tts
from core.audio.recorder import record_audio
from core.voice.whisper import stt

from core.conversation.engine import engine
from core.browser.manager import browser_manager

from core.services.logger import logger
from core.skills.gmail import gmail_skill

class Jarvis:

    def __init__(self):
        self.running = True
        gmail_skill.set_voice_functions(
            self.listen,
            self.speak
        )
    # =========================================
    # GREETING
    # =========================================

    def greet(self):

        print("=" * 50)
        print("      JARVIS AI STARTED")
        print("=" * 50)

        greeting = (
            "Hello Pawan. I am Jarvis. "
            "How can I help you today?"
        )

        # Print ONCE
        print(f"\n🤖 Jarvis: {greeting}\n")

        # Speak without printing
        self.speak(greeting)

    # =========================================
    # LISTEN
    # =========================================

    def listen(self):



        try:

            audio = record_audio()
            if not audio:
                return ""
            text = stt.transcribe(audio)

            if text is None:
                return ""

            return text.strip()

        except KeyboardInterrupt:

            raise

        except Exception as e:

            logger.error(
                f"Speech recognition failed: {e}"
            )

            return ""

    # =========================================
    # THINK
    # =========================================

    def think(self, text):

        return engine.reply(text)

    # =========================================
    # SPEAK
    # =========================================

    def speak(self, text):

        """
        Speak only.

        IMPORTANT:
        This method does NOT print anything.
        Printing is handled by run().
        """

        if not text:
            return

        try:

            tts.speak(text)

        except KeyboardInterrupt:

            logger.warning(
                "Speech playback interrupted."
            )

        except Exception as e:

            logger.error(
                f"TTS failed: {e}"
            )

    # =========================================
    # EXIT COMMAND
    # =========================================

    def should_exit(self, text):

        if not text:
            return False
        command = text.lower().strip().rstrip(".!?")
        return command in [
            "exit",
            "quit",
            "bye",
            "goodbye",
            "stop",
        ]

    # =========================================
    # SHUTDOWN
    # =========================================

    def shutdown(self):

        self.running = False

        print("\n🛑 Shutting down Jarvis...")

        try:
            engine.close()
        except Exception as e:
            logger.error(
                f"Engine shutdown failed: {e}"
            )

        try:
            browser_manager.close()
        except Exception as e:
            logger.error(
                f"Browser shutdown failed: {e}"
            )

        print("\n=========================================")
        print("       JARVIS SHUTDOWN COMPLETE")
        print("=========================================")

    # =========================================
    # MAIN LOOP
    # =========================================

    def run(self):

        try:

            self.greet()

            while self.running:

                # -------------------------
                # LISTEN
                # -------------------------

                user_text = self.listen()

                if not user_text:

                    print(
                        "⚠️ I didn't hear anything."
                    )

                    continue

                print(
                    f"\n🧑 You: {user_text}"
                )

                # -------------------------
                # EXIT
                # -------------------------

                if self.should_exit(user_text):

                    answer = "Goodbye Pawan."

                    # Print ONCE
                    print(
                        f"\n🤖 Jarvis: {answer}"
                    )

                    # Speak only
                    self.speak(answer)
                    self.running = False
                    break

                # -------------------------
                # THINK
                # -------------------------

                print("\n🧠 Thinking...")

                try:

                    answer = self.think(
                        user_text
                    )

                except Exception as e:

                    logger.error(
                        f"Conversation error: {e}"
                    )

                    answer = (
                        "Sorry, I encountered "
                        "an internal error."
                    )

                # -------------------------
                # EMPTY RESPONSE
                # -------------------------

                if not answer:

                    answer = (
                        "Sorry, I couldn't "
                        "generate a response."
                    )

                # -------------------------
                # RESPOND
                # -------------------------

                # PRINT EXACTLY ONCE
                print(
                    f"\n🤖 Jarvis:\n{answer}"
                )

                # SPEAK ONLY
                self.speak(answer)

        except KeyboardInterrupt:

            print(
                "\n\n🛑 Keyboard interrupt detected."
            )

            answer = "Goodbye Pawan."

            # Print ONCE
            print(
                f"\n🤖 Jarvis: {answer}"
            )

            # Speak only
            try:
                self.speak(answer)
            except Exception:
                pass

        finally:

            self.shutdown()
