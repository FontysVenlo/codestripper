import logging
from logging import LogRecord

import pytest

from codestripper.utils import ColourFormatter, set_logger_level


@pytest.mark.parametrize(
    "level, name, control", [
        (0, "", False),
        (10, "DEBUG", True),
        (20, "INFO", True),
        (30, "WARNING", True),
        (40, "ERROR", True),
        (50, "CRITICAL", True)
    ]
)
def test_colour_formatter(level: int, name: str, control: bool):
    formatter = ColourFormatter()
    record = LogRecord(name="test", level=level, pathname="testpath", lineno=0, msg="Test message", args=None, exc_info=None)
    formatted = formatter.format(record)
    contains_name = name in formatted
    contains_control = '\x1b[' in formatted
    control_correct = contains_control if control else not contains_control
    assert (contains_name and control_correct), "Colour formatter should format correctly"


@pytest.mark.parametrize(
    "verbosity, level, add_colours", [
        (0, 40, True),
        (1, 30, True),
        (2, 20, True),
        (3, 10, True),
        (0, 40, False),
        (1, 30,  False),
        (2, 20,  False),
        (3, 10, False),
    ]
)
def test_set_logger(verbosity: int, level: int, add_colours: bool):
    logger_name = f"test{verbosity}{add_colours}"
    set_logger_level(logger_name, verbosity, add_colours)
    logger = logging.getLogger(logger_name)
    correct_level = logger.getEffectiveLevel() == level

    formatter = logger.handlers[0].formatter
    correct_formatter = isinstance(formatter, ColourFormatter) if add_colours else formatter is None
    assert correct_level and correct_formatter, "set_logger should set correct formatter and level"
