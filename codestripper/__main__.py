from pathlib import Path

from codestripper.code_stripper import CodeStripper
from codestripper.utils import FileUtils

if __name__ == '__main__':
    files = FileUtils(["*.java"], [], recursive=False)
    stripper = CodeStripper("")
    print(stripper.strip())
