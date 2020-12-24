"""Pycc"""
import sys
from typing import Optional

from pycc.error import error, error_tok
from pycc.token import Token, TokenKind
from pycc.tokenizer import tokenize


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
        if prog[i + tok.loc] != s[i]:
            return False

    return True


def skip(tok: Token, prog: str, s: str) -> Optional[Token]:
    """Ensures that the current token is `s`.

    Args:
        tok: A token.
        prog: The program's source code.
        s: A string to be comapred with.

    Returns:
        The token that matches `s`.
    """

    if not equal(tok, prog, s):
        error(f"expected '{s}'")

    return tok.next


def get_number(tok: Token, prog: str) -> int:
    """Ensures the current token is TK_NUM.

    Args:
        tok: A token.

    Returns:
        The token's value if it is TK_NUM.
    """

    if tok.kind is not TokenKind.TK_NUM:
        error_tok(tok, prog, "expected a number")
    return tok.val


def main(argv):
    if len(argv) != 2:
        error(f"{argv[0]} invalid number of arguments")

    prog = argv[1]
    tok = tokenize(prog)

    print("  .globl main")
    print("main:")

    # The first token must be a number.
    print(f"  mov ${get_number(tok, prog)}, %rax")
    tok = tok.next

    # ... followed by either `+ <number>` or `- <number>`.
    while tok.kind != TokenKind.TK_EOF:
        if equal(tok, prog, "+"):
            print(f"  add ${get_number(tok.next, prog)}, %rax")
            tok = tok.next.next
            continue

        tok = skip(tok, prog, "-")
        print(f"  sub ${get_number(tok, prog)}, %rax")
        tok = tok.next

    print("  ret")


def run_main():
    main(sys.argv)


if __name__ == "__main__":
    run_main()
