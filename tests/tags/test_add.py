from codestripper.code_stripper import CodeStripper


def test_add_should_add():
    case = """
    public class AssessmentResult {
        //cs:add://TODO

    """
    expected = """
    public class AssessmentResult {
        //TODO

    """
    output = CodeStripper(case, "//").strip()
    assert output == expected, "Add should add the replacement"


def test_add_valid():
    case = "//cs:add"
    expected = "//cs:add"
    output = CodeStripper(case, "//").strip()
    assert output == expected, "Add should only trigger with valid tag"


def test_add_without_replacement():
    case = "    //cs:add:"
    expected = "    "
    output = CodeStripper(case, "//").strip()
    assert output == expected, "Add without replacement keeps whitelines"

def test_add_with_content_before():
    case = """asd//cs:add:test"""
    expected = """asdtest"""
    output = CodeStripper(case, "//").strip()
    assert output == expected, "Replace should replace with empty string keeping whitespace"
