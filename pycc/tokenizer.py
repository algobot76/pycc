"""Pycc tokenizer."""

import string
from typing import Optional

from pycc.exception import GeneralError, PyccError, TokenError
from pycc.token import Token, TokenKind, new_token


class Tokenizer:
    """Pycc tokenizer.

    The tokenizer is a singleton and any call to its __init__ method
    will raise an exception. Call its tokenize method to translate a program into
    a linked list of tokens.
    """

    _prog: str = ""

    def __init__(self):
        raise Exception("You cannot create an instance of Tokenizer")

    @classmethod
    def tokenize(cls, prog: str) -> Optional[Token]:
        """Tokenizes the `prog` and return new tokens.

        Args:
            prog: The program to be tokenized.

        Returns:
            Tokens that represent the program.
        """

        cls._prog = prog
        head = Token(TokenKind.TK_RESERVED, None, 0, 0, 0)  # Dummy
        cur = head

        n = len(cls._prog)
        idx = 0
        while idx < n:
            ch = cls._prog[idx]
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
                    ch = cls._prog[idx]
                cur.next.val = int(num)
                cur.next.len = idx - old_idx
            elif (
                cls._peak(idx, idx + 2) == ("==")
                or cls._peak(idx, idx + 2) == ("!=")
                or cls._peak(idx, idx + 2) == ("<=")
                or cls._peak(idx, idx + 2) == (">=")
            ):
                # Multi-letter punctuators
                cur.next = new_token(TokenKind.TK_RESERVED, idx, idx + 2)
                idx += 2
            elif ch in string.punctuation:
                # Single-letter punctuators
                cur.next = new_token(TokenKind.TK_RESERVED, idx, idx + 1)
                idx += 1
            else:
                raise GeneralError(idx, cls._prog, "invalid token")

            cur = cur.next  # type: ignore

        cur.next = new_token(TokenKind.TK_EOF, idx, idx)
        return head.next

    @classmethod
    def equal(cls, tok: Token, s: str) -> bool:
        """Consumes the current token if it matches `s`.

        Args:
            tok: The token to be compared with.
            s: The string to be comapred with.

        Returns:
            A bool that indicates if the match exists.
        """

        if tok.len != len(s):
            return False

        for i in range(tok.len):
            if cls._prog[i + tok.loc] != s[i]:
                return False

        return True

    @classmethod
    def skip(cls, tok: Token, s: str) -> Optional[Token]:
        """Ensures that the current token is `s`.

        Args:
            tok: The token to be compared with.
            prog: The program's source code.
            s: The string to be comapred with.

        Returns:
            The token that matches `s`.
        """

        if not cls.equal(tok, s):
            raise PyccError(f"expected '{s}'")

        return tok.next

    @classmethod
    def get_number(cls, tok: Token) -> int:
        """Ensures the current token is TK_NUM.

        Args:
            tok: A token.

        Returns:
            The token's value if it is TK_NUM.
        """

        if tok.kind is not TokenKind.TK_NUM:
            raise TokenError(tok, cls._prog, "expected a number")
        return tok.val

    @classmethod
    def _peak(cls, start: int, end: int) -> str:
        return cls._prog[start:end]
