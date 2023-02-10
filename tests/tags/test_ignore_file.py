import pytest

from codestripper.code_stripper import CodeStripper
from codestripper.errors import InvalidTagError
from codestripper.tags import IgnoreFileError


def test_invalid_tag():
    case = """
    test line
    //cs:ignore
    """
    with pytest.raises(InvalidTagError) as ex:
        CodeStripper(case, "//").strip()
    message = str(ex)
    print(message)
    assert message.__contains__("IgnoreFileTag") and message.__contains__("3")


def test_ignored_file():
    case = "//cs:ignore"
    with pytest.raises(IgnoreFileError):
        CodeStripper(case, "//").strip()
