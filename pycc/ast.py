"""Abstract syntax tree"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from pycc.error import error_tok
from pycc.tokenizer import Tokenizer
from pycc.utils import unwrap_optional

from .token import Token, TokenKind


class NodeKind(Enum):
    """Represents a node kind

    Attributes:
        ND_ADD: +
        ND_SUB: -
        ND_MUL: *
        ND_DIV: /
        ND_NUM: Integer
    """

    ND_ADD = auto()
    ND_SUB = auto()
    ND_MUL = auto()
    ND_DIV = auto()
    ND_NUM = auto()


@dataclass
class Node:
    """Represents a node

    Attributes:
        kind: Node kind
        lhs: Left hand side of the node
        rhs: Right hand side of the node
        val: Int value of the node
    """

    kind: NodeKind
    lhs: Optional[Node]
    rhs: Optional[Node]
    val: Optional[int]


def new_binary(kind: NodeKind, lhs: Node, rhs: Node) -> Node:
    """Creates a new node without a value.

    Args:
        kind: NodeKind
        lhs: Left hand side Node
        rhs: Right hand side Node
        val: Value of node

    Returns:
        A new node with the given parameters
    """

    return Node(kind, lhs, rhs, None)


def new_num(val: int) -> Node:
    """Creates a new node with a value.

    Args:
        val: Node value

    Returns:
        A new node with the value
    """

    return Node(NodeKind.ND_NUM, None, None, val)


def primary(tok: Token, prog: str) -> Tuple[Node, Token]:
    """Primary expression in parentheses

    Args:
        tok: Token to analyze
        prog: Program

    Returns:
        A tuple
            Node: Node of the current token
            Token: Token for the next token
    """

    if Tokenizer.equal(tok, "("):
        next_token = unwrap_optional(tok.next)
        node, tok = expr(next_token, prog)
        rest = unwrap_optional(Tokenizer.skip(tok, ")"))
        return node, rest

    if tok.kind == TokenKind.TK_NUM:
        node = new_num(tok.val)
        rest = unwrap_optional(tok.next)
        return node, rest

    error_tok(tok, prog, "expected an expression")
    return Node(NodeKind.ND_ADD, None, None, None), tok  # dummy return for mypy


def mul(tok: Token, prog: str) -> Tuple[Node, Token]:
    """Multiplication expression node constructor

    Args:
        tok: Token to analyze
        prog: Program to analyze

    Returns:
        A tuple
            Node: Node of the current token
            Token: Token for the next token
    """
    node, tok = primary(tok, prog)

    while True:
        if Tokenizer.equal(tok, "/"):
            pri_node, tok = primary(unwrap_optional(tok.next), prog)
            node = new_binary(NodeKind.ND_DIV, node, pri_node)
            continue
        if Tokenizer.equal(tok, "*"):
            pri_node, tok = primary(unwrap_optional(tok.next), prog)
            node = new_binary(NodeKind.ND_MUL, node, pri_node)
            continue

        rest = tok
        return node, rest


def expr(tok: Token, prog: str) -> Tuple[Node, Token]:
    """Expression node constructor

    Args:
        tok: Token to analyze
        prog: Program to analyze

    Returns:
        A tuple
            Node: Node of the current token
            Token: Token for the next token
    """
    node, tok = mul(tok, prog)
    while True:
        if Tokenizer.equal(tok, "+"):
            mul_node, tok = mul(unwrap_optional(tok.next), prog)
            node = new_binary(NodeKind.ND_ADD, node, mul_node)
            continue
        if Tokenizer.equal(tok, "-"):
            mul_node, tok = mul(unwrap_optional(tok.next), prog)
            node = new_binary(NodeKind.ND_SUB, node, mul_node)
            continue
        rest = tok
        return node, rest
