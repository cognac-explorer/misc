#python3
import sys
from collections import deque

class StackWithMax():
    def __init__(self):
        self.maxvs = deque()
        self.max_v = 0
        self.__stack = []

    def Push(self, a):
        self.__stack.append(a)
        if self.max_v < a:
            self.max_v = a
            self.maxvs.append(a)
        else:
            self.maxvs.append(self.max_v)

    def Pop(self):
        assert(len(self.__stack))
        self.__stack.pop()
        self.maxvs.pop()

    def Max(self):
        assert(len(self.__stack))
        return self.maxvs[-1]


if __name__ == '__main__':
    stack = StackWithMax()

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        query = sys.stdin.readline().split()

        if query[0] == "push":
            stack.Push(int(query[1]))
        elif query[0] == "pop":
            stack.Pop()
        elif query[0] == "max":
            print(stack.Max())
        else:
            assert(0)
