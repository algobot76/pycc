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
    print(f"  mov ${numbers[0]}, %rax")

    for i in range(len(operators)):
        if operators[i] == "+":
            print(f"  add ${numbers[i+1]}, %rax")
        elif operators[i] == "-":
            print(f"  sub ${numbers[i+1]}, %rax")
        else:
            sys.stderr.write(f"unexpected character: {operators[i]}")

    print("  ret")
