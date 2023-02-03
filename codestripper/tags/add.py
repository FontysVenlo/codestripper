from codestripper.tags.tag import SingleTag, TagData
from codestripper.tags.utils import calculate_replacement


class AddTag(SingleTag):
    regex = [r'cs:add:.*?$']

    def __init__(self, data: TagData) -> None:
        super().__init__(data)

    def execute(self, content: str) -> str:
        return calculate_replacement(content, ":", self)
