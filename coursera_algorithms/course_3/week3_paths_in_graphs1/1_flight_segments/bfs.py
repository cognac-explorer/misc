#Uses python3

import sys
import queue

def bfs(adj, s):

    dist = [-1 for v in range(len(adj))]
    tree = [-1 for v in range(len(adj))]
    q = queue.Queue()

    dist[s] = 0
    q.put(s)

    while not q.empty():
        u = q.get()
        for w in adj[u]:
            if dist[w] == -1:
                q.put(w)
                dist[w] = dist[u] + 1
                tree[w] = u
    return tree


def distance(tree, s, t):
    result = 0
    while t != s:
        result += 1
        t = tree[t]
        if t == -1:
            return -1
        
    return result


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
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1

    tree = bfs(adj, s)
    print(distance(tree, s, t))
