# Uses python3
import sys

def optimal_weight(W, n, w):
    vals = [[0 for _ in range(n+1)] for _ in range(W+1)]

    for i in range(1, n+1):
        for currw in range(1, W+1):
            vals[currw][i] = vals[currw][i-1]
            if w[i-1] <= currw:
                val = vals[currw-w[i-1]][i-1] + w[i-1]
                if val > vals[currw][i]:
                    vals[currw][i] = val           
          
    return vals[W][n]

if __name__ == '__main__':
    input = sys.stdin.read()
    W, n, *w = list(map(int, input.split()))
    print(optimal_weight(W, n, w))
