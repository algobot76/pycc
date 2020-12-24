"""Pycc token"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TokenKind(Enum):
    """Represnets a token kind.

    Attributes:
        TK_RESERVED: Keywords or punctuators.
        TK_NUM: Numerical literals.
        TK_EOF: End-of-file markers.
    """

    TK_RESERVED = auto()
    TK_NUM = auto()
    TK_EOF = auto()


@dataclass
class Token:
    """Represents a token.

    Attributes:
        kind: Token kind.
        next: Next token.
        val: If kind is TK_NUM, its value.
        loc: Token location.
        len: Token length.
    """

    kind: TokenKind
    next: Optional[Token]
    val: int
    loc: int
    len: int


def new_token(kind: TokenKind, start: int = 0, end: int = 0) -> Token:
    """Creates a new token.

    Args:
        kind: Token kind.
        star: Start index of the token.
        end: End index of the token.

    Returns:
        A new token constructed with the given paramters.
    """

    return Token(kind, None, 0, start, end - start)
