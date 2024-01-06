import math


def binary_search(keys, query):
    l = 0
    r = len(keys) -1
    while l <= r:
        m = l + math.floor((r - l)/ 2)
        if keys[m] == query:
            return m
        if keys[m] < query:
            l = m + 1
        else:
            r = m - 1
    return -1


if __name__ == '__main__':
    num_keys = int(input())
    input_keys = list(map(int, input().split()))
    assert len(input_keys) == num_keys

    num_queries = int(input())
    input_queries = list(map(int, input().split()))
    assert len(input_queries) == num_queries

    for q in input_queries:
        print(binary_search(input_keys, q), end=' ')
