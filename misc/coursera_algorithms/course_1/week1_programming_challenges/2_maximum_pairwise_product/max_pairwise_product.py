import random

def max_pairwise_product(numbers):
    n = len(numbers)
    max1 = 0
    max1_indx = 0
    max2 = 0
    for i in range(n):
        if numbers[i] > max1:
            max1 = numbers[i]
            max1_indx = i
        
    for i in range(n):
        if numbers[i] > max2 and i != max1_indx:
            max2 = numbers[i]

    return max1 * max2


def max_pairwise_product2(numbers):
    n = len(numbers)
    if n < 2:
        return 0
    if n == 2:
        return numbers[0] * numbers[1]
    max1 = 0
    max1_prev = 0
    max2 = 0
    for i in range(n):
        if numbers[i] > max1:
            max1_prev = max1
            max1 = numbers[i]
    
        if numbers[i] > max1_prev:
                max2 = max1_prev

    return max1 * max2

if __name__ == '__main__':
    for n in range(1, 10):
        input_n = [random.randrange(5) for i in range(n)]
        if not max_pairwise_product(input_n) == max_pairwise_product2(input_n):
            print('fail')
            print(max_pairwise_product(input_n), max_pairwise_product2(input_n))
            print(input_n)
            break
        else:
            print('ok')