def ex1(lista):
    return {el for el in lista if len(str(el)) % 2 == 1}


def ex2(matrix, k):
    return {el for (linie, linie_element) in enumerate(matrix) for (coloana, el) in enumerate(linie_element) if linie >= k and coloana >= k}


if __name__ == "__main__":
    # ex1
    lista = [11, 22, 1, 1000, 11, 15, 1, 1, 1, 88346]
    print("Ex1")
    print(ex1(lista))
    # ex2
    matrix = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 1, 2, 3],
        [4, 5, 4, 5, 6],
        [5, 6, 7, 9, 9],
    ]
    k = 2
    print("Ex2")
    print(ex2(matrix, k))
