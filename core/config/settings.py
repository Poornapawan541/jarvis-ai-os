"""
=========================================
JARVIS SETTINGS
=========================================
"""

from dataclasses import dataclass


@dataclass
class Settings:

    # Audio
    sample_rate: int = 16000
    channels: int = 1
    record_seconds: int = 5

    # Models
    llm_model: str = "llama3:latest"
    whisper_model: str = "base"

    # Database
    memory_database: str = "jarvis_memory.db"

    # Logging
    log_level: str = "INFO"

    # User
    user_name: str = "Pawan"

    # Assistant
    assistant_name: str = "Jarvis"


settings = Settings()