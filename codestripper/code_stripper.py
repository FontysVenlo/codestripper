from pathlib import Path
from typing import Optional, Union, Deque

from codestripper.errors import InvalidTagError
from codestripper.tags import IgnoreFileError, UncommentRangeTag
from codestripper.tags.tag import Tag, RangeTag
from codestripper.tokenizer import Tokenizer


class CodeStripper:

    def __init__(self, content: str, comment: str = "//") -> None:
        self.content = content
        self.comment = comment

    def strip(self) -> str:

        if self.content is not None:
            # Hack for now
            Tag.comment = self.comment
            tokenizer = Tokenizer(self.content, self.comment)
            tags = tokenizer.tokenize()
            self.__traverse(tags)
        return self.content
            # try:
            #     self.__traverse(tags)
            # except IgnoreFileError as ignored:
            #     print(f"File is ignored, because of IgnoreTag")
            # except InvalidTagError as invalid:
            #     print(invalid)
            # print(self.content)

    def __traverse(self, tags: Deque[Tag], offset=0) -> int:
        old_offset = offset
        if len(tags) == 0:
            return offset - old_offset
        for tag in tags:
            tag.offset = offset
            if isinstance(tag, RangeTag):
                changed = self.__traverse(tag.tags, offset)
                tag.inset = changed
                delta = self.__execute_tag(tag)
                tag.open_tag.offset = offset
                offset += self.__execute_tag(tag.open_tag)
                offset += delta + changed
                tag.close_tag.offset = offset
                offset += self.__execute_tag(tag.close_tag)
            else:
                offset += self.__execute_tag(tag)
        return offset - old_offset

    def __execute_tag(self, tag: Tag):
        if not tag.is_valid():
            raise InvalidTagError(tag)
        processed = tag.execute(self.content)
        old_size = tag.end - tag.start
        new_size = len(processed) if processed is not None else 0
        # print(f"({tag}) {processed}: size: {old_size} -> {new_size}")
        # print(repr(self.content[(tag.start+offset):(tag.start+new_size+offset)]))
        before = self.content[:tag.start]

        # Return of None means remove the complete line
        if processed is None:
            # Check if there is a newline at the end of the line
            # The tags don't capture newlines, so manually make sure to remove
            last_char = self.content[tag.end:tag.end+1]
            if "\n" in last_char:
                after = self.content[tag.end+1:]
                old_size += 1
            else:
                after = self.content[tag.end:]
            self.content = before + after
            return -1 * old_size
        else:
            after = self.content[tag.end:]
            self.content = before + processed + after
            return new_size - old_size
