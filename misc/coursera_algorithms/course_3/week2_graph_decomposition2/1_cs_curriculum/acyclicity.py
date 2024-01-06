#Uses python3

import sys

def explore(adj, visited, verified_not_cycle, v):
    visited[v] = True

    for w in adj[v]:
        if not visited[w]:
            if explore(adj, visited, verified_not_cycle, w) == 1:
                return 1
        elif visited[w] and not verified_not_cycle[w]:
            return 1
        
    verified_not_cycle[v] = True


def acyclic(adj):
    for v in range(n):
        visited = [False for _ in range(n)] 
        verified_not_cycle = [False for _ in range(n)] 
        ans = explore(adj, visited, verified_not_cycle, v)
        if ans == 1:
            return 1

    return 0

if __name__ == '__main__':
    
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]

    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)

    print(acyclic(adj))
