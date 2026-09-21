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


def test_uncomment_multiple_comment_styles():
    """The comment style of an earlier run must not leak into a later one"""
    slashes = "//cs:uncomment:start\n//test\n//cs:uncomment:end\n"
    assert CodeStripper(slashes, Comment("//")).strip() == "test\n"
    hashes = "#cs:uncomment:start\n#test\n#cs:uncomment:end\n"
    assert CodeStripper(hashes, Comment("#")).strip() == "test\n"


def test_uncomment_special_regex_characters():
    case = "(*cs:uncomment:start*)\n(*test*)\n(*cs:uncomment:end*)\n"
    assert CodeStripper(case, Comment("(*", "*)")).strip() == "test\n"


def test_uncomment_removes_close_symbol():
    case = "<!--cs:uncomment:start-->\n    <!--<tag/>-->\n<!--cs:uncomment:end-->\n"
    assert CodeStripper(case, Comment("<!--", "-->")).strip() == "    <tag/>\n"
