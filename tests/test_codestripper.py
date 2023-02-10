import logging
import os.path
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
        strip_files(files, os.getcwd(), "//", "out", dry_run=True)
        stripped = [rec.message for rec in caplog.records]
        tags_in_content = False
        for content in stripped:
            if content.__contains__("//cs:"):
                tags_in_content = True
                break
        assert len(stripped) == 5 and not tags_in_content


def test_project_out(monkeypatch: pytest.MonkeyPatch, caplog: LogCaptureFixture):
    monkeypatch.chdir(test_project_dir)
    files = FileUtils(["**/*.java", "pom.xml"], working_directory="testproject").get_matching_files()
    strip_files(files, "//", "out", False)
