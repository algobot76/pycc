"""Pycc code generator."""

from pycc.ast import Node, NodeKind
from pycc.exception import PyccError
from pycc.utils import unwrap_optional


class Codegen:
    """Pycc code generator.

    The code generator is a singleton for generating code expressions. Any call to its
    __init__ method will raise an exception. Call its codegen method on an AST to
    generate the corresponding assembly code.
    """

    _depth: int = 0

    def __init__(self):
        raise Exception("You cannot create an instance of Codegen")

    @classmethod
    def codegen(cls, node: Node):
        """Generates assembly code for a given AST.

        Args:
            node: The root node of the AST.
        """

        print("  .globl main")
        print("main:")

        while node:
            cls._gen_stmt(node)
            assert cls._depth == 0
            if node.next is None:
                break
            node = unwrap_optional(node.next)

        print("  ret")

    @classmethod
    def _gen_stmt(cls, node: Node):
        if node.kind == NodeKind.ND_EXPR_STMT:
            cls._gen_expr(unwrap_optional(node.lhs))
        else:
            raise PyccError("invalid statement")

    @classmethod
    def _gen_expr(cls, node: Node):
        if node.kind == NodeKind.ND_NUM:
            print(f"  mov ${node.val}, %rax")
            return
        elif node.kind == NodeKind.ND_NEG:
            cls._gen_expr(unwrap_optional(node.lhs))
            print("  neg %rax")
            return

        cls._gen_expr(unwrap_optional(node.rhs))
        cls._push()
        cls._gen_expr(unwrap_optional(node.lhs))
        cls._pop("%rdi")

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
    def _push(cls):
        print("  push %rax")
        cls._depth += 1

    @classmethod
    def _pop(cls, arg: str):
        print(f"  pop {arg}")
        cls._depth -= 1
