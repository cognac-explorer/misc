import math


def binary_search(keys, query, r):
    l = 0
    while l <= r:
        m = l + math.floor((r - l)/ 2)
        if keys[m] == query:
            return m
        if keys[m] < query:
            l = m + 1
        else:
            r = m - 1
    return -1


def solution(keys, query):
    r = len(keys) -1
    while True:
        indx = binary_search(keys, query, r)
        if indx <= 0 or keys[indx-1] != keys[indx]:
            return indx
        r = indx-1


if __name__ == '__main__':
    num_keys = int(input())
    input_keys = list(map(int, input().split()))
    assert len(input_keys) == num_keys

    num_queries = int(input())
    input_queries = list(map(int, input().split()))
    assert len(input_queries) == num_queries

    for q in input_queries:
        print(solution(input_keys, q), end=' ')
