import logging
import os.path
from pathlib import Path
from typing import Union, Iterable, List

from codestripper.errors import InvalidTagError
from codestripper.tags import IgnoreFileError
from codestripper.tags.tag import Tag, RangeTag
from codestripper.tokenizer import Tokenizer
from codestripper.utils import get_working_directory

logger = logging.getLogger("codestripper")


def strip_files(files: Iterable[str], working_directory: Union[str, None] = None, comment: str = "//",
                output: Union[Path, str] = "out", dry_run: bool = False) -> List[str]:
    cwd = get_working_directory(working_directory)
    out = os.path.join(os.getcwd(), output)
    stripped_files: List[str] = []
    for file in files:
        with open(os.path.join(cwd, file), 'r') as handle:
            content = handle.read()
        if content is not None:
            try:
                stripped = CodeStripper(content, comment).strip()
            except IgnoreFileError:
                logger.info(f"File '{file} is ignore, because of ignore tag'")
                continue
            stripped_files.append(file)
            if dry_run:
                logger.info(stripped)
            else:
                path = os.path.join(out, file)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w+') as handle:
                    handle.write(stripped)
    return stripped_files


class CodeStripper:

    def __init__(self, content: str, comment: str) -> None:
        self.content = content
        self.comment = comment

    def strip(self) -> str:

        if self.content is not None:
            tokenizer = Tokenizer(self.content, self.comment)
            tags = tokenizer.tokenize()
            self.__traverse(tags)
        return self.content

    def __traverse(self, tags: List[Tag], offset=0) -> int:
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
