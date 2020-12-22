from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenKind(Enum):
    TK_RESERVED = auto()
    TK_NUM = auto()
    TK_EOF = auto()


@dataclass
class Token:
    kind: TokenKind
    next: Token
    val: int
    loc: Any
    len: int


def equal(tok: Token, s: str) -> bool:
    """Consumes the current token if it matches `s`.

    Args:
        tok: A token.
        s: A string to be comapred with.

    Returns:
        A bool that indicates if the match exists.
    """

    pass


def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"{sys.argv[0]} invalid number of arguments\n")
        exit(1)

    params = sys.argv[1]
    numbers = re.findall(r'\d+', params)
    operators = re.findall(r'[\/\+\-\*]', params)

    print("  .globl main")
    print("main:")
    print(f"  mov ${numbers[0]}, %rax")

    for i in range(len(operators)):
        if operators[i] == "+":
            print(f"  add ${numbers[i+1]}, %rax")
        elif operators[i] == "-":
            print(f"  sub ${numbers[i+1]}, %rax")
        else:
            sys.stderr.write(f"unexpected character: {operators[i]}")

    print("  ret")
