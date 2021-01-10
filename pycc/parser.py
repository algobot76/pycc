"""Pycc parser."""

from pycc.ast import Node, NodeKind, new_unary, new_var_node
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

        head = Node(NodeKind.ND_EXPR_STMT)  # dummy node
        cur = head

        while cls._rest.kind != TokenKind.TK_EOF:
            cur.next = cls._stmt(cls._rest)
            cur = cur.next

        return unwrap_optional(head.next)

    @classmethod
    def _expr(cls, tok: Token) -> Node:
        # expr = assign
        return cls._assign(tok)

    @classmethod
    def _assign(cls, tok: Token) -> Node:
        # assign = equality ("=" assign)?
        node = cls._equality(tok)
        if Tokenizer.equal(cls._rest, "="):
            node = Node(
                NodeKind.ND_ASSIGN,
                lhs=node,
                rhs=cls._assign(unwrap_optional(cls._rest.next)),
            )
        return node

    @classmethod
    def _equality(cls, tok: Token) -> Node:
        # equality = relational ("==" relational | "!=" relational)*
        node = cls._relational(tok)

        while True:
            if Tokenizer.equal(cls._rest, "=="):
                node = Node(
                    NodeKind.ND_EQ,
                    lhs=node,
                    rhs=cls._relational(unwrap_optional(cls._rest.next)),
                )
                continue

            if Tokenizer.equal(cls._rest, "!="):
                node = Node(
                    NodeKind.ND_NE,
                    lhs=node,
                    rhs=cls._relational(unwrap_optional(cls._rest.next)),
                )
                continue

            return node

    @classmethod
    def _relational(cls, tok: Token) -> Node:
        # relational = add ("<" add | "<=" add | ">" add | ">=" add)*
        node = cls._add(tok)

        while True:
            if Tokenizer.equal(cls._rest, "<"):
                node = Node(
                    NodeKind.ND_LT,
                    lhs=node,
                    rhs=cls._add(unwrap_optional(cls._rest.next)),
                )
                continue

            if Tokenizer.equal(cls._rest, "<="):
                node = Node(
                    NodeKind.ND_LE,
                    lhs=node,
                    rhs=cls._add(unwrap_optional(cls._rest.next)),
                )
                continue

            if Tokenizer.equal(cls._rest, ">"):
                node = Node(
                    NodeKind.ND_LT,
                    lhs=cls._add(unwrap_optional(cls._rest.next)),
                    rhs=node,
                )
                continue

            if Tokenizer.equal(cls._rest, ">="):
                node = Node(
                    NodeKind.ND_LE,
                    lhs=cls._add(unwrap_optional(cls._rest.next)),
                    rhs=node,
                )
                continue

            return node

    @classmethod
    def _add(cls, tok: Token) -> Node:
        # add = mul ("+" mul | "-" mul)*``
        node = cls._mul(tok)

        while True:
            if Tokenizer.equal(cls._rest, "+"):
                node = Node(
                    NodeKind.ND_ADD,
                    lhs=node,
                    rhs=cls._mul(unwrap_optional(cls._rest.next)),
                )
                continue

            if Tokenizer.equal(cls._rest, "-"):
                node = Node(
                    NodeKind.ND_SUB,
                    lhs=node,
                    rhs=cls._mul(unwrap_optional(cls._rest.next)),
                )
                continue

            return node

    @classmethod
    def _mul(cls, tok: Token) -> Node:
        # mul = unary ("*" unary | "/" unary)*
        node = cls._unary(tok)

        while True:
            if Tokenizer.equal(cls._rest, "/"):
                node = Node(
                    NodeKind.ND_DIV,
                    lhs=node,
                    rhs=cls._unary(unwrap_optional(cls._rest.next)),
                )
                continue
            if Tokenizer.equal(cls._rest, "*"):
                node = Node(
                    NodeKind.ND_MUL,
                    lhs=node,
                    rhs=cls._unary(unwrap_optional(cls._rest.next)),
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
        # primary = "(" expr ")" | ident | num
        if Tokenizer.equal(tok, "("):
            node = cls._expr(unwrap_optional(tok.next))
            cls._rest = unwrap_optional(Tokenizer.skip(cls._rest, ")"))
            return node

        if tok.kind == TokenKind.TK_IDENT:
            node = new_var_node(cls._prog[tok.loc])
            cls._rest = unwrap_optional(tok.next)
            return node
        if tok.kind == TokenKind.TK_NUM:
            node = Node(NodeKind.ND_NUM, val=tok.val)
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
