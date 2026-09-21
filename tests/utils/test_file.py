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
        (["data/**/*"], [], True, ["data/test1.java", "data/test1.txt", "data/test2.txt", "data/recursive/test2.java",
                                   "data/recursive/test3.txt"]),
        (["data/test1*"], [], True, ["data/test1.java", "data/test1.txt"]),
        (["data/test1*"], ["**/*.txt"], True, ["data/test1.java"])
    ]
)
def test_glob(included: List[str], excluded: List[str], recursive: bool, expected: List[Path],
              monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    expected_paths = [str(Path(path)) for path in expected]
    files = FileUtils(included, excluded, working_directory=None, recursive=recursive).get_matching_files()
    difference = set(files) ^ set(expected_paths)
    assert not difference


def test_cwd(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    cwd = get_working_directory("data/recursive")
    files = FileUtils(["*.java"], working_directory=cwd).get_matching_files()
    assert len(files) == 1


def test_cwd_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    assert get_working_directory(None) == os.path.realpath(test_data_dir)


def test_cwd_absolute_inside(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    inside = test_data_dir / "data" / "recursive"
    assert get_working_directory(str(inside)) == os.path.realpath(inside)


def test_cwd_normalizes_inside_path(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    assert get_working_directory("data/recursive/..") == os.path.realpath(test_data_dir / "data")


@pytest.mark.parametrize("path", ["/etc/passwd", "..", "../other", "data/../../other"])
def test_non_relative(path: str, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)
    with pytest.raises(ValueError, match="is not inside the current directory"):
        get_working_directory(path)


@pytest.mark.skipif(os.name == "nt", reason="creating symbolic links requires extra privileges on Windows")
def test_symlink_outside_is_rejected(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    outside = tmp_path / "outside"
    outside.mkdir()
    inside = tmp_path / "inside"
    inside.mkdir()
    (inside / "link").symlink_to(outside, target_is_directory=True)
    monkeypatch.chdir(inside)
    with pytest.raises(ValueError, match="is not inside the current directory"):
        get_working_directory("link")


def test_does_not_change_current_directory(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_data_dir)

    def fail_on_chdir(path):
        raise AssertionError("The current directory should not be changed")

    monkeypatch.setattr(os, "chdir", fail_on_chdir)
    files = FileUtils(["*.java"], ["*.txt"], working_directory="data/recursive").get_matching_files()
    assert len(files) == 1
    assert os.getcwd() == str(test_data_dir)


def test_glob_characters_in_working_directory(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    special = tmp_path / "dir[1]"
    special.mkdir()
    (special / "a.java").write_text("class A {}")
    monkeypatch.chdir(tmp_path)
    files = FileUtils(["*.java"], working_directory="dir[1]").get_matching_files()
    assert set(files) == {"a.java"}
