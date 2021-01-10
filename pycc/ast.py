"""Pycc abstract syntax tree."""

from __future__ import annotations

from enum import Enum, auto
from typing import Optional


class NodeKind(Enum):
    """Represents a node kind.

    Attributes:
        ND_ADD:       +
        ND_SUB:       -
        ND_MUL:       *
        ND_DIV:       /
        ND_NEG:       Unary -
        ND_EQ:        ==
        ND_NE:        !=
        ND_LT:        <
        ND_LE:        <=
        ND_ASSIGN:    =
        ND_EXPR_STMT: Expression statement
        ND_VAR:       Variable
        ND_NUM:       Integer
    """

    ND_ADD = auto()
    ND_SUB = auto()
    ND_MUL = auto()
    ND_DIV = auto()
    ND_NEG = auto()
    ND_EQ = auto()
    ND_NE = auto()
    ND_LT = auto()
    ND_LE = auto()
    ND_ASSIGN = auto()
    ND_EXPR_STMT = auto()
    ND_VAR = auto()
    ND_NUM = auto()


class Node:
    """Represents a node.

    Attributes:
        kind: The node kind.
        lhs: The left hand side of the node.
        rhs: The right hand side of the node.
        name: The identifier of the node.
        val: The value of the node.
    """

    # kind: NodeKind
    # next: Optional[Node]
    # lhs: Optional[Node]
    # rhs: Optional[Node]
    # name: str
    # val: int

    def __init__(
        self,
        kind: NodeKind,
        next_: Optional[Node] = None,
        lhs: Optional[Node] = None,
        rhs: Optional[Node] = None,
        name: str = "",
        val: int = 0,
    ):
        self.kind = kind
        self.next = next_
        self.lhs = lhs
        self.rhs = rhs
        self.name = name
        self.val = val
