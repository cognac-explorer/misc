# python3

from collections import namedtuple
from math import floor

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])


class MyThread:

    def __init__(self, index, finish_time):
        self.index = index
        self.finish_time = finish_time

    def __gt__(self, other):
        if self.finish_time > other.finish_time:
            return True 
        elif self.finish_time == other.finish_time and self.index > other.index:
            return True
        else:
            return False


class ThreadHeap:

    def __init__(self, thread_list):
        self.size = len(thread_list)
        self.threads = thread_list

    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2

    def parent(self, i):
        return floor((i - 1) / 2)

    def sift_up(self, i):
        while i > 0 and self.threads[i] < self.threads[self.parent(i)]:
            self.threads[i], self.threads[self.parent(i)] = self.threads[self.parent(i)], self.threads[i]
            i = self.parent(i)

    def sift_down(self, i):
        max_indx = i 
    
        l = self.left_child(i)
        if l < self.size and self.threads[l] < self.threads[max_indx]:
            max_indx = l
    
        r = self.right_child(i)
        if r < self.size and self.threads[r] < self.threads[max_indx]:
            max_indx = r
        
        if i != max_indx:
            self.threads[i], self.threads[max_indx] = self.threads[max_indx], self.threads[i]
            self.sift_down(max_indx)
    
    def insert(self, thread):
        self.size = self.size + 1
        self.threads[self.size - 1] = thread 
        self.sift_up(self.size - 1)

    def extract_min(self):
        result = self.threads[0]
        self.threads[0] = self.threads[self.size - 1]
        self.size = self.size - 1
        self.sift_down(0)
        return  result

    def build_heap(self):
        for i in range(floor(self.size / 2) - 1, -1, -1):
            self.sift_down(i)


def assign_jobs(n_workers, jobs):
    result = []
    threads_heap = ThreadHeap([MyThread(i, finish_time) for i, finish_time in enumerate([0] * n_workers)])
    
    for job in jobs:
        next_worker = threads_heap.extract_min()
        result.append(AssignedJob(next_worker.index, next_worker.finish_time))
        threads_heap.insert(MyThread(next_worker.index, next_worker.finish_time + job))

    return result


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
