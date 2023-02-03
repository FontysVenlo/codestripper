import re
from typing import Union

from codestripper.tags.tag import SingleTag

whitespace_regex = re.compile(r"\s+")


def calculate_replacement(content: str, symbol: str, tag: SingleTag) -> str:
    match = content[tag.start:tag.end]
    match_index = match.rfind(symbol)
    if match_index == -1:
        raise AssertionError(f"Cannot find replacement for tag {tag.__class__.__name__} at line {tag.data.line_number}")
    replace_start = match_index + len(symbol)
    whitespace_match = whitespace_regex.match(match)
    whitespace = ''
    if whitespace_match:
        whitespace = whitespace_match.group()
    replacement = whitespace + match[replace_start:]
    return replacement


def calculate_replacement_whitespace(content: str, symbol: str, tag: SingleTag) -> Union[str, None]:
    replacement = calculate_replacement(content, symbol, tag)
    if len(replacement.strip()) > 0:
        return replacement
    else:
        return None
