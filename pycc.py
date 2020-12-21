import sys


def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"{sys.argv[0]} invalid number of arguments\n")
        exit(1)

    print("  .globl main")
    print("main:")
    print(f"  mov ${sys.argv[1]}, %rax")
    print("  ret")
