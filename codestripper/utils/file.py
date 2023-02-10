import glob
import os
import logging
from pathlib import Path
from typing import Dict, Generator, Iterable, Set


class FileUtils:
    def __init__(self,
                 included: Iterable[str],
                 excluded: Iterable[str],
                 recursive: bool = True,
                 logger: str = "codestripper"
                 ) -> None:
        self.included = included
        self.excluded = excluded
        self.recursive = recursive
        self.cwd = os.getcwd()
        self.logger = logging.getLogger(f"{logger}.fileutils")

    def __get_normalized_files(self, file_names: Iterable[str], relative_to: Path, recursive=True) -> \
            Generator[Path, None, None]:
        for file_name in file_names:
            for file in glob.glob(Path(file_name).resolve().as_posix(), recursive=recursive):
                try:
                    tmp = Path(file).relative_to(relative_to)
                    if tmp.is_file():
                        yield tmp.as_posix()
                except ValueError:
                    self.logger.error(f"{file} is invalid, must be relative to {relative_to}")

    def __convert_to_paths_set(self, file_names: Iterable[str], recursive=True) -> Set[Path]:
        """Convert the file name(s) that are passed as CLI arguments to file paths (can contain GLOB)"""
        files = set()
        for file in self.__get_normalized_files(file_names, Path(os.getcwd()), recursive):
            files.add(file)
        return files

    def get_matching_files(self) -> Iterable[Path]:
        """Get files that fullfill requirements, match included and do not match excluded"""
        included_files = self.__convert_to_paths_set(self.included, self.recursive)
        self.logger.debug(f"Included files are: {included_files}")

        excluded_files = self.__convert_to_paths_set(self.excluded, self.recursive)
        self.logger.debug(f"Excluded files are: {excluded_files}")

        return included_files - excluded_files
