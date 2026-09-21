from codestripper.code_stripper import CodeStripper
from codestripper.utils.comments import Comment


def test_replace():
    case = """
    asd//cs:replace:test
    """
    expected = """
    test
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Replace should replace keeping whitespace"


def test_replace_empty():
    case = """
    asd//cs:replace:
    """
    expected = "\n    \n    "  # The replacement is empty, the whitespace in front of the tag is kept
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Replace should replace with empty string keeping whitespace"


def test_replace_valid():
    case = """
    asd//cs:replace
    """
    expected = """
    asd//cs:replace
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Only valid replace tag should work"


def test_replace_symbol():
    case = """
    asd//cs:replace://TODO: test
    """
    expected = """
    //TODO: test
    """
    output = CodeStripper(case, Comment("//")).strip()
    assert output == expected, "Replace with ':' should work"
