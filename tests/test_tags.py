import pytest

from codestripper.code_stripper import CodeStripper
from codestripper.tokenizer import Tokenizer


def test_comment():
    case = "#cs:add:test"
    expected = "test"
    output = CodeStripper(case, "#").strip()
    assert output == expected, "Different comments can be used"


def test_nested_tags():
    case = """
    //cs:uncomment:start
    //test//cs:replace:replaced
    //test2
    //cs:uncomment:end
    """
    stripper = CodeStripper(case, "//")
    output = stripper.strip()

    expected = """
    replaced
    test2
    """
    assert output == expected, "Nested tags should work"
