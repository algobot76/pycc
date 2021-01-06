"""Debug utilities"""
from typing import Optional

from pycc.token import Token, TokenKind


def print_tokens(tok: Token):
    """Prints the tokens.

    It takes the head of a linked list of tokens and prints all the tokens. This
    function is used for debugging only.

    Args:
        tok: The token to start with.
    """

    cur: Optional[Token] = tok
    while cur:
        next_kind: Optional[TokenKind] = None
        if cur.next:
            next_kind = cur.next.kind
        print(
            f"Token(kind={cur.kind}, next={next_kind}, val={cur.val}, "
            f"loc={cur.loc}, len={cur.len})"
        )
        cur = cur.next
