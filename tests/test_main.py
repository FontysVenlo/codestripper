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
    args = ["filename", "-c", "//", "-x", "*.class", "-vv", "-o", "out", "-w", "testproject", "**/*.java"]
    with patch.object(sys, 'argv', args):
        with caplog.at_level(logging.INFO, logger='codestripper'):
            main()
            info = [rec.message for rec in caplog.records]
    files = glob.glob("out/**/*.java", recursive=True)
    assert len(info) == 1 and len(files) == 4

