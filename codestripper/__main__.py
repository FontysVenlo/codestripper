import argparse

from codestripper.code_stripper import CodeStripper
from codestripper.utils import FileUtils, set_logger_level


def add_commandline_arguments(parser: argparse.ArgumentParser) -> any:
    """Add command line arguments"""
    # Add positional arguments
    parser.add_argument("include", nargs="+", help="files to include for code stripping (multiple files or glob)")
    # Add optional arguments
    parser.add_argument("-x", "--exclude", action="append", help="files to include for code stripping (multiple files or glob)", default=[])
    parser.add_argument("-c", "--comment", action="store", help="comment symbol(s) for the given language", default="//")
    parser.add_argument("-v", "--verbosity", action="count", help="increase output verbosity", default=0)
    parser.add_argument("-o", "--output", action="store", help="the output directory to store the stripped files", default="out")
    parser.add_argument("-r", "--recursive", action="store_true", help="use recursive globs for include/exclude", default=True)
    return parser.parse_args()


def main() -> None:
    """Parse the command line arguments, find all the files and strip the found files"""

    # Handle command line arguments
    parser = argparse.ArgumentParser()
    args = add_commandline_arguments(parser)

    # Setup the logger
    logger = "codestripper"
    set_logger_level(logger, args.verbosity)

    # Find the files, based on the command line arguments
    files = FileUtils(args.include, args.exclude, args.recursive, logger).get_matching_files()

    # Strip all the files
    for file in files:

        CodeStripper(file, args.comment).strip()


if __name__ == '__main__':
    main()
