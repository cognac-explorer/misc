#Uses python3

import sys
from collections import deque

def explore(adj, v, visited, order):
    visited[v] = True
    for w in adj[v]:
        if not visited[w]:
            explore(adj, w, visited, order)
    order.appendleft(v)


def dfs(adj):
    order = deque()
    visited = [False] * len(adj)

    for v in range(n):
        if not visited[v]:
            explore(adj, v, visited, order)
    return order


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = dfs(adj)
    for x in order:
        print(x + 1, end=' ')

