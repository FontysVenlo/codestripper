import re

import pytest

from codestripper.tags import AddTag
from codestripper.tags.tag import TagData
from codestripper.tags.utils import calculate_replacement


def test_replacement():
    regex = re.compile("test")
    match = regex.search("test")
    data = TagData("test", 0, 0, match, "test")
    tag = AddTag(data)
    with pytest.raises(AssertionError) as ex:
        calculate_replacement("test", ":", tag)

