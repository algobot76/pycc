"""Pycc"""
import sys

from pycc.codegen import Codegen
from pycc.exception import PyccError, TokenError
from pycc.parser import Parser
from pycc.token import Token, TokenKind
from pycc.tokenizer import Tokenizer


def main(argv):
    if len(argv) != 2:
        raise PyccError(f"{argv[0]} invalid number of arguments")

    prog = argv[1]
    tok: Token = Tokenizer.tokenize(prog)
    node = Parser.parse(tok, prog)
    Codegen.codegen(node)


def run_main():
    try:
        main(sys.argv)
    except PyccError as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(1)


if __name__ == "__main__":
    run_main()
