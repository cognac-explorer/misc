# Uses python3
from math import inf
import sys


def optimal_seq_dp(n):

    if n == 1:
        return [1]

    sequence = [0] * (n+1)
    prev_elems = [0]
    ans = []

    for i in range(2, n+1):
        num_operations = inf
        
        if i % 3 == 0:
            if sequence[i//3] < num_operations:
                num_operations = sequence[i//3] + 1
                prev_number = i // 3
        
        if i % 2 == 0:
            if sequence[i//2] < num_operations:
                num_operations = sequence[i//2] + 1
                prev_number = i // 2

        if sequence[i-1] < num_operations:
            num_operations = sequence[i-1] + 1
            prev_number = i - 1
        
        sequence[i] = num_operations
        prev_elems.append(prev_number)
    
    ans.append(n)
    while prev_number != 1:
        ans.append(prev_number)
        prev_number = prev_elems[prev_number-1]
    ans.append(1)
    
    return ans[::-1]


if __name__ == '__main__':
    n = int(sys.stdin.read())
    sequence = list(optimal_seq_dp(n))
    print(len(sequence) - 1)
    for x in sequence:
        print(x, end=' ')
