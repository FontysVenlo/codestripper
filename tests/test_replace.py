from codestripper.code_stripper import CodeStripper


def test_replace():
    case = """
    asd//cs:replace:test
    """
    expected = """
    test
    """
    output = CodeStripper(case).strip()
    assert output == expected, "Replace should replace keeping whitespace"


def test_replace_empty():
    case = """
    asd//cs:replace:
    """
    expected = """
    
    """
    output = CodeStripper(case).strip()
    assert output == expected, "Replace should replace with empty string keeping whitespace"


def test_replace_valid():
    case = """
    asd//cs:replace
    """
    expected = """
    asd//cs:replace
    """
    output = CodeStripper(case).strip()
    assert output == expected, "Replace should only replace with valid tag"
