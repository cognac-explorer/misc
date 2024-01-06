# Uses python3
import sys

def lcm_naive(a, b):
    min_c = min(a, b)
    for l in range(min_c, a*b + 1, min_c):
        if l % a == 0 and l % b == 0:
            return l

    return a*b

if __name__ == '__main__':
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(lcm_naive(a, b))

