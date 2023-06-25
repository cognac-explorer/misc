# Uses python3
import sys

def get_pissano_period(m):

    previous = 0
    current  = 1

    if m == 2:
        return 3

    period = 0
    while True:
        previous, current = current, previous + current
        period += 1
        if previous % m == 0 and current % m == 1:
            break

    return period


def fib_mod(n, m):
    period = get_pissano_period(m)
    r = n % period 
    
    if r == 0:
        return 0
        
    prev, cur = 0, 1

    for _ in range(r-1):
        prev, cur = cur, prev + cur 
    
    return cur % m


if __name__ == '__main__':
    input = sys.stdin.read();
    n, m = map(int, input.split())
    print(fib_mod(n, m))
