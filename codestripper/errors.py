from codestripper.tags.tag import Tag, RangeTag, SingleTag


def _line_number(tag: Tag) -> int:
    """The line the tag is on, for a range this is the line of the open tag"""
    if isinstance(tag, SingleTag):
        return tag.data.line_number
    if isinstance(tag, RangeTag):
        return tag.open_tag.data.line_number
    return -1


class StripError(Exception):
    """Raised when stripping one or more files failed, the details are logged"""


class InvalidTagError(Exception):
    """Raise if the tag is not valid"""
    def __init__(self, tag: Tag):
        self.tag = tag

    @property
    def line_number(self) -> int:
        return _line_number(self.tag)

    @property
    def message(self) -> str:
        return self.__str__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        message = f"Tag {self.tag.__class__.__name__} is invalid"
        if self.tag.invalid_reason:
            message += f": {self.tag.invalid_reason}"
        return message


class TokenizerError(Exception):

    def __init__(self, tag: Tag, message: str):
        self.tag = tag
        self.message = message

    @property
    def line_number(self) -> int:
        return _line_number(self.tag)
