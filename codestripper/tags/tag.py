import re
from dataclasses import dataclass
from typing import Type, Union, List, Pattern, Iterable


@dataclass
class TagData:
    line: str
    line_number: int
    line_start: int
    match: re.Match
    matched_regex: str

    @property
    def match_start(self):
        return self.match.start()

    @property
    def match_end(self):
        return self.match.end()

    @property
    def line_end(self):
        return self.match.end()

    def __repr__(self) -> str:
        return (f"{self.line}, line ({self.line_number}): {self.line_start}:{self.line_end},"
                f"match: {self.match_start}:{self.match_end}")


class Tag:
    comment = "//"

    def __init__(self) -> None:
        self._offset = 0

    def is_valid(self) -> bool:
        return True

    def execute(self, content: str) -> Union[str, None]:
        return None

    @property
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, offset: int) -> None:
        self._offset = offset

    @property
    def start(self) -> int:
        """Start position of the line in the file"""
        return -1

    @property
    def end(self) -> int:
        """End position of the line in the file"""
        return -1


class SingleTag(Tag):
    regex: List[str] = []

    def __init__(self, data: TagData) -> None:
        super().__init__()
        self.data = data

    def is_valid(self) -> bool:
        return len(self.regex) != 0

    @property
    def start(self) -> int:
        return self.data.line_start + self.offset

    @property
    def end(self) -> int:
        return self.data.line_end + self.offset


class RangeOpenTag(SingleTag):

    def __init__(self, parent: Type, data: TagData) -> None:
        super().__init__(data)
        self.parent = parent


class RangeCloseTag(SingleTag):

    def __init__(self, parent: Type, data: TagData) -> None:
        super().__init__(data)
        self.parent = parent


class RangeTag(Tag):

    def __init__(self, open_tag: RangeOpenTag, close_tag: RangeCloseTag) -> None:
        super().__init__()
        self.open_tag = open_tag
        self.close_tag = close_tag
        self.tags: List[Tag] = []
        self._inset = 0

    def add_tags(self, tags: Iterable[Tag]) -> None:
        self.tags.extend(tags)

    @property
    def inset(self) -> int:
        return self._inset

    @inset.setter
    def inset(self, inset: int) -> None:
        self._inset = inset

    @property
    def start(self) -> int:
        return self.open_tag.end + 1 + self.offset

    @property
    def end(self) -> int:
        return self.close_tag.start - 1 + self.offset + self.inset
