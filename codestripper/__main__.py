from pathlib import Path

from codestripper.code_stripper import CodeStripper

if __name__ == '__main__':
    path = Path("Phonebook.java")
    with open(path) as file:
        content = file.read()
    stripper = CodeStripper(content)
    print(stripper.strip())
