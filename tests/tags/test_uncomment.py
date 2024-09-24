from codestripper.code_stripper import CodeStripper
from codestripper.utils.comments import Comment


def test_uncomment_range():
    case = """
    //cs:uncomment:start
    //test
    // test2
    //cs:uncomment:end
    """
    expected = """
    test
     test2
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Uncomment should uncomment all, keeping whitespace"


def test_uncomment_without_comments():
    case = """
    //cs:uncomment:start
    test
     test2
    //cs:uncomment:end
    """
    expected = """
    test
     test2
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Uncomment shouldn't process non-commented lines"
