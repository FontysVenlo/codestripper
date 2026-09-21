from typing import Union

from codestripper.tags.errors import IgnoreFileError
from codestripper.tags.tag import SingleTag, TagData


class IgnoreFileTag(SingleTag):
    invalid_reason = "the ignore tag is only allowed on the first line"
    # Not followed by a word character or ':', so 'cs:ignored' or 'cs:ignore:<something>' are not this tag
    regex = r'cs:ignore(?![\w:])'

    def __init__(self, data: TagData) -> None:
        super().__init__(data)

    def is_valid(self) -> bool:
        return self.data.line_number == 1

    def execute(self, content: str) -> Union[str, None]:
        raise IgnoreFileError(self)
