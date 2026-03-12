# cachemed/utils/logger.py
import logging
import os


def get_logger(name):
    """Get configured logger"""
    logger = logging.getLogger(name)

    if not logger.handlers:
        level = os.environ.get('LOG_LEVEL', 'INFO')
        logger.setLevel(getattr(logging, level))

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger