import sounddevice as sd
import numpy as np
import time


SAMPLE_RATE = 16000
BLOCK_SIZE = 1024


def calculate_db(audio):

    rms = np.sqrt(np.mean(np.square(audio)))

    if rms <= 1e-10:
        return -100.0

    return 20 * np.log10(rms)


print("=========================================")
print("JARVIS MICROPHONE LEVEL TEST")
print("=========================================")

print("\nSpeak normally...")
print("Press CTRL+C to stop.\n")


try:

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=BLOCK_SIZE,
    ) as stream:

        while True:

            audio, overflowed = stream.read(
                BLOCK_SIZE
            )

            audio = audio.flatten()

            db = calculate_db(audio)

            print(
                f"\rMicrophone level: {db:6.1f} dBFS",
                end=""
            )

            time.sleep(0.05)

except KeyboardInterrupt:

    print("\n\nTest stopped.")
