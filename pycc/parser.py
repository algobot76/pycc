"""Pycc parser"""
from typing import Tuple

from pycc.ast import Node, NodeKind, new_binary, new_num
from pycc.error import error_tok
from pycc.token import Token, TokenKind
from pycc.tokenizer import Tokenizer
from pycc.utils import unwrap_optional


class Parser:
    """Pycc parser.

    The parser is a singleton and any call to its __init__ method will raise
    an exception.
    """

    _prog: str = ""

    def __init__(self):
        raise Exception("You cannot create an instance of Tokenizer")

    @classmethod
    def primary(cls, tok: Token) -> Tuple[Node, Token]:
        """Primary expression in parentheses.

        Args:
            tok: Token to analyze.
            prog: Program.

        Returns:
            A tuple
                Node: Node of the current token.
                Token: Token for the next token.
        """

        if Tokenizer.equal(tok, "("):
            next_tok = unwrap_optional(tok.next)
            node, tok = cls.expr(next_tok, cls._prog)
            rest = unwrap_optional(Tokenizer.skip(tok, ")"))
            return node, rest

        if tok.kind == TokenKind.TK_NUM:
            node = new_num(tok.val)
            rest = unwrap_optional(tok.next)
            return node, rest

        error_tok(tok, cls._prog, "expected an expression")
        return Node(NodeKind.ND_ADD, None, None, 0), tok  # dummy return

    @classmethod
    def mul(cls, tok: Token) -> Tuple[Node, Token]:
        """Multiplication expression node constructor.

        Args:
            tok: Token to analyze.
            prog: Program to analyze.

        Returns:
            A tuple
                Node: Node of the current token.
                Token: Token for the next token.
        """
        node, tok = cls.primary(tok)

        while True:
            if Tokenizer.equal(tok, "/"):
                pri_node, tok = cls.primary(unwrap_optional(tok.next))
                node = new_binary(NodeKind.ND_DIV, node, pri_node)
                continue
            if Tokenizer.equal(tok, "*"):
                pri_node, tok = cls.primary(unwrap_optional(tok.next))
                node = new_binary(NodeKind.ND_MUL, node, pri_node)
                continue

            rest = tok
            return node, rest

    @classmethod
    def expr(cls, tok: Token, prog: str) -> Tuple[Node, Token]:
        """Expression node constructor.

        Args:
            tok: Token to analyze.
            prog: Program to analyze.

        Returns:
            A tuple
                Node: Node of the current token.
                Token: Token for the next token.
        """
        cls._prog = prog

        node, tok = cls.mul(tok)
        while True:
            if Tokenizer.equal(tok, "+"):
                mul_node, tok = cls.mul(unwrap_optional(tok.next))
                node = new_binary(NodeKind.ND_ADD, node, mul_node)
                continue
            if Tokenizer.equal(tok, "-"):
                mul_node, tok = cls.mul(unwrap_optional(tok.next))
                node = new_binary(NodeKind.ND_SUB, node, mul_node)
                continue
            rest = tok
            return node, rest
