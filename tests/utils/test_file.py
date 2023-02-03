import os
from pathlib import Path
from typing import List

import pytest

from codestripper.utils import FileUtils


@pytest.mark.parametrize(
    "included, excluded, recursive, expected",
    [
        (["**/*.java"], [], True, ["data/test1.java", "data/recursive/test2.java"]),
        (["**/*.java"], [], False, ["data/test1.java"]),
        (["*.java"], [], False, []),
        (["*.java"], [], True, []),
        (["**/*.java"], ["data/recursive/*.java"], False, ["data/test1.java"]),
        (["**/*.java"], ["data/*.java"], True, ["data/recursive/test2.java"]),
        (["**/*.java"], ["data/*.java"], False, []),
        (["data/**/*"], [], True, ["data/test1.java", "data/test1.txt", "data/test2.txt", "data/recursive/test2.java", "data/recursive/test3.txt"]),
        (["data/test1*"], [], True, ["data/test1.java", "data/test1.txt"]),
        (["data/test1*"], ["**/*.txt"], True, ["data/test1.java"])
    ]
)
def test_glob(included: List[str], excluded: List[str], recursive: bool, expected: List[Path]):
    files = FileUtils(included, excluded, recursive).get_matching_files()
    print(files)
    print(expected)
    difference = set(files) ^ set(expected)
    assert not difference

