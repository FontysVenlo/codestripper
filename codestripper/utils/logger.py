import logging
from typing import Dict


class ColourFormatter(logging.Formatter):
    """
    Custom logger that adds color based on level
    Taken from: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    """

    light_blue = "\x1b[1;34m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_log = "%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS: Dict[int, str] = {
        logging.DEBUG: grey + format_log + reset,
        logging.INFO: grey + format_log + reset,
        logging.WARNING: yellow + format_log + reset,
        logging.ERROR: red + format_log + reset,
        logging.CRITICAL: bold_red + format_log + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CodeStripperHandler(logging.StreamHandler):
    """Handler that is added by `set_logger_level`, so that it can be replaced instead of duplicated"""


# Level per verbosity, more verbosity than available uses the last level
VERBOSITY_LEVELS = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]


def set_logger_level(logger_name: str, verbosity: int = 0, add_colours: bool = True) -> None:
    logger = logging.getLogger(logger_name)
    level = VERBOSITY_LEVELS[min(max(verbosity, 0), len(VERBOSITY_LEVELS) - 1)]
    handler = CodeStripperHandler()
    if add_colours:
        handler.setFormatter(ColourFormatter())
    logger.setLevel(level)
    handler.setLevel(level)
    # Replace the handler of an earlier call, otherwise every message is logged multiple times
    for existing in [h for h in logger.handlers if isinstance(h, CodeStripperHandler)]:
        logger.removeHandler(existing)
    logger.addHandler(handler)
