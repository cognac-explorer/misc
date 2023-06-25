# python3
import sys


def compute_min_refills(distance, tank, stops):

    current_dist = 0
    ans = 0
    stops.sort()
    
    while current_dist + tank < distance:
        
        
        while len(stops) != 0 and stops[0] <= current_dist + tank:
            prev_point = stops[0]
            stops.pop(0)
        
        current_dist = prev_point

        if len(stops) == 0 and current_dist + tank < distance:
            return -1

        if len(stops) != 0 and stops[0] - current_dist > tank:
            return -1
        
        ans += 1

    return ans

if __name__ == '__main__':
    d, m, _, *stops = map(int, sys.stdin.read().split())
    print(compute_min_refills(d, m, stops))
