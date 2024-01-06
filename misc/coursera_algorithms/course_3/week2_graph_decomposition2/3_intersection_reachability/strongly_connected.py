#Uses python3

import sys

sys.setrecursionlimit(200000)


def explore_dfs(adj, v, visited, order):
    visited[v] = True
    for w in adj[v]:
        if not visited[w]:
            explore_dfs(adj, w, visited, order)
    order.append(v)


def explore(adj, v, visited):
    visited[v] = True
    for w in adj[v]:
        if not visited[w]:
            explore(adj, w, visited)
    

def dfs(adj, visited):
    order = []
    for v in range(n):
        if not visited[v]:
            explore_dfs(adj, v, visited, order)

    return order

def number_of_strongly_connected_components(adj, adj_r):
    visited = [False] * len(adj)
    r_post_order = dfs(adj_r, visited)
    # print(r_post_order)
    result = 0
    visited = [False] * len(adj)
    for v in r_post_order:
        if not visited[v]:
            explore(adj_r, v, visited)
            result += 1

    return result

if __name__ == '__main__':
        
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    # print(data)
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    edges_r = []

    for edge in edges:
        a, b = edge
        edges_r.append((b, a))  

    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)

    adj_r = [[] for _ in range(n)]
    for (a, b) in edges_r:
        adj_r[a - 1].append(b - 1)

    print(number_of_strongly_connected_components(adj, adj_r))
