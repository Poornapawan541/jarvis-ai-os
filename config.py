"""
=========================================
JARVIS AI - Configuration File
=========================================
Author : Pawan
Version: 1.0
"""

# -----------------------------
# Assistant Settings
# -----------------------------

ASSISTANT_NAME = "Jarvis"
WAKE_WORD = "hey jarvis"

# -----------------------------
# Audio Settings
# -----------------------------

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280
RECORD_SECONDS = 5
SILENCE_TIMEOUT = 1.0
MAX_RECORD_SECONDS = 15.0

# -----------------------------
# Whisper Settings
# -----------------------------

WHISPER_MODEL = "small"
WHISPER_DEVICE = "cuda"
WHISPER_COMPUTE_TYPE = "float16"

# Available models:
# tiny
# base
# small
# medium
# large-v3

# -----------------------------
# Ollama Settings
# -----------------------------

OLLAMA_MODEL = "llama3.2:3b"

# -----------------------------
# Voice Settings
# -----------------------------

VOICE_RATE = 170
VOICE_VOLUME = 1.0

# -----------------------------
# Paths
# -----------------------------

MEMORY_FOLDER = "memory"
LOG_FOLDER = "logs"
MODEL_FOLDER = "models"

# -----------------------------
# Debug Mode
# -----------------------------

DEBUG = True