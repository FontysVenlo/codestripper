from typing import Optional

from codestripper.tags.tag import SingleTag, TagData
from codestripper.tags.utils import calculate_add


class AddTag(SingleTag):
    regex = r'cs:add:.*?$'

    def __init__(self, data: TagData) -> None:
        super().__init__(data)

    def execute(self, content: str) -> Optional[str]:
        return calculate_add(content, ":", self)
