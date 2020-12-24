"""Pycc tokenizer"""
from typing import Optional

from pycc.error import error, error_at, error_tok
from pycc.token import Token, TokenKind, new_token


class Tokenizer:
    """Pycc tokenizer.

    The tokenizer is a singleton and any call to its __init__ method will raise
    an exception.
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
            elif ch in ("+", "-"):
                # Punctuator
                cur.next = new_token(TokenKind.TK_RESERVED, idx, idx + 1)
                idx += 1
            else:
                error_at(idx, cls._prog, "invalid token")

            cur = cur.next  # type: ignore

        cur.next = new_token(TokenKind.TK_EOF, idx, idx)
        return head.next

    @classmethod
    def equal(cls, tok: Token, s: str) -> bool:
        """Consumes the current token if it matches `s`.

        Args:
            tok: A token.
            s: A string to be comapred with.

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
            tok: A token.
            prog: The program's source code.
            s: A string to be comapred with.

        Returns:
            The token that matches `s`.
        """

        if not cls.equal(tok, s):
            error(f"expected '{s}'")

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
            error_tok(tok, cls._prog, "expected a number")
        return tok.val