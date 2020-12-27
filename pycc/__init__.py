"""Pycc"""
import sys

from pycc.codegen import CodeGen
from pycc.error import error, error_tok
from pycc.parser import Parser
from pycc.token import Token, TokenKind
from pycc.tokenizer import Tokenizer


def main(argv):
    if len(argv) != 2:
        error(f"{argv[0]} invalid number of arguments")

    prog = argv[1]
    tok: Token = Tokenizer.tokenize(prog)
    node = Parser.expr(tok, prog)

    if Parser.rest.kind != TokenKind.TK_EOF:
        error_tok(Parser.rest, prog, "extra token")

    print("  .globl main")
    print("main:")

    CodeGen.gen_expr(node)
    print("  ret")

    assert CodeGen.depth == 0


def run_main():
    main(sys.argv)


if __name__ == "__main__":
    run_main()
