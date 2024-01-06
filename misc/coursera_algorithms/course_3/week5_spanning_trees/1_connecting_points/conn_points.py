#Uses python3
from cmath import e
import sys
import math
from heapq import heappush, heappop


def distance(x, y, s, f):
    return math.sqrt((x[s] - x[f])*(x[s] - x[f]) + (y[s] - y[f])*(y[s] - y[f]))

# implement simple disjoint for kruskal alg
class DSet:
    def __init__(self, max_count):
        self.parent = [0] * max_count
        self.rank = [0] * max_count

    def make_set(self, v):
        self.parent[v] = v
        self.rank[v] = 0
    
    def find(self, v):
        while v != self.parent[v]:
            v = self.parent[v]
        return v
    
    def union(self, u, v):

        u_id = self.find(u)
        v_id = self.find(v)
        if u_id == v_id:
            return 
        
        if self.rank[u_id] > self.rank[v_id]:
            self.parent[v_id] = u_id 
        else:
            self.parent[u_id] = v_id 
            if self.rank[u_id] == self.rank[v_id]:
                self.rank[v_id] = self.rank[v_id] + 1


def minimum_distance_prim(x, y):  # Failed case #23/40: Wrong answer ?

    cost = [math.inf for _ in range(len(x))]
    cost[0] = 0

    q = []
    for i in range(len(x)):
        heappush(q, (cost[i], i))  # (dist, vertex index)

    while q:
        _, v = heappop(q)
    
        for u in range(len(x)):
            if (cost[u], u) in q and cost[u] > distance(x, y, u, v):
                q.remove((cost[u], u))
                cost[u] = distance(x, y, u, v)
                heappush(q, (cost[u], u))

    return sum(cost) 


class Edge:
    def __init__(self, x, y, u, v):
        self.u = u 
        self.v = v 
        self.distance = distance(x, y, u, v)


def minimum_distance_kruskal(x, y):

    dset = DSet(201)
    for i in range(len(x)):
        dset.make_set(i)

    edges = []
    for i in range(len(x)):
        for j in range(i):
            edges.append(Edge(x, y, i, j))

    edges.sort(key=lambda x: x.distance)
    
    result = 0
    for edge in edges:        
        if dset.find(edge.u) != dset.find(edge.v):
            dset.union(edge.u, edge.v) 
            result += edge.distance

    return result


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.7f}".format(minimum_distance_kruskal(x, y)))
