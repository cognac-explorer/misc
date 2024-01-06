# python3

import sys, threading
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class TreeOrders:
  def read(self):
    self.n = int(sys.stdin.readline())
    self.key = [0 for i in range(self.n)]
    self.left = [0 for i in range(self.n)]
    self.right = [0 for i in range(self.n)]
    self.result = []
    for i in range(self.n):
      [a, b, c] = map(int, sys.stdin.readline().split())
      self.key[i] = a
      self.left[i] = b
      self.right[i] = c

  def inOrder(self, i=0):
    if i == -1:
      return
    self.inOrder(self.left[i])
    self.result.append(self.key[i])
    self.inOrder(self.right[i])
    return self.result

  def preOrder(self, i=0):
    if i == -1:
      return
    self.result.append(self.key[i])
    self.preOrder(self.left[i])
    self.preOrder(self.right[i])
    return self.result

  def postOrder(self, i=0):
    if i == -1:
      return
    self.postOrder(self.left[i])
    self.postOrder(self.right[i])
    self.result.append(self.key[i])
    return self.result
        

def main():
  tree = TreeOrders()
  tree.read()
  print(" ".join(str(x) for x in tree.inOrder()))
  tree.result = []
  print(" ".join(str(x) for x in tree.preOrder()))
  tree.result = []
  print(" ".join(str(x) for x in tree.postOrder()))

threading.Thread(target=main).start()
