# python3
import math


def sift_down(data, size, i, swaps):
    max_indx = i 

    l = left_child(i)
    if l < size and data[l] < data[max_indx]:
        max_indx = l

    r = right_child(i)
    if r < size and data[r] < data[max_indx]:
        max_indx = r
    
    if i != max_indx:
        swaps.append((i, max_indx))
        data[i], data[max_indx] = data[max_indx], data[i]
        sift_down(data, size, max_indx, swaps)


def left_child(i):
    return 2 * i + 1


def right_child(i):
    return 2 * i + 2


def build_heap(data):
    n = len(data)
    swaps = []
    for i in range(math.floor(n/2) - 1, -1, -1):
        sift_down(data, n, i, swaps)

    return swaps


def main():
    
    n = int(input())
    data = list(map(int, input().split()))
    swaps = build_heap(data)
   
    print(len(swaps))
    for i, j in swaps:
        print(i, j)


if __name__ == "__main__":
    main()
