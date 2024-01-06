# python3

class Query:

    def __init__(self, query):
        self.type = query[0]
        if self.type == 'check':
            self.ind = int(query[1])
        else:
            self.s = query[1]


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        # store all strings in one list
        self.chain_list = [[] for _ in range (self.bucket_count)]

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self._multiplier + ord(c)) % self._prime
        return ans % self.bucket_count

    def write_chain(self, chain):
        print(' '.join(chain))

    def read_query(self):
        return Query(input().split())

    def process_query(self, query):
        if query.type == "check":
            # use reverse order, because we append strings to the end
            self.write_chain(cur for cur in reversed(self.chain_list[query.ind]))
                        
        else:
            hash_val = self._hash_func(query.s)
            ind = -1
            for i, s in enumerate(self.chain_list[hash_val]):
                if s == query.s:
                    ind = i

            if query.type == 'find':
                if ind == -1:
                        print('no')
                else:
                    print('yes')

            elif query.type == 'add':
                if ind == -1:
                    self.chain_list[hash_val].append(query.s)
            else:
                if ind != -1:
                    self.chain_list[hash_val].pop(ind)

    def process_queries(self):
        n = int(input())
        for i in range(n):
            self.process_query(self.read_query())

if __name__ == '__main__':
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
