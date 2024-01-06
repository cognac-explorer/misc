#Uses python3

import sys
import queue


def bfs(adj, s, color):
    q = queue.Queue()
    color[s] = 0  # no matter from whet color to start
    q.put(s)

    while not q.empty():
        u = q.get()
        ancestor_color = color[u]

        for w in adj[u]:
            if color[w] == -1:
                q.put(w)
                color[w] = 0 if ancestor_color == 1 else 1
            else:
                if color[w] == ancestor_color:
                    return 0
    
    return 1


def bipartite(adj):
     # -1 no color yet, 0, 1 - colors
    color = [-1 for v in range(len(adj))]

    for v in range(len(adj)):
        if color[v] == -1:
            ans = bfs(adj, v, color)
            if ans == 0:
                return 0

    return 1


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(bipartite(adj))
