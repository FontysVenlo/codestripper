from dataclasses import dataclass
from typing import Optional, Dict, Iterable, Tuple


@dataclass(frozen=True)
class Comment:
    open: str
    close: Optional[str] = None

comments_mapping: Dict[str, Comment] = {
    ".java": Comment("//"),
    ".cs": Comment("//"),
    ".js": Comment("//"),
    ".php": Comment("//"),
    ".swift": Comment("//"),
    ".xml": Comment("<!--", "-->"),
    ".tex": Comment("%"),
    ".m": Comment("%"),
    ".sql": Comment("--"),
    ".lua": Comment("--"),
    ".ml": Comment("(*", "*)"),
    ".r": Comment("#"),
    ".py": Comment("#"),
    ".ps1": Comment("#"),
    ".rb": Comment("#"),
    ".yml": Comment("#"),
    ".yaml": Comment("#"),
    "": Comment("#"),  # Default comment style for unknown file types
}


def parse_comment(specification: str) -> Tuple[str, Comment]:
    """
    Parse a comment specification: <extension>:<open> or <extension>:<open>:<close> (e.g. .java://)

    :return: the (lowercase) extension and the comment
    :raises ValueError: if the specification is invalid
    """
    parts = specification.split(":")
    if len(parts) not in (2, 3) or any(len(part) == 0 for part in parts):
        raise ValueError(f"Invalid comment '{specification}', expected <extension>:<open> or "
                         f"<extension>:<open>:<close> (e.g. .java://)")
    extension = parts[0].lower()
    if not extension.startswith("."):
        raise ValueError(f"Invalid comment '{specification}', the extension '{parts[0]}' should start with a '.'")
    return extension, Comment(*parts[1:])


def get_comments_mapping(specifications: Optional[Iterable[str]] = None) -> Dict[str, Comment]:
    """Get a copy of the default comments mapping, extended (or overridden) by the given specifications"""
    mapping = dict(comments_mapping)
    for specification in specifications or []:
        extension, comment = parse_comment(specification)
        mapping[extension] = comment
    return mapping
