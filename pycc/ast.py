"""Pycc abstract syntax tree."""

from __future__ import annotations

from dataclasses import dataclass
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


@dataclass
class Node:
    """Represents a node.

    Attributes:
        kind: The node kind.
        lhs: The left hand side of the node.
        rhs: The right hand side of the node.
        name: The identifier of the node.
        val: The value of the node.
    """

    kind: NodeKind
    next: Optional[Node]
    lhs: Optional[Node]
    rhs: Optional[Node]
    name: str
    val: int


def new_binary(kind: NodeKind, lhs: Node, rhs: Node) -> Node:
    """Creates a new node with the given LHS and RHS nodes.

    Args:
        kind: The kind of the node.
        lhs: The left hand side of the node.
        rhs: The right hand side of the node.

    Returns:
        A new node with the specified LHS and RHS.
    """

    return Node(kind, None, lhs, rhs, "", 0)


def new_num(val: int) -> Node:
    """Creates a new node with the given value.

    Args:
        val: The value of the node.

    Returns:
        A new node with the value.
    """

    return Node(NodeKind.ND_NUM, None, None, None, "", val)


def new_unary(kind: NodeKind, lhs: Node) -> Node:
    """Creates a new node with the given LHS node.

    Args:
        kind: The kind of the node.
        lhs: The left hand side of the node.

    Returns:
        A new node with the LHS node.
    """

    return Node(kind, None, lhs, None, "", 0)


def new_var_node(name: str) -> Node:
    """Creates a new node with the given identifier.

    Args:
        name: The identifier of the node.

    Returns:
        A new node with the identifier.
    """

    return Node(NodeKind.ND_VAR, None, None, None, name, 0)
