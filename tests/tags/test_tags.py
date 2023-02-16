import re
from pathlib import Path

import pytest

from codestripper import tokenizer
from codestripper.code_stripper import CodeStripper
from codestripper.errors import InvalidTagError
from codestripper.tags import RemoveRangeTag
from codestripper.tags.tag import RangeOpenTag, Tag, SingleTag, TagData, RangeCloseTag, RangeTag
from codestripper.tokenizer import Tokenizer, calculate_mappings


class InvalidOpenTag(RangeOpenTag):
    regex = [r'cs:invalid:start(.*)?']

    def __init__(self, data: TagData) -> None:
        super().__init__(InvalidRangeTag, data)


class InvalidCloseTag(RangeCloseTag):
    regex = [r'cs:invalid:end(.*)?']

    def __init__(self, data: TagData) -> None:
        super().__init__(InvalidRangeTag, data)


class InvalidRangeTag(RangeTag):

    def __init__(self, open_tag: InvalidOpenTag, close_tag: InvalidCloseTag) -> None:
        super().__init__(open_tag, close_tag)

    def is_valid(self) -> bool:
        return False


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


def test_tag_end_file():
    case = """
    //cs:uncomment:start
    //test2
    //cs:uncomment:end"""
    stripper = CodeStripper(case, "//")
    output = stripper.strip()

    expected = """
    test2\n"""
    assert output == expected, "Tags at the end of file should work"


def test_missing_close_tag():
    case = """
        test line
        //cs:remove:start
        """
    with pytest.raises(AssertionError):
        CodeStripper(case, "//").strip()


def test_missing_close_tag_nested():
    case = """
        test line
        //cs:remove:start
        //cs:remove:start
        //cs:remove:end
        """
    with pytest.raises(AssertionError):
        CodeStripper(case, "//").strip()


def test_close_without_open():
    case = """
        test line
        //cs:remove:end
        """
    with pytest.raises(AssertionError):
        CodeStripper(case, "//").strip()


def test_mismatch_open_close():
    case = """
        test line
        //cs:uncomment:start
        //cs:remove:end
        """
    with pytest.raises(AssertionError):
        CodeStripper(case, "//").strip()


def test_invalid_tag():
    case = """
            test line
            !!cs:invalid:start
            !!cs:invalid:end
            """
    default_tags = tokenizer.default_tags
    tokenizer.default_tags = {
        InvalidOpenTag,
        InvalidCloseTag
    }
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, "!!").strip()
    tokenizer.default_tags = default_tags
    assert "InvalidRangeTag" in str(ex)


def test_data():
    regex = re.compile("test")
    match = regex.search("test")
    data = TagData("test", 0, 0, match, "test")
    assert str(data).__contains__("test")
