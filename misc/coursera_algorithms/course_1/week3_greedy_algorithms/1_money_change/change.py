# Uses python3
import sys

def get_change(m):
    ans = 0
    for coin in [10, 5, 1]:
        n = m // coin
        if n > 0:
            ans += n
            m = m - n * coin
    return ans

if __name__ == '__main__':
    m = int(sys.stdin.read())
    print(get_change(m))
