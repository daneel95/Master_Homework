def ex1(n):
    return [[el for el in range(1, n + 1)]] * n


def ex2(matrix):
    return [el[::-1] for el in matrix]


def ex3(m1, m2):
    try:
        return [[min(m1[i][j], m2[i][j]) for j in range(max(len(m1[i]), len(m2[i])))] for i in range(max(len(m1), len(m2)))]
    except IndexError:
        raise IndexError("Matricile nu au aceleasi dimensiuni")


def ex4(n):
    return [[0 if i == j else 1 if i < j else -1 for j in range(n)] for i in range(n)]


def ex5(l1, l2):
    return [[0 if l1[i] % 2 == l2[j] % 2 else 1 for j in range(len(l2))] for i in range(len(l1))]


if __name__ == "__main__":
    # ex1
    n = 4
    print("Ex1")
    print(ex1(n))
    # ex2
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    print("Ex2")
    print(ex2(matrix))
    # ex3
    try:
        m1 = [
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"]
        ]
        m2 = [
            ["b", "c", "d"],
            ["c", "d", "h"],
            ["a", "p", "i"]
        ]
        print("Ex3")
        print(ex3(m1, m2))
    except IndexError as e:
        print(e)

    # ex4
    n = 3
    print("Ex4")
    print(ex4(n))
    # ex5
    l1 = [3, 5]
    l2 = [1, 2, 3, 4, 5]
    print("Ex5")
    print(ex5(l1, l2))
