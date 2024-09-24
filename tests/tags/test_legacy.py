from codestripper.code_stripper import CodeStripper
from codestripper.utils.comments import Comment


def test_legacy_should_remove():
    case = """
    //Start Solution::replacewith::
    test
    //End Solution::replacewith::
    """
    expected = """
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Legacy should remove contents inbetween tags"


def test_legacy_should_replace():
    case = """
    //Start Solution::replacewith::start
    test
    //End Solution::replacewith::end
    """
    expected = """
    start
    end
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Legacy should replace on start and end"
