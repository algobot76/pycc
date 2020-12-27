"""Pycc code generator"""
from pycc.ast import Node, NodeKind
from pycc.error import error
from pycc.utils import unwrap_optional


class CodeGen:
    """Pycc code generator.

    The code generator is a singleton for generating code expressions
    """

    depth: int = 0

    def __init__(self):
        raise Exception("You cannot create an instance of CodeGen")

    @classmethod
    def gen_expr(cls, node: Node):
        if node.kind == NodeKind.ND_NUM:
            print(f"  mov ${node.val}, %rax")
            return

        cls.gen_expr(unwrap_optional(node.rhs))
        cls.push()
        cls.gen_expr(unwrap_optional(node.lhs))
        cls.pop("%rdi")

        if node.kind == NodeKind.ND_ADD:
            print("  add %rdi, %rax")
        elif node.kind == NodeKind.ND_SUB:
            print("  sub %rdi, %rax")
        elif node.kind == NodeKind.ND_MUL:
            print("  imul %rdi, %rax")
        elif node.kind == NodeKind.ND_DIV:
            print("  cqo")
            print("  idiv %rdi")
        else:
            error("invalid expression")

    @classmethod
    def push(cls):
        print("  push %rax")
        cls.depth += 1

    @classmethod
    def pop(cls, arg: str):
        print(f"  pop {arg}")
        cls.depth -= 1
