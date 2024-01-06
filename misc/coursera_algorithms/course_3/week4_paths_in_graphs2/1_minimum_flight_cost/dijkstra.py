#Uses python3

from math import inf
import sys
from heapq import heappush, heappop


def distance(adj, cost, s, t):

    dist = [inf for _ in range(len(adj))]
    dist[s] = 0
    # prev = [None for _ in range(len(adj))]
    q = []
    heappush(q, (0, s))
    
    while q:
        dist_u, u = heappop(q)
        for i, v in enumerate(adj[u]):
            if dist[v] > dist_u + cost[u][i]:
                dist[v] = dist_u + cost[u][i]
                # prev[v] = u
                heappush(q, (dist[v], v))
    
    if dist[t] == inf:
        return -1
    
    # print(prev)
    return dist[t]


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
