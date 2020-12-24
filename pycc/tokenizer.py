"""Pycc tokenizer"""
from typing import Optional

from pycc.error import error_at
from pycc.token import Token, TokenKind, new_token


def tokenize(prog: str) -> Optional[Token]:
    """Tokenizes the `prog` and return new tokens.

    Args:
        prog: The program to be tokenized.

    Returns:
        Tokens that represent the program.
    """

    head = Token(TokenKind.TK_RESERVED, None, 0, 0, 0)  # Dummy
    cur = head

    n = len(prog)
    idx = 0
    while idx < n:
        ch = prog[idx]
        if ch.isspace():
            # Skip spaces
            idx += 1
            continue
        elif ch.isdigit():
            # Numerical literal
            cur.next = new_token(TokenKind.TK_NUM, idx, idx)
            old_idx = idx
            num = ""
            while ch.isdigit():
                num += ch
                idx += 1
                if idx == n:
                    break
                ch = prog[idx]
            cur.next.val = int(num)
            cur.next.len = idx - old_idx
        elif ch in ("+", "-"):
            # Punctuator
            cur.next = new_token(TokenKind.TK_RESERVED, idx, idx + 1)
            idx += 1
        else:
            error_at(idx, prog, "invalid token")

        cur = cur.next  # type: ignore

    cur.next = new_token(TokenKind.TK_EOF, idx, idx)
    return head.next
