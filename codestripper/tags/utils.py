import re
from typing import Union

from codestripper.tags.tag import SingleTag

whitespace_regex = re.compile(r"\s+")


def calculate_regex_length(tag: SingleTag) -> int:
    # Symbol is either ':' or '::'
    last_index = tag.regex.rfind(":")
    if last_index == -1:
        raise AssertionError(f"Cannot find replacement for tag {tag.__class__.__name__} at line {tag.data.line_number}")
    regex_length = last_index + len(tag.data.comment)
    return tag.data.match_start + regex_length + 1


def calculate_add(content: str, comment: str, tag: SingleTag) -> str:
    match = content[tag.start:tag.end]
    replace_start = calculate_regex_length(tag)
    if replace_start > len(match):
        raise AssertionError(f"Cannot find replacement for tag {tag.__class__.__name__} at line {tag.data.line_number}")
    replacement = match[:tag.data.match_start] + match[replace_start:]
    return replacement


def calculate_replacement(content: str, tag: SingleTag) -> str:
    match = content[tag.start:tag.end]
    replace_start = calculate_regex_length(tag)
    if replace_start > len(match):
        raise AssertionError(f"Cannot find replacement for tag {tag.__class__.__name__} at line {tag.data.line_number}")
    whitespace_match = whitespace_regex.match(match)
    whitespace = ''
    if whitespace_match:
        whitespace = whitespace_match.group()
    replacement = whitespace + match[replace_start:]
    return replacement


def calculate_replacement_whitespace(content: str, comment: str, tag: SingleTag) -> Union[str, None]:
    replacement = calculate_replacement(content, tag)
    if len(replacement.strip()) > 0:
        return replacement
    else:
        return None
