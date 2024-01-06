# Uses python3
import sys

def get_optimal_value(capacity, n, weights, values):
    value = 0.
    fractions = [values[i] / weights[i] for i in range(n)]
 
    for _ in range(n):
        if capacity == 0:
            return value
        cur_max = max(fractions)
        cur_max_indx = fractions.index(cur_max)
        item_weight = min(capacity, weights[cur_max_indx])
        value += values[cur_max_indx] * (item_weight / weights[cur_max_indx])
        capacity -= item_weight
        fractions.remove(cur_max)
        values.pop(cur_max_indx)
        weights.pop(cur_max_indx)
    return value


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = get_optimal_value(capacity, n, weights, values)
    print("{:.10f}".format(opt_value))
