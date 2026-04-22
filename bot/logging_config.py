import logging
import os

def setup_logger(name: str = "trading_bot") -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File handler — logs everything
    fh = logging.FileHandler("logs/trading_bot.log")
    fh.setLevel(logging.DEBUG)

    # Console handler — logs INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
