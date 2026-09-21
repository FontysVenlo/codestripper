import glob
import os
import logging
from pathlib import Path
from typing import Generator, Iterable, Set, Union


def get_working_directory(working_directory: Union[str, None]) -> str:
    """
    Get the absolute working directory, which should be (a subdirectory of) the current working directory

    :raises ValueError: if the working directory is not inside the current working directory
    """
    current = os.path.realpath(os.getcwd())
    if working_directory is None:
        return current
    # Resolve '..' and symbolic links first, so they cannot be used to escape the current directory
    cwd = os.path.realpath(os.path.join(current, working_directory))
    try:
        Path(cwd).relative_to(current)
    except ValueError:
        raise ValueError(f"Working directory '{working_directory}' is not inside the current directory '{current}'")
    return cwd


class FileUtils:
    def __init__(self,
                 included: Iterable[str],
                 excluded: Union[Iterable[str], None] = None,
                 working_directory: Union[str, None] = None,
                 recursive: bool = True,
                 logger: str = "codestripper"
                 ) -> None:
        self.logger = logging.getLogger(f"{logger}.fileutils")
        self.included = included
        if excluded is None:
            self.excluded: Iterable[str] = []
        else:
            self.excluded = excluded
        self.recursive = recursive
        self.cwd = get_working_directory(working_directory)

    def __get_normalized_files(self, file_names: Iterable[str], relative_to: Path, recursive=True) -> \
            Generator[str, None, None]:
        for file_name in file_names:
            # Only the given file name is a glob pattern, so escape the working directory to match it literally
            path = os.path.join(glob.escape(self.cwd), file_name)
            for file in glob.glob(path, recursive=recursive):
                # The found file is absolute, so no need to change the current directory to check it
                if Path(file).is_file():
                    yield str(Path(file).relative_to(relative_to))

    def __convert_to_paths_set(self, file_names: Iterable[str], recursive=True) -> Set[str]:
        """Convert the file name(s) that are passed as CLI arguments to file paths (can contain GLOB)"""
        files = set()
        for file in self.__get_normalized_files(file_names, Path(self.cwd), recursive):
            files.add(file)
        return files

    def get_matching_files(self) -> Iterable[str]:
        """Get files that fulfill requirements, match included and do not match excluded"""
        included_files = self.__convert_to_paths_set(self.included, self.recursive)
        self.logger.debug(f"Included files are: {included_files}")

        excluded_files = self.__convert_to_paths_set(self.excluded, self.recursive)
        self.logger.debug(f"Excluded files are: {excluded_files}")
        return included_files - excluded_files
