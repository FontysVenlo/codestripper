import os
from pathlib import Path
from typing import List

import pytest

from codestripper.utils import FileUtils, get_working_directory

test_data_dir = Path(__file__).parent.absolute()


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
def test_glob(included: List[str], excluded: List[str], recursive: bool, expected: List[Path], monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    files = FileUtils(included, excluded, working_directory=None, recursive=recursive).get_matching_files()
    difference = set(files) ^ set(expected)
    assert not difference


def test_cwd(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    cwd = get_working_directory("data/recursive")
    files = FileUtils(["*.java"], working_directory=cwd).get_matching_files()
    print(files)
    assert len(files) == 1


def test_non_relative(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    with pytest.raises(ValueError) as ex:
        get_working_directory("/etc/passwd")
