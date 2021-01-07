"""Pycc parser."""

from pycc.ast import Node, NodeKind, new_binary, new_num, new_unary
from pycc.exception import TokenError
from pycc.token import Token, TokenKind
from pycc.tokenizer import Tokenizer
from pycc.utils import unwrap_optional


class Parser:
    """Pycc parser.

    The parser is a singleton and any call to its __init__ method will raise
    an exception. Call its parse method to turn tokens into an AST.
    """

    _prog: str = ""
    _rest: Token

    def __init__(self):
        raise Exception("You cannot create an instance of Parser")

    @classmethod
    def parse(cls, tok: Token, prog: str) -> Node:
        """Parses the tokens into an AST.

        Arg:
            tok: The head of the token list.
            prog: The program to be parsed.

        Returns:
            The root node of the AST.
        """

        cls._prog = prog
        cls._rest = tok

        head = Node(NodeKind.ND_EXPR_STMT, None, None, None, 0)  # dummy node
        cur = head

        while cls._rest.kind != TokenKind.TK_EOF:
            cur.next = cls._stmt(cls._rest)
            cur = cur.next

        return unwrap_optional(head.next)

    @classmethod
    def _expr(cls, tok: Token) -> Node:
        # expr = equality
        return cls._equality(tok)

    @classmethod
    def _equality(cls, tok: Token) -> Node:
        # equality = relational ("==" relational | "!=" relational)*
        node = cls._relational(tok)

        while True:
            if Tokenizer.equal(cls._rest, "=="):
                node = new_binary(
                    NodeKind.ND_EQ,
                    node,
                    cls._relational(unwrap_optional(cls._rest.next)),
                )
                continue

            if Tokenizer.equal(cls._rest, "!="):
                node = new_binary(
                    NodeKind.ND_NE,
                    node,
                    cls._relational(unwrap_optional(cls._rest.next)),
                )
                continue

            return node

    @classmethod
    def _relational(cls, tok: Token) -> Node:
        # relational = add ("<" add | "<=" add | ">" add | ">=" add)*
        node = cls._add(tok)

        while True:
            if Tokenizer.equal(cls._rest, "<"):
                node = new_binary(
                    NodeKind.ND_LT, node, cls._add(unwrap_optional(cls._rest.next))
                )
                continue

            if Tokenizer.equal(cls._rest, "<="):
                node = new_binary(
                    NodeKind.ND_LE, node, cls._add(unwrap_optional(cls._rest.next))
                )
                continue

            if Tokenizer.equal(cls._rest, ">"):
                node = new_binary(
                    NodeKind.ND_LT, cls._add(unwrap_optional(cls._rest.next)), node
                )
                continue

            if Tokenizer.equal(cls._rest, ">="):
                node = new_binary(
                    NodeKind.ND_LE, cls._add(unwrap_optional(cls._rest.next)), node
                )
                continue

            return node

    @classmethod
    def _add(cls, tok: Token) -> Node:
        # add = mul ("+" mul | "-" mul)*``
        node = cls._mul(tok)

        while True:
            if Tokenizer.equal(cls._rest, "+"):
                node = new_binary(
                    NodeKind.ND_ADD, node, cls._mul(unwrap_optional(cls._rest.next))
                )
                continue

            if Tokenizer.equal(cls._rest, "-"):
                node = new_binary(
                    NodeKind.ND_SUB, node, cls._mul(unwrap_optional(cls._rest.next))
                )
                continue

            return node

    @classmethod
    def _mul(cls, tok: Token) -> Node:
        # mul = unary ("*" unary | "/" unary)*
        node = cls._unary(tok)

        while True:
            if Tokenizer.equal(cls._rest, "/"):
                node = new_binary(
                    NodeKind.ND_DIV, node, cls._unary(unwrap_optional(cls._rest.next))
                )
                continue
            if Tokenizer.equal(cls._rest, "*"):
                node = new_binary(
                    NodeKind.ND_MUL, node, cls._unary(unwrap_optional(cls._rest.next))
                )
                continue

            return node

    @classmethod
    def _unary(cls, tok: Token) -> Node:
        # unary = ("+" | "-") unary | primary
        if Tokenizer.equal(tok, "+"):
            return cls._unary(unwrap_optional(tok.next))

        if Tokenizer.equal(tok, "-"):
            return new_unary(NodeKind.ND_NEG, cls._unary(unwrap_optional(tok.next)))

        return cls._primary(tok)

    @classmethod
    def _primary(cls, tok: Token) -> Node:
        # primary = "(" expr ")" | num
        if Tokenizer.equal(tok, "("):
            node = cls._expr(unwrap_optional(tok.next))
            cls._rest = unwrap_optional(Tokenizer.skip(cls._rest, ")"))
            return node

        if tok.kind == TokenKind.TK_NUM:
            node = new_num(tok.val)
            cls._rest = unwrap_optional(tok.next)
            return node

        raise TokenError(tok, cls._prog, "expected an expression")

    @classmethod
    def _stmt(cls, tok: Token) -> Node:
        # stmt = expr-stmt
        return cls._expr_stmt(tok)

    @classmethod
    def _expr_stmt(cls, tok: Token) -> Node:
        # expr-stmt = expr ";"
        node = new_unary(NodeKind.ND_EXPR_STMT, cls._expr(tok))
        cls._rest = unwrap_optional(Tokenizer.skip(cls._rest, ";"))
        return node
