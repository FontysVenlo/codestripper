import pytest

from codestripper.code_stripper import CodeStripper
from codestripper.errors import InvalidTagError
from codestripper.tags import IgnoreFileError
from codestripper.utils.comments import Comment


def test_invalid_tag():
    case = """
    test line
    //cs:ignore
    """
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, Comment("//")).strip()
    message = str(ex)
    assert message.__contains__("IgnoreFileTag")


def test_ignored_file():
    case = "//cs:ignore"
    with pytest.raises(IgnoreFileError):
        CodeStripper(case, Comment("//")).strip()

def test_ignored_file_closing():
    case = "<!--cs:ignore-->"
    with pytest.raises(IgnoreFileError):
        CodeStripper(case, Comment("<!--", "-->")).strip()