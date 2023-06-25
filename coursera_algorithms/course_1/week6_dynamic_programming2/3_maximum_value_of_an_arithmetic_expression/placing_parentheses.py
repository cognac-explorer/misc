import sys
from cmath import inf

# Uses python3
def evalt(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        assert False

def min_and_max(digits, operators, M, m, i, j):
    min_v = inf
    max_v = -inf

    for k in range(i, j):
        a = evalt(M[i][k], M[k+1][j], operators[k])
        b = evalt(M[i][k], m[k+1][j], operators[k])
        c = evalt(m[i][k], M[k+1][j], operators[k])
        d = evalt(m[i][k], m[k+1][j], operators[k])
        min_v = min(min_v, a, b, c, d)
        max_v = max(max_v, a, b, c, d)

    return min_v, max_v


def get_maximum_value(digits, operators):
    n = len(digits)
    m = [[0 for _ in range(n)] for _ in range(n)]
    M = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        m[i][i] = digits[i]
        M[i][i] = digits[i]

    for s in range(1, n):
        for i in range(n-s):
            j = i + s
            curr_min, curr_max = min_and_max(digits, operators, M, m, i, j)
            m[i][j] = curr_min
            M[i][j] = curr_max
    
    return M[0][n-1]


if __name__ == "__main__":
    input = sys.stdin.read()
    digits = []
    operators = []
    for indx, s in enumerate(input):
        if indx % 2 == 0:
            digits.append(int(s))
        else:
            operators.append(s)

    print(get_maximum_value(digits, operators))
