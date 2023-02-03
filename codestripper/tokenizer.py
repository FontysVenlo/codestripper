import re
from collections import deque
from typing import Optional, Set, Dict, Callable, List, Pattern, Type, Tuple, Deque

from codestripper.tags import ReplaceTag, UncommentCloseTag, IgnoreFileTag, RemoveOpenTag, RemoveCloseTag, \
    UncommentOpenTag, LegacyOpenTag, LegacyCloseTag, RemoveTag, AddTag
from codestripper.tags.tag import SingleTag, Tag, RangeOpenTag, RangeCloseTag, RangeTag, TagData

tags: Set[type] = {
    IgnoreFileTag,
    RemoveOpenTag,
    RemoveCloseTag,
    RemoveTag,
    ReplaceTag,
    UncommentOpenTag,
    UncommentCloseTag,
    LegacyOpenTag,
    LegacyCloseTag,
    AddTag
}

# Type for lambda that creates a tag based on the type
CreateTagLambda = Callable[[TagData, Type], SingleTag]
# Type for mapping of name to CreateTagLambda
CreateTagMapping = Dict[str, CreateTagLambda]


def calculate_mappings(comment) -> Tuple[CreateTagMapping, Pattern]:
    strings = [r"(?P<newline>\n)"]
    mappings = {}
    for tag in tags:
        if issubclass(tag, SingleTag):
            for idx, reg in enumerate(tag.regex):
                name = f"{tag.__name__}{idx}"
                mappings[name] = lambda data, tag=tag: tag(data)
                strings.append(f"(?P<{name}>{comment}{reg})")
        else:
            print(f"Mapping is ony for single tags: {tag}")
    regex = re.compile("|".join(strings), flags=re.MULTILINE)
    return mappings, regex


class Tokenizer:
    mappings: Dict[str, Callable[[str, int, re.Match, Type], SingleTag]] = {}
    regex: Pattern = {}

    def __init__(self, content: str, comment: str) -> None:
        self.content = content
        self.comment = comment
        self.ordered_tags: Deque[Tag] = deque()
        self.open_stack: List[RangeOpenTag] = []
        self.range_stack: Dict[int, Optional[List[Tag]]] = {}
        if len(Tokenizer.mappings) == 0:
            Tokenizer.mappings, Tokenizer.regex = calculate_mappings(self.comment)

    def tokenize(self) -> Deque[Tag]:
        line_number = 1
        line_start = 0
        for match in self.regex.finditer(self.content):
            kind = match.lastgroup
            column_end = match.end()
            if kind == "newline":
                line_number += 1
                line_start = column_end
            else:
                # print(f"kind: {kind}, value: {value}, line: {line_number}({line_start}):{column_start}-{column_end}")
                data: TagData = TagData(self.content[line_start:column_end], line_number, line_start, match, kind)
                tag = Tokenizer.mappings[kind](data)
                self.__handle_tag(tag)
        if len(self.open_stack) != 0 or len(self.range_stack) != 0:
            raise AssertionError("Stack not empty!")
        return self.ordered_tags

    def __add_range_stack(self, index: int, tag: Tag) -> None:
        if index not in self.range_stack:
            self.range_stack[index] = []
        self.range_stack[index].append(tag)

    def __handle_tag(self, tag: Tag) -> None:
        if isinstance(tag, RangeOpenTag):
            self.open_stack.append(tag)
        elif isinstance(tag, RangeCloseTag):
            if len(self.open_stack) == 0:
                raise AssertionError("Stack is empty")
            range_open = self.open_stack.pop()
            if range_open.parent != tag.parent:
                raise ValueError(f"Cannot match closing tag: {tag} to open tag: {range_open}")
            range_tag: RangeTag = tag.parent(range_open, tag)
            index = len(self.open_stack)
            embedded = self.range_stack.pop(index + 1, None)
            if embedded is not None:
                range_tag.add_tags(embedded)

            if index > 0:
                self.__add_range_stack(index, range_tag)
            else:
                self.ordered_tags.append(range_tag)
        else:
            index: int = len(self.open_stack)
            if index > 0:
                self.__add_range_stack(index, tag)
            else:
                self.ordered_tags.append(tag)
