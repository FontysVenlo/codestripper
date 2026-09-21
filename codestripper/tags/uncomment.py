import re
from functools import lru_cache
from typing import Union, Pattern, Optional, Tuple

from codestripper.tags.tag import RangeTag, RangeOpenTag, RangeCloseTag, TagData
from codestripper.utils.comments import Comment


@lru_cache(maxsize=None)
def _uncomment_patterns(comment: Comment) -> Tuple[Pattern, Optional[Pattern]]:
    """Regexes that remove the open (keeping the leading whitespace) and, if present, the close symbol of a comment"""
    open_pattern = re.compile(rf"(?P<whitespace>\s*){re.escape(comment.open)}")
    close_pattern = re.compile(re.escape(comment.close)) if comment.close is not None else None
    return open_pattern, close_pattern


class UncommentOpenTag(RangeOpenTag):
    regex = r'cs:uncomment:start(.*)?'

    def __init__(self, data: TagData) -> None:
        super().__init__(UncommentRangeTag, data)


class UncommentCloseTag(RangeCloseTag):
    regex = 'cs:uncomment:end(.*)?'

    def __init__(self, data: TagData) -> None:
        super().__init__(UncommentRangeTag, data)


class UncommentRangeTag(RangeTag):

    def __init__(self, open_tag: RangeOpenTag, close_tag: RangeCloseTag):
        super().__init__(open_tag, close_tag)

    def execute(self, content: str) -> Union[str, None]:
        open_pattern, close_pattern = _uncomment_patterns(self.open_tag.data.comment)
        lines = content[self.start:self.end]
        replacement = open_pattern.sub(r"\g<whitespace>", lines)
        if close_pattern is not None:
            replacement = close_pattern.sub("", replacement)
        return replacement
