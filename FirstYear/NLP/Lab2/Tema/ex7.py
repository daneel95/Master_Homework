def ex1(lista, n):
    return all(el % n == 0 for el in lista)


def ex2(lista):
    return any(el.isdigit() for el in lista)


def ex3(matrix):
    return any(all(el == 0 for el in row) for row in matrix)


def ex4(sir, lista):
    return all(el in sir for el in lista)


if __name__ == "__main__":
    # ex1
    n = 2
    lista = [2, 4, 6, 8, 10]
    print("Ex1")
    print(ex1(lista, n))
    # ex2
    lista = ["abc", "def", "12222", "abcdefss"]
    print("Ex2")
    print(ex2(lista))
    # ex3
    matrix = [
        [1, 2, 3, 4],
        [0, 0, 0, 0],
        [1, 2, 3, 4],
        [0, 8, 0, 0]
    ]
    print("Ex3")
    print(ex3(matrix))
    # ex4
    sir = "abcdef"
    lista = ["bcd", "f", "ab", "bcd"]
    print("Ex4")
    print(ex4(sir, lista))
