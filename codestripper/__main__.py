import argparse
import os
import sys
from typing import List

from codestripper.code_stripper import CodeStripper, strip_files
from codestripper.utils import FileUtils, set_logger_level, get_working_directory


def add_commandline_arguments(parser: argparse.ArgumentParser) -> None:
    """Add command line arguments"""
    # Add positional arguments
    parser.add_argument("include", nargs="+", help="files to include for code stripping (multiple files or glob)")
    # Add optional arguments
    parser.add_argument("-x", "--exclude", action="append",
                        help="files to include for code stripping (multiple files or glob)", default=[])
    parser.add_argument("-c", "--comment", action="store",
                        help="comment symbol(s) for the given language", default="//")
    parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity", default=0)
    parser.add_argument("-o", "--output", action="store",
                        help="the output directory to store the stripped files", default="out")
    parser.add_argument("-r", "--recursive", action="store_false",
                        help="use recursive globs for include/exclude")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="dry run of the codestripper, no output is written", default=False)
    parser.add_argument("-w", "--working-directory", action="store",
                        help="set the working directory, relative to pwd", default=os.getcwd())


def main(arguments: List[str]) -> None:
    """Parse the command line arguments, find all the files and strip the found files"""

    # Handle command line arguments
    parser = argparse.ArgumentParser()
    add_commandline_arguments(parser)
    args = parser.parse_args(arguments)

    # Setup the logger
    logger_name = "codestripper"
    set_logger_level(logger_name, args.verbosity)

    # Find the files, based on the command line arguments
    cwd = get_working_directory(args.working_directory)
    files = FileUtils(args.include, args.exclude, cwd, args.recursive, logger_name).get_matching_files()
    # Strip all the files
    strip_files(files, cwd, args.comment, args.output, args.dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
