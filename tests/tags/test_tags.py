import pytest

from codestripper import tokenizer
from codestripper.code_stripper import CodeStripper
from codestripper.errors import InvalidTagError, TokenizerError
from codestripper.tags.tag import RangeOpenTag, TagData, RangeCloseTag, RangeTag
from codestripper.utils.comments import Comment


class InvalidOpenTag(RangeOpenTag):
    regex = r'cs:invalid:start(.*)?'

    def __init__(self, data: TagData) -> None:
        super().__init__(InvalidRangeTag, data)


class InvalidCloseTag(RangeCloseTag):
    regex = r'cs:invalid:end(.*)?'

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
    output = CodeStripper(case, Comment("#")).strip()
    assert output == expected, "Different comments can be used"


def test_nested_tags():
    case = """
    //cs:uncomment:start
    //test//cs:replace:replaced
    //test2
    //cs:uncomment:end
    """
    stripper = CodeStripper(case, Comment("//"))
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
    stripper = CodeStripper(case, Comment("//"))
    output = stripper.strip()

    expected = """
    test2\n"""
    assert output == expected, "Tags at the end of file should work"


def test_missing_close_tag():
    case = """
        test line
        //cs:remove:start
        """
    with pytest.raises(TokenizerError):
        CodeStripper(case, Comment("//")).strip()


def test_missing_close_tag_nested():
    case = """
        test line
        //cs:remove:start
        //cs:remove:start
        //cs:remove:end
        """
    with pytest.raises(TokenizerError):
        CodeStripper(case, Comment("//")).strip()


def test_close_without_open():
    case = """
        test line
        //cs:remove:end
        """
    with pytest.raises(TokenizerError):
        CodeStripper(case, Comment("//")).strip()


def test_mismatch_open_close():
    case = """
        test line
        //cs:uncomment:start
        //cs:remove:end
        """
    with pytest.raises(TokenizerError):
        CodeStripper(case, Comment("//")).strip()


def test_invalid_tag():
    case = """
            test line
            ^^cs:invalid:start
            ^^cs:invalid:end
            """
    default_tags = tokenizer.default_tags
    tokenizer.default_tags = {
        InvalidOpenTag,
        InvalidCloseTag
    }
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, Comment("^^")).strip()
    tokenizer.default_tags = default_tags
    assert "InvalidRangeTag" in str(ex)


def test_data():
    data = TagData("test", 0, 0, 0, 0, 0, 0, 0, "//")
    assert str(data).__contains__("test")


def test_invalid_range_tag_reports_line_and_reason():
    case = "line 1\n//cs:remove:start\n//cs:remove:end\n"
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, Comment("//")).strip()
    assert ex.value.line_number == 2
    assert "RemoveRangeTag" in ex.value.message and "does not contain any lines" in ex.value.message


def test_invalid_legacy_range_tag_reports_line():
    case = "line 1\nline 2\n//Start Solution::replacewith::\n//End Solution::replacewith::\n"
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, Comment("//")).strip()
    assert ex.value.line_number == 3


def test_invalid_single_tag_reports_line_and_reason():
    case = "line 1\nline 2\n//cs:ignore\n"
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, Comment("//")).strip()
    assert ex.value.line_number == 3
    assert "only allowed on the first line" in ex.value.message


def test_tokenizer_error_line_numbers():
    with pytest.raises(TokenizerError) as ex:
        CodeStripper("a\nb\n//cs:remove:start\nc\n", Comment("//")).strip()
    assert ex.value.line_number == 3
    with pytest.raises(TokenizerError) as ex:
        CodeStripper("a\n//cs:remove:end\n", Comment("//")).strip()
    assert ex.value.line_number == 2
