import glob
import logging
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from _pytest.logging import LogCaptureFixture

from codestripper.cli import main

test_project_dir = os.path.join(Path(__file__).parent.absolute())


def test_main(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    shutil.rmtree("out", ignore_errors=True)
    args = ["filename", "-c", ".test:!!", "-c", ".cs:#", "-x", "*.class", "-vv", "-o", "out", "-w", "testproject", "**/*.java"]
    with patch.object(sys, 'argv', args):
        with caplog.at_level(logging.INFO, logger='codestripper'):
            main()
            info = [rec.message for rec in caplog.records]
    files = glob.glob("out/**/*.java", recursive=True)
    assert len(info) == 1 and len(files) == 4



def test_main_unknown_include(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "file.unknownext").write_text("content")
    monkeypatch.chdir(tmp_path)
    args = ["codestripper", "-u", "include", "-o", "out", "file.unknownext"]
    with patch.object(sys, 'argv', args):
        main()
    assert (tmp_path / "out" / "file.unknownext").is_file()


def test_main_unknown_ignore(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    (tmp_path / "file.unknownext").write_text("content")
    monkeypatch.chdir(tmp_path)
    args = ["codestripper", "-u", "ignore", "-o", "out", "file.unknownext"]
    with patch.object(sys, 'argv', args):
        main()
    assert not (tmp_path / "out" / "file.unknownext").exists()


def test_main_binary_include(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_project_dir)
    shutil.rmtree("out", ignore_errors=True)
    args = ["codestripper", "-b", "include", "-o", "out", "-w", "testproject", "test.jpg"]
    with patch.object(sys, 'argv', args):
        main()
    assert os.path.isfile("out/test.jpg")


def test_main_binary_ignore(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_project_dir)
    shutil.rmtree("out", ignore_errors=True)
    args = ["codestripper", "-b", "ignore", "-o", "out", "-w", "testproject", "test.jpg"]
    with patch.object(sys, 'argv', args):
        main()
    assert not os.path.exists("out/test.jpg")


def test_main_invalid_choice(monkeypatch: pytest.MonkeyPatch):
    args = ["codestripper", "-b", "nonsense", "test.jpg"]
    with patch.object(sys, 'argv', args):
        with pytest.raises(SystemExit):
            main()
