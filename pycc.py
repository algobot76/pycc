import re
import sys


def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"{sys.argv[0]} invalid number of arguments\n")
        exit(1)

    params = sys.argv[1]
    numbers = re.findall(r'\d+', params)
    operators = re.findall(r'[\/\+\-\*]', params)

    print("  .globl main")
    print("main:")
    print(f"  mov rax, {numbers[0]}")

    for i in range(0, len(operators)):
        if operators[i] == "+":
            print(f"  add rax, {numbers[i+1]}")
        elif operators[i] == "-":
            print(f"  sub rax, {numbers[i+1]}")
        else:
            sys.stderr.write(f"unexpected character: {operators[i]}")

    print("  ret")
