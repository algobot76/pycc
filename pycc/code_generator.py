"""Pycc code generator"""
from pycc.ast import Node, NodeKind
from pycc.error import error
from pycc.utils import unwrap_optional


class CodeGenerator:
    """Pycc code generator.

    The code generator is a singleton for generating code expressions
    """

    depth: int = 0

    def __init__(self):
        raise Exception("You cannot create an instance of CodeGenerator")

    @staticmethod
    def gen_expr(node: Node):
        if node.kind == NodeKind.ND_NUM:
            print(f"  mov ${node.val}, %rax")
            return

        CodeGenerator.gen_expr(unwrap_optional(node.rhs))
        CodeGenerator.push()
        CodeGenerator.gen_expr(unwrap_optional(node.lhs))
        CodeGenerator.pop("%rdi")

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

    @staticmethod
    def push():
        print("  push %rax")
        CodeGenerator.depth += 1

    @staticmethod
    def pop(arg: str):
        print(f"  pop {arg}")
        CodeGenerator.depth -= 1
