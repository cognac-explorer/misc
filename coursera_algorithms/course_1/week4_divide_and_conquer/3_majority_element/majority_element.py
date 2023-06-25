# Uses python3
import sys

# def get_majority_element(a, left, right):
#     if left == right:
#         return -1
#     if left + 1 == right:
#         return a[left]
#     #write your code here
#     return -1


def get_majority_element(a, l, r):
    if l == r:
        return a[l]
    m = l + (r - l) // 2
    left = get_majority_element(a, l, m)
    right = get_majority_element(a, m + 1, r)
    if left == right:
        return left
    else:
        left_count = sum([1 for ai in a[l:r] if ai == left])
        right_count = sum([1 for ai in a[l:r] if ai == right])
        return left if left_count > right_count else right
        

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    elem = get_majority_element(a, 0, n-1)
    count = 0
    ans = 0
    for i in range(n):
        if a[i] == elem:
            count += 1
            if count > n / 2:
                ans = 1
                break
    if ans:
        print(1)
    else:
        print(0)
