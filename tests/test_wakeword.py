from core.audio.wakeword import wake_word_detector


print("=" * 50)
print("JARVIS WAKE WORD TEST")
print("=" * 50)


tests = [
    "Jarvis",
    "jarvis",
    "Hello Jarvis",
    "Hey Jarvis",
    "Jarosh",
    "Jarves",
    "hello pawan",
    "open github",
    "calculator",
]


for text in tests:

    result = wake_word_detector.detect(text)

    status = "✅" if result else "❌"

    print(
        f"{status} "
        f"{text:<20} -> {result}"
    )