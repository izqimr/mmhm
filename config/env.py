from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / os.getenv("LOG_FILE_NAME", "framework.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
