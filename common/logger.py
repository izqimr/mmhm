import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.env import LOG_DIR, LOG_FILE, LOG_LEVEL

_INITIALIZED = False


def init_logger(log_file: str | Path | None = None, level: str | int | None = None) -> logging.Logger:
    global _INITIALIZED

    root = logging.getLogger()
    if _INITIALIZED:
        return root

    target_file = Path(log_file) if log_file else Path(LOG_FILE)
    target_file.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(level, int):
        log_level = level
    else:
        level_name = (level or LOG_LEVEL).upper()
        log_level = getattr(logging, level_name, logging.INFO)

    root.setLevel(log_level)
    root.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        filename=target_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    _INITIALIZED = True
    root.info("logger initialized: file=%s level=%s", target_file, logging.getLevelName(log_level))
    return root


def get_logger(name: str | None = None) -> logging.Logger:
    if not _INITIALIZED:
        init_logger()
    return logging.getLogger(name)
