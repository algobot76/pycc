"""Pycc code generator"""
from pycc.ast import Node, NodeKind
from pycc.error import PyccError
from pycc.utils import unwrap_optional


class CodeGen:
    """Pycc code generator.

    The code generator is a singleton for generating code expressions.
    """

    depth: int = 0

    def __init__(self):
        raise Exception("You cannot create an instance of CodeGen")

    @classmethod
    def gen_expr(cls, node: Node):
        if node.kind == NodeKind.ND_NUM:
            print(f"  mov ${node.val}, %rax")
            return
        elif node.kind == NodeKind.ND_NEG:
            cls.gen_expr(unwrap_optional(node.lhs))
            print("  neg %rax")
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
        elif (
            node.kind == NodeKind.ND_EQ
            or node.kind == NodeKind.ND_NE
            or node.kind == NodeKind.ND_LT
            or node.kind == NodeKind.ND_LE
        ):
            print("  cmp %rdi, %rax")
            if node.kind == NodeKind.ND_EQ:
                print("  sete %al")
            elif node.kind == NodeKind.ND_NE:
                print("  setne %al")
            elif node.kind == NodeKind.ND_LT:
                print("  setl %al")
            elif node.kind == NodeKind.ND_LE:
                print("  setle %al")
            print("  movzb %al, %rax")
        else:
            raise PyccError("invalid expression")

    @classmethod
    def push(cls):
        print("  push %rax")
        cls.depth += 1

    @classmethod
    def pop(cls, arg: str):
        print(f"  pop {arg}")
        cls.depth -= 1
