import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class LogFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level


def set_up_logger():
    MIN_LEVEL = logging.DEBUG
    stdout_hdlr = logging.StreamHandler(sys.stdout)
    stderr_hdlr = logging.StreamHandler(sys.stderr)
    log_filter = LogFilter(logging.WARNING)
    file_info_hdlr = logging.FileHandler(BASE_DIR / "logs/logs/info.log")
    file_info_hdlr.setLevel(logging.INFO)
    file_dubug_hdlr = logging.FileHandler(BASE_DIR / "logs/logs/debug.log")
    file_dubug_hdlr.setLevel(logging.DEBUG)
    file_error_hdlr = logging.FileHandler(BASE_DIR / "logs/logs/error.log")
    file_error_hdlr.setLevel(logging.ERROR)
    file_critical_hdlr = logging.FileHandler(BASE_DIR / "logs/logs/critical.log")
    file_critical_hdlr.setLevel(logging.CRITICAL)
    file_warning_hdlr = logging.FileHandler(BASE_DIR / "logs/logs/warning.log")
    file_warning_hdlr.setLevel(logging.WARNING)
    stdout_hdlr.addFilter(log_filter)
    stdout_hdlr.setLevel(MIN_LEVEL)
    stderr_hdlr.setLevel(max(MIN_LEVEL, logging.WARNING))
    rootLogger = logging.getLogger()
    rootLogger.addHandler(stdout_hdlr)
    rootLogger.addHandler(stderr_hdlr)
    rootLogger.addHandler(file_info_hdlr)
    rootLogger.addHandler(file_dubug_hdlr)
    rootLogger.addHandler(file_error_hdlr)
    rootLogger.addHandler(file_critical_hdlr)
    rootLogger.addHandler(file_warning_hdlr)

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    stdout_hdlr.setFormatter(formatter)
    stderr_hdlr.setFormatter(formatter)
    file_info_hdlr.setFormatter(formatter)
    file_dubug_hdlr.setFormatter(formatter)
    file_error_hdlr.setFormatter(formatter)
    file_critical_hdlr.setFormatter(formatter)
    file_warning_hdlr.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(
        logging.DEBUG,
    )
    return logger


logger = set_up_logger()
