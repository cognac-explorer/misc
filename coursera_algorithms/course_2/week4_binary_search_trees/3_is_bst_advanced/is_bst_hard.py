#!/usr/bin/python3

import sys, threading

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size


def IsBinarySearchTree(tree, i, min_val, max_val):

  if i == -1 or not tree:
    return True
  
  if tree[i][0] < min_val or tree[i][0] >= max_val:
    return False

  return IsBinarySearchTree(tree, tree[i][1], min_val, tree[i][0]) and IsBinarySearchTree(tree, tree[i][2], tree[i][0], max_val)


def main():
  nodes = int(sys.stdin.readline().strip())
  tree = []
  for i in range(nodes):
    tree.append(list(map(int, sys.stdin.readline().strip().split())))
  if IsBinarySearchTree(tree, 0, -2**31, 2**31):
    print("CORRECT")
  else:
    print("INCORRECT")

threading.Thread(target=main).start()
