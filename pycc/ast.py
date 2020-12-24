"""Abstract syntax tree"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


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
