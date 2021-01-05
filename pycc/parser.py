"""Pycc parser"""
from pycc.ast import Node, NodeKind, new_binary, new_num, new_unary
from pycc.exception import TokenError
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
    def expr(cls, tok: Token, prog: str) -> Node:
        """Parses expressions.

        Args:
            tok: Token to be parsed.
            prog: Source code to be parsed.

        Returns:
            Node of the AST.
        """

        cls._prog = prog
        return cls.equality(tok)

    @classmethod
    def equality(cls, tok: Token) -> Node:
        """Parses relational expressions.

        equality = relational ("==" relational | "!=" relational)*

        Args:
            tok: Token to be parsed.

        Returns:
            A new binary node.
        """

        node = cls.relational(tok)

        while True:
            if Tokenizer.equal(cls.rest, "=="):
                node = new_binary(
                    NodeKind.ND_EQ, node, cls.relational(unwrap_optional(cls.rest.next))
                )
                continue

            if Tokenizer.equal(cls.rest, "!="):
                node = new_binary(
                    NodeKind.ND_NE, node, cls.relational(unwrap_optional(cls.rest.next))
                )
                continue

            return node

    @classmethod
    def relational(cls, tok: Token) -> Node:
        """Parses relational operators.

        relational = add ("<" add | "<=" add | ">" add | ">=" add)*

        Args:
            tok: Token to be parsed.

        Returns:
            A new relational node.
        """

        node = cls.add(tok)

        while True:
            if Tokenizer.equal(cls.rest, "<"):
                node = new_binary(
                    NodeKind.ND_LT, node, cls.add(unwrap_optional(cls.rest.next))
                )
                continue

            if Tokenizer.equal(cls.rest, "<="):
                node = new_binary(
                    NodeKind.ND_LE, node, cls.add(unwrap_optional(cls.rest.next))
                )
                continue

            if Tokenizer.equal(cls.rest, ">"):
                node = new_binary(
                    NodeKind.ND_LT, cls.add(unwrap_optional(cls.rest.next)), node
                )
                continue

            if Tokenizer.equal(cls.rest, ">="):
                node = new_binary(
                    NodeKind.ND_LE, cls.add(unwrap_optional(cls.rest.next)), node
                )
                continue

            return node

    @classmethod
    def add(cls, tok: Token) -> Node:
        """Parses addition/substraction expressions.

        add = mul ("+" mul | "-" mul)*

        Args:
            tok: Token to be parsed.

        Returns:
            A new binary node.
        """

        node = cls.mul(tok)

        while True:
            if Tokenizer.equal(cls.rest, "+"):
                node = new_binary(
                    NodeKind.ND_ADD, node, cls.mul(unwrap_optional(cls.rest.next))
                )
                continue

            if Tokenizer.equal(cls.rest, "-"):
                node = new_binary(
                    NodeKind.ND_SUB, node, cls.mul(unwrap_optional(cls.rest.next))
                )
                continue

            return node

    @classmethod
    def mul(cls, tok: Token) -> Node:
        """Parses multiplication/division expressions.

        mul = unary ("*" unary | "/" unary)*

        Args:
            tok: Token to be parsed.

        Returns:
            A new binary node.
        """
        node = cls.unary(tok)

        while True:
            if Tokenizer.equal(cls.rest, "/"):
                node = new_binary(
                    NodeKind.ND_DIV, node, cls.unary(unwrap_optional(cls.rest.next))
                )
                continue
            if Tokenizer.equal(cls.rest, "*"):
                node = new_binary(
                    NodeKind.ND_MUL, node, cls.unary(unwrap_optional(cls.rest.next))
                )
                continue

            return node

    @classmethod
    def unary(cls, tok: Token) -> Node:
        """Parses unary expressions.

        unary = ("+" | "-") unary | primary

        Args:
            tok: The token to be parsed.

        Returns:
            A new unary node.
        """

        if Tokenizer.equal(tok, "+"):
            return cls.unary(unwrap_optional(tok.next))

        if Tokenizer.equal(tok, "-"):
            return new_unary(NodeKind.ND_NEG, cls.unary(unwrap_optional(tok.next)))

        return cls.primary(tok)

    @classmethod
    def primary(cls, tok: Token) -> Node:
        """Parses primary expressions.

        primary = "(" expr ")" | num

        Args:
            tok: The token to be parsed.

        Returns:
            Node of the current token.
        """

        if Tokenizer.equal(tok, "("):
            node = cls.expr(unwrap_optional(tok.next), cls._prog)
            cls.rest = unwrap_optional(Tokenizer.skip(cls.rest, ")"))
            return node

        if tok.kind == TokenKind.TK_NUM:
            node = new_num(tok.val)
            cls.rest = unwrap_optional(tok.next)
            return node

        raise TokenError(tok, cls._prog, "expected an expression")
