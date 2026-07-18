import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name:str)->logging.Logger:
    log_dir=Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger=logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    sh=logging.StreamHandler()
    sh.setFormatter(fmt)
    fh=RotatingFileHandler(log_dir/"engine.log",maxBytes=1_000_000,backupCount=3)
    fh.setFormatter(fmt)
    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger
