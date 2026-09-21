import pytest

from codestripper.utils.comments import Comment, comments_mapping, get_comments_mapping, parse_comment


def test_parse_comment_open_only():
    assert parse_comment(".java://") == (".java", Comment("//"))


def test_parse_comment_open_and_close():
    assert parse_comment(".html:<!--:-->") == (".html", Comment("<!--", "-->"))


def test_parse_comment_lowercases_extension():
    assert parse_comment(".Java://") == (".java", Comment("//"))


@pytest.mark.parametrize("specification", [".java", "", ".java:", ":", ":#", ".java:a:b:c", "java://", ".java:://"])
def test_parse_comment_invalid(specification: str):
    with pytest.raises(ValueError):
        parse_comment(specification)


def test_get_comments_mapping_overrides_and_extends():
    mapping = get_comments_mapping([".java:#", ".kt://"])
    assert mapping[".java"] == Comment("#")
    assert mapping[".kt"] == Comment("//")
    assert mapping[".py"] == comments_mapping[".py"]


def test_get_comments_mapping_does_not_change_defaults():
    get_comments_mapping([".java:#", ".kt://"])
    assert comments_mapping[".java"] == Comment("//")
    assert ".kt" not in comments_mapping
