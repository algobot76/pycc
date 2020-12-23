from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum, auto


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
    next: Token
    val: int
    loc: int
    len: int


def error(msg: str):
    """Writes the error message to stderr then exits.

    Args:
        msg: An error message.
    """

    sys.stderr.write(f"{msg}\n")
    exit(1)


def equal(tok: Token, prog: str, s: str) -> bool:
    """Consumes the current token if it matches `s`.

    Args:
        tok: A token.
        prog: The program's source code.
        s: A string to be comapred with.

    Returns:
        A bool that indicates if the match exists.
    """

    if tok.len != len(s):
        return False

    for i in range(tok.len):
        if prog[i+tok.loc] != s[i]:
            return False

    return True


def skip(tok: Token, prog: str, s: str) -> Token:
    """Ensures that the current token is `s`.

    Args:
        tok: A token.
        prog: The program's source code.
        s: A string to be comapred with.

    Returns:
        The token that matches `s`.
    """

    if not equal(tok, prog, s):
        error(f"expected \'{s}\'")

    return tok.next


def get_number(tok: Token) -> int:
    """Ensures the current token is TK_NUM.

    Args:
        tok: A token.

    Returns:
        The token's value if it is TK_NUM.
    """

    if tok.kind is not TokenKind.TK_NUM:
        error("expected a number")
    return tok.val


def new_token(kind: TokenKind, start: int = 0, end: int = 0) -> Token:
    """Creates a new token.

    Args:
        kind: Token kind.
        star: Start index of the token.
        end: End index of the token.

    Returns:
        A new token constructed with the given paramters.
    """

    return Token(kind, None, 0, start, end-start)


def tokenize(prog: str) -> Token:
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
            num = ''
            while ch.isdigit():
                num += ch
                idx += 1
                if idx == n:
                    break
                ch = prog[idx]
            cur.next.val = int(num)
            cur.next.len = idx - old_idx
        elif ch == "+" or ch == "-":
            # Punctuator
            cur.next = new_token(TokenKind.TK_RESERVED, idx, idx+1)
            idx += 1
        else:
            error("invalid token")

        cur = cur.next

    cur.next = new_token(TokenKind.TK_EOF)
    return head.next


def print_tokens(tok: Token):
    """Prints the tokens.

    This function is used for debugging only.

    Args:
        tok: A token to start with.
    """
    cur = tok
    while cur:
        if cur.next:
            next_kind = cur.next.kind
        else:
            next_kind = None
        print(
            f"Token(kind={cur.kind}, next={next_kind}, val={cur.val}, loc={cur.loc}, len={cur.len})")
        cur = cur.next


def main():
    if len(sys.argv) != 2:
        error(f"{sys.argv[0]} invalid number of arguments")

    prog = sys.argv[1]
    tok = tokenize(prog)

    print("  .globl main")
    print("main:")

    # The first token must be a number.
    print(f"  mov ${get_number(tok)}, %rax")
    tok = tok.next

    # ... followed by either `+ <number>` or `- <number>`.
    while tok.kind != TokenKind.TK_EOF:
        if equal(tok, prog,  "+"):
            print(f"  add ${get_number(tok.next)}, %rax")
            tok = tok.next.next
            continue

        tok = skip(tok, prog, "-")
        print(f"  sub ${get_number(tok)}, %rax")
        tok = tok.next

    print("  ret")
