def two_sum(sequence, t):
    '''
    Args:
        sequence: the given sequence as a list
        t: the given target number, which should be the sum of two selected integers.

    Returns:
        res: A list of tuple. And each tuple would be the idx of two selected integers.
    Example:
        input:
        1 2 3 4
        5
        output:
        0 3
        1 2

    '''
    res = []

    ##############
    #  Please write your own code in the given space.
    #############

    for i in range(len(sequence)):
        x = sequence[i]
        for j in range(i + 1, len(sequence)):
            y = sequence[j]
            if x + y == t:
                res.append((i, j))

    #############

    return res


if __name__ == '__main__':
    for i in range(3):
        print(f'case {i}')
        with open(f'./test_cases/problem1/{i + 1}.txt', 'r') as f:
            seq, tar = f.read().strip().split('\n')
            seq = [*map(int, seq.split(' '))]
            tar = int(tar)

        for item in two_sum(seq, tar):
            print('%d %d' % item)
