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


@pytest.mark.parametrize("case", [
    "//cs:ignore some explanation\nclass A {}\n",
    "//cs:ignore \nclass A {}\n",
])
def test_ignored_file_with_trailing_text(case: str):
    with pytest.raises(IgnoreFileError):
        CodeStripper(case, Comment("//")).strip()


@pytest.mark.parametrize("case", [
    "//cs:ignored\nclass A {}\n",
    "//cs:ignore_this\nclass A {}\n",
    "//cs:ignore:something\nclass A {}\n",
])
def test_not_an_ignore_tag(case: str):
    assert CodeStripper(case, Comment("//")).strip() == case
