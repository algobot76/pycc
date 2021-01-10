"""Pycc token."""

from __future__ import annotations

from enum import Enum, auto
from typing import Optional


class TokenKind(Enum):
    """Token kind.

    Attributes:
        TK_RESERVED: Keywords or punctuators.
        TK_IDENT: Identifiers
        TK_NUM: Numerical literals.
        TK_EOF: End-of-file markers.
    """

    TK_RESERVED = auto()
    TK_IDENT = auto()
    TK_NUM = auto()
    TK_EOF = auto()


class Token:
    """Token.

    The val attribute is used if its kind is TK_NUM.

    Attributes:
        kind: The token kind.
        next: The next token.
        val: The value of the token.
        loc: The start location within the program.
        len: The length of the program segment represented by the token.
    """

    def __init__(
        self,
        kind: TokenKind,
        *,
        next_: Optional[Token] = None,
        val: int = 0,
        start: int = 0,
        end: int = 0,
    ):
        self.kind = kind
        self.next = next_
        self.val = val
        self.loc = start
        self.len = end - start
