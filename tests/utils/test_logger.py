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
    record = LogRecord(name="test", level=level, pathname="testpath", lineno=0, msg="Test message", args=None,
                       exc_info=None)
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


@pytest.mark.parametrize("verbosity, level", [(4, 10), (10, 10), (-1, 40)])
def test_set_logger_out_of_range_verbosity(verbosity: int, level: int):
    logger_name = f"testrange{verbosity}"
    set_logger_level(logger_name, verbosity)
    logger = logging.getLogger(logger_name)
    assert logger.level == level and logger.handlers[0].level == level


def test_set_logger_twice_does_not_duplicate_handlers(capsys: pytest.CaptureFixture):
    logger_name = "testtwice"
    set_logger_level(logger_name, 0)
    set_logger_level(logger_name, 2)
    logger = logging.getLogger(logger_name)
    assert len(logger.handlers) == 1 and logger.level == logging.INFO
    logger.info("only once")
    assert capsys.readouterr().err.count("only once") == 1


def test_set_logger_keeps_other_handlers():
    logger_name = "testother"
    logger = logging.getLogger(logger_name)
    other = logging.NullHandler()
    logger.addHandler(other)
    set_logger_level(logger_name, 1)
    set_logger_level(logger_name, 1)
    assert other in logger.handlers and len(logger.handlers) == 2
