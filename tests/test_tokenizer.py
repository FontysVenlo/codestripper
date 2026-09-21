from codestripper.tags import RemoveTag
from codestripper.tokenizer import Tokenizer
from codestripper.utils.comments import Comment


def test_tokenizers_do_not_share_state():
    """A tokenizer that is created later should not change how an earlier tokenizer works"""
    slashes = Tokenizer("a\n//cs:remove\n", Comment("//"))
    hashes = Tokenizer("a\n#cs:remove\n", Comment("#"))

    hash_tags = hashes.tokenize()
    slash_tags = slashes.tokenize()

    assert len(slash_tags) == 1 and isinstance(slash_tags[0], RemoveTag)
    assert slash_tags[0].data.comment == Comment("//")
    assert len(hash_tags) == 1 and hash_tags[0].data.comment == Comment("#")

