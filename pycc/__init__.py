"""Pycc"""
import sys

from pycc.error import error
from pycc.token import TokenKind
from pycc.tokenizer import Tokenizer


def main(argv):
    if len(argv) != 2:
        error(f"{argv[0]} invalid number of arguments")

    prog = argv[1]
    tok = Tokenizer.tokenize(prog)

    print("  .globl main")
    print("main:")

    # The first token must be a number.
    print(f"  mov ${Tokenizer.get_number(tok)}, %rax")
    tok = tok.next

    # ... followed by either `+ <number>` or `- <number>`.
    while tok.kind != TokenKind.TK_EOF:
        if Tokenizer.equal(tok, "+"):
            print(f"  add ${Tokenizer.get_number(tok.next)}, %rax")
            tok = tok.next.next
            continue

        tok = Tokenizer.skip(tok, "-")
        print(f"  sub ${Tokenizer.get_number(tok)}, %rax")
        tok = tok.next

    print("  ret")


def run_main():
    main(sys.argv)


if __name__ == "__main__":
    run_main()
