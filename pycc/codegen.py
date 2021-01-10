"""Pycc code generator."""

from typing import Optional

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
    def codegen(cls, node: Optional[Node]):
        """Generates assembly code for a given AST.

        Args:
            node: The root node of the AST.
        """

        print("  .globl main")
        print("main:")

        # Prologue
        print("  push %rbp")
        print("  mov %rsp, %rbp")
        print("  sub $208, %rsp")

        while node:
            cls._gen_stmt(node)
            assert cls._depth == 0
            node = node.next

        print("  mov %rbp, %rsp")
        print("  pop %rbp")
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
        elif node.kind == NodeKind.ND_VAR:
            cls._gen_addr(unwrap_optional(node))
            print("  mov (%rax), %rax")
            return
        elif node.kind == NodeKind.ND_ASSIGN:
            cls._gen_addr(unwrap_optional(node.lhs))
            cls._push()
            cls._gen_expr(unwrap_optional(node.rhs))
            cls._pop("%rdi")
            print("  mov %rax, (%rdi)")
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

    @classmethod
    def _align_to(cls, n: int, align: int) -> int:
        # Round up n to the nearest multiple of align. For instance, _align_to(5, 8)
        # returns 8 and align_to(11, 8) returns 16.
        return (n + align - 1) // align * align

    @classmethod
    def _gen_addr(cls, node: Node):
        if node.kind == NodeKind.ND_VAR:
            offset = (ord(node.name) - ord("a") + 1) * 8
            print(f"  lea {-offset}(%rbp), %rax")
        else:
            raise PyccError("Not an lvalue")
