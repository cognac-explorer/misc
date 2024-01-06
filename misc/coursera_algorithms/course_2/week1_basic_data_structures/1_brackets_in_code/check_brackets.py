# python3

from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])

def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def find_mismatch(text):
    opening_brackets_stack = []
    for i, next in enumerate(text):
        if next in "([{":
             opening_brackets_stack.append(Bracket(next, i))

        if next in ")]}":

            if len(opening_brackets_stack) == 0:
                return str(i+1)

            prev = opening_brackets_stack.pop()
            if not are_matching(prev.char, next):
                return str(i+1)
    
    if len(opening_brackets_stack) != 0:
        return str(opening_brackets_stack[0].position+1)
    else:
        return 'Success'
            


def main():
    text = input()
    mismatch = find_mismatch(text)
    print(mismatch)


if __name__ == "__main__":
    main()
    # import os
    # path = r'1_brackets_in_code/tests'
    # tests = os.listdir(path)
    # tests.sort()

    # for test in tests:
    #     with open(os.path.join(path, test)) as f:
    #         content = f.read()
    #     if '.a' not in test:
    #         ans = find_mismatch(content)
    #     else:
    #         content = content.rstrip()
    #         print(test, ans, content, content == ans)

