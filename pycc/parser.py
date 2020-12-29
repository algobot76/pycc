"""Pycc parser"""
from pycc.ast import Node, NodeKind, new_binary, new_num, new_unary
from pycc.error import TokenError
from pycc.token import Token, TokenKind
from pycc.tokenizer import Tokenizer
from pycc.utils import unwrap_optional


class Parser:
    """Pycc parser.

    The parser is a singleton and any call to its __init__ method will raise
    an exception.
    """

    _prog: str = ""
    rest: Token

    def __init__(self):
        raise Exception("You cannot create an instance of Parser")

    @classmethod
    def primary(cls, tok: Token) -> Node:
        """Primary expression in parentheses.

        Args:
            tok: Token to analyze.

        Returns:
            Node: Node of the current token.
        """

        if Tokenizer.equal(tok, "("):
            next_tok = unwrap_optional(tok.next)
            node = cls.expr(next_tok, cls._prog)
            cls.rest = unwrap_optional(Tokenizer.skip(cls.rest, ")"))
            return node

        if tok.kind == TokenKind.TK_NUM:
            node = new_num(tok.val)
            cls.rest = unwrap_optional(tok.next)
            return node

        raise TokenError(tok, cls._prog, "expected an expression")

    @classmethod
    def mul(cls, tok: Token) -> Node:
        """Multiplication expression node constructor.

        Args:
            tok: Token to analyze.

        Returns:
            Node: Node of the current token.
        """
        node = cls.unary(tok)

        while True:
            if Tokenizer.equal(cls.rest, "/"):
                unary_node = cls.unary(unwrap_optional(cls.rest.next))
                node = new_binary(NodeKind.ND_DIV, node, unary_node)
                continue
            if Tokenizer.equal(cls.rest, "*"):
                unary_node = cls.unary(unwrap_optional(cls.rest.next))
                node = new_binary(NodeKind.ND_MUL, node, unary_node)
                continue

            return node

    @classmethod
    def expr(cls, tok: Token, prog: str) -> Node:
        """Expression node constructor.

        Args:
            tok: Token to analyze.
            prog: Program to analyze.

        Returns:
            Node: Node of the current token.
        """
        cls._prog = prog

        node = cls.mul(tok)
        while True:
            if Tokenizer.equal(cls.rest, "+"):
                mul_node = cls.mul(unwrap_optional(cls.rest.next))
                node = new_binary(NodeKind.ND_ADD, node, mul_node)
                continue
            if Tokenizer.equal(cls.rest, "-"):
                mul_node = cls.mul(unwrap_optional(cls.rest.next))
                node = new_binary(NodeKind.ND_SUB, node, mul_node)
                continue
            return node

    @classmethod
    def unary(cls, tok: Token) -> Node:
        """Constructs a new unary node.

        unary = ("+" | "-") unary | primary

        Args:
            tok: Token to be parsed.

        Returns:
            A new unary node.
        """

        if Tokenizer.equal(tok, "+"):
            return cls.unary(unwrap_optional(tok.next))

        if Tokenizer.equal(tok, "-"):
            return new_unary(NodeKind.ND_NEG, cls.unary(unwrap_optional(tok.next)))

        return cls.primary(tok)
