from codestripper.tags.tag import Tag, RangeTag, SingleTag


class InvalidTagError(Exception):
    """Raise if the tag is not valid"""
    def __init__(self, tag: Tag):
        self.tag = tag

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        line_number = -1
        if isinstance(self.tag, RangeTag):
            line_number = self.tag.open_tag.data.line_number
        elif isinstance(self.tag, SingleTag):
            line_number = self.tag.data.line_number

        return f"Tag {self.tag.__class__.__name__} at line {line_number} is invalid"
