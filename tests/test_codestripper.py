import logging
import os.path
import re
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture

from codestripper.code_stripper import strip_files
from codestripper.utils import FileUtils

test_project_dir = os.path.join(Path(__file__).parent.absolute())


def test_project(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    with caplog.at_level(logging.INFO, logger='codestripper'):
        files = FileUtils(["testproject/**/*.java", "testproject/pom.xml"]).get_matching_files()
        strip_files(files, dry_run=True)
        stripped = [rec.message for rec in caplog.records]
        tags_in_content = False
        for content in stripped:
            if content.__contains__("//cs:"):
                tags_in_content = True
                break
        assert len(stripped) == 6 and not tags_in_content


def test_project_out(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(test_project_dir)
    files = FileUtils(["**/*.java", "pom.xml"], working_directory="testproject").get_matching_files()
    stripped_files = strip_files(files, "testproject", "//", "out", False)
    stripped = len(stripped_files) == 5
    regex = re.compile("//cs:")
    for file in stripped_files:
        with open(os.path.join(os.getcwd(), "out", file), 'r') as handle:
            content = handle.read()
            if regex.search(content) is not None:
                stripped = False
                break
    assert stripped


def test_log_missing_close_tag(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    files = FileUtils(["MissingClose.java"], working_directory="files").get_matching_files()
    with caplog.at_level(logging.ERROR, logger='codestripper'):
        strip_files(files, "files", "//", "out", True)
        errors = [rec.message for rec in caplog.records]
        assert len(errors) == 1 and "MissingClose.java" in errors[0] and "1" in errors[0]


def test_log_wrong_close_tag(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    files = FileUtils(["WrongClose.java"], working_directory="files").get_matching_files()
    with caplog.at_level(logging.ERROR, logger='codestripper'):
        strip_files(files, "files", "//", "out", True)
        errors = [rec.message for rec in caplog.records]
        assert len(errors) == 1 and "WrongClose.java" in errors[0] and "3" in errors[0]


def test_log_missing_open_tag(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    files = FileUtils(["MissingOpen.java"], working_directory="files").get_matching_files()
    with caplog.at_level(logging.ERROR, logger='codestripper'):
        strip_files(files, "files", "//", "out", True)
        errors = [rec.message for rec in caplog.records]
        assert len(errors) == 1 and "MissingOpen.java" in errors[0] and "1" in errors[0]


def test_log_invalid_tag(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    files = FileUtils(["InvalidTag.java"], working_directory="files").get_matching_files()
    with caplog.at_level(logging.ERROR, logger='codestripper'):
        strip_files(files, "files", "//", "out", True)
        errors = [rec.message for rec in caplog.records]
        assert len(errors) == 1 and "InvalidTag.java" in errors[0] and "2" in errors[0]
