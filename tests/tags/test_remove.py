from codestripper.code_stripper import CodeStripper
from codestripper.utils.comments import Comment


def test_remove_range():
    case = """
    //cs:remove:start
    test
    //cs:remove:end
    """
    expected = """
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Remove should remove all"


def test_remove_single():
    case = """
    asd//cs:remove
    """
    expected = """
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Remove should remove single line"
