# Uses python3
def calc_fib(n):
    if n < 2:
        return n
    arr = [0] * (n + 1)
    arr[0] = 0
    arr[1] = 1
    for i in range(2, n + 1):
        arr[i] = arr[i-1] + arr[i-2]

    return arr[-1]

n = int(input())
print(calc_fib(n))
