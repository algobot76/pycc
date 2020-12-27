"""Pycc"""
import sys

from pycc.ast import expr
from pycc.code_generator import CodeGenerator
from pycc.error import error, error_tok
from pycc.token import Token, TokenKind
from pycc.tokenizer import Tokenizer


def main(argv):
    if len(argv) != 2:
        error(f"{argv[0]} invalid number of arguments")

    prog = argv[1]
    tok: Token = Tokenizer.tokenize(prog)
    node, tok = expr(tok, prog)

    if tok.kind != TokenKind.TK_EOF:
        error_tok(tok, prog, "extra token")

    print("  .globl main")
    print("main:")

    CodeGenerator.gen_expr(node)
    print("  ret")

    assert CodeGenerator.depth == 0


def run_main():
    main(sys.argv)


if __name__ == "__main__":
    run_main()
