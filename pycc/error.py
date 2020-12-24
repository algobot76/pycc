"""Pycc error handling"""
import sys

from pycc.token import Token


def error(msg: str):
    """Writes the error message to stderr then exits.

    Args:
        msg: An error message.
    """

    sys.stderr.write(f"{msg}\n")
    sys.exit(1)


def verror_at(pos: int, prog: str, msg: str):
    """Writes the error at a specific place to stderr then exits.

    Args:
        pos: Position of where the error is
        prog: The program where the error is
        msg: An error message.
    """
    sys.stderr.write(f"{prog}\n")
    sys.stderr.write(" " * pos)
    sys.stderr.write("^ ")
    sys.stderr.write(f"{msg}\n")
    sys.exit(1)


def error_at(pos: int, prog: str, msg: str):
    """Specifies a general error at a specific place to verror_at

    Args:
        pos: Position of where the error is
        prog: The program where the error is
        msg: An error message.
    """
    verror_at(pos, prog, msg)


def error_tok(tok: Token, prog: str, msg: str):
    """Specifies a error when consuming a token at a specific place to verror_at

    Args:
        tok: The token
        prog: The program where the error is
        msg: An error message.
    """
    verror_at(tok.loc, prog, msg)
