def ex1(n):
    return {key: [key * el for el in range(1, n+1)] for key in range(1, 10)}


def ex2(matrix):
    return {len(key): sorted(key) for key in matrix}


def ex3(lm):
    return {key: [el for el in lm if key.issubset(el)] for key in lm}


if __name__ == "__main__":
    # ex1
    n = 5
    print("Ex1")
    print(ex1(n))
    # ex2
    matrix = [
        [5, 9, 1],
        [5, 2, 0, 7],
        [1, 4, 3, 0, 8]
    ]
    print("Ex2")
    print(ex2(matrix))
    # ex3
    lm = [frozenset({1, 2}), frozenset({3, 4, 5}), frozenset({3, 5}), frozenset({1, 2, 3, 4, 5}), frozenset({4, 5}), frozenset({1})]
    print("Ex3")
    print(ex3(lm))
