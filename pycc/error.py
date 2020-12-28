"""Pycc error handling"""
import sys

from pycc.token import Token


class PyccError(Exception):
    """Base class for Pycc exceptions."""


class GeneralError(PyccError):
    """General error.

    Args:
        pos: Position of where the error is.
        prog: The program where the error is.
        msg: An error message.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, pos: int, prog: str, msg: str):
        self.pos = pos
        self.prog = prog
        self.msg = msg

    def __str__(self):
        return verror_msg(self.pos, self.prog, self.msg)


class TokenError(PyccError):
    """Token error.

    Raise this exception if a token-related error occurs.


    Attributes:
        tok: The token.
        prog: The program where the error is.
        msg: An error message.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, tok: Token, prog: str, msg: str):
        self.tok = tok
        self.prog = prog
        self.msg = msg

    def __str__(self):
        return verror_msg(self.tok.loc, self.prog, self.msg)


def verror_msg(pos: int, prog: str, msg: str) -> str:
    """Returns the formatted error message for the given paramters.

    Args:
        pos: Position of where the error is.
        prog: The program where the error is.
        msg: An error message.
    """

    result = f"{prog}\n"
    result += " " * pos
    result += "^ "
    result += f"{msg}"

    return result


def error(msg: str):
    """Writes the error message to stderr then exits.

    Args:
        msg: An error message.
    """

    sys.stderr.write(f"{msg}\n")
    sys.exit(1)
