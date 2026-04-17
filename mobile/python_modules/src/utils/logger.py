"""
Logging utility
"""
import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "AstroKnowledge", log_level: str = "INFO") -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler is always available.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File logging is optional: Android assets paths can be read-only.
    try:
        log_dir = Path(os.environ.get("ASTRO_LOG_DIR", "logs"))
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except Exception:
        # Console-only logging keeps runtime features working in restricted FS envs.
        pass
    
    return logger


# Default logger
logger = setup_logger()
