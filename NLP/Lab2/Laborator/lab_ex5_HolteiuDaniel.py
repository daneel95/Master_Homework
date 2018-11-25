def ex1():
    return [el for el in range(1, 10, 2)]


def ex2():
    return [chr(el) for el in range(ord('a'), ord('z'))]


def ex3(n):
    return [el if el % 2 == 1 else -el for el in range(1, n + 1)]


def ex4(lista):
    return [el for el in lista if el % 2 == 1]


def ex5(lista):
    return [el for (i, el) in enumerate(lista) if i % 2 == 1]


def ex6(lista):
    return [el for (i, el) in enumerate(lista) if i % 2 == el % 2]


# cerinta putin ambigua (exemplul este ambiguu)
def ex7(lista):
    return [(lista[i], lista[i + 1]) for i in range(len(lista) - 1)]


def ex8(n):
    return [["{}*{}={}".format(nr, y, nr * y) for y in range(1, n + 1)] for nr in range(1, n + 1)]


def ex9(sir):
    return [sir[n:] + sir[:n] for n in range(len(sir))]


def ex10(n):
    return [[el] * el for el in range(n)]


if __name__ == "__main__":
    # ex1
    print("Ex1")
    print(ex1())
    # ex2
    print("Ex2")
    print(ex2())
    # ex3
    n = 10
    print("Ex3")
    print(ex3(n))
    # ex4
    lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    print("Ex4")
    print(ex4(lista))
    # ex5
    print("Ex5")
    print(ex5(lista))
    # ex6
    lista = [2, 4, 1, 7, 5, 1, 8, 10]
    print("Ex6")
    print(ex6(lista))
    # ex7
    print("Ex7")
    print(ex7([1, 2, 3, 4]))
    # ex8
    print("Ex8")
    print(ex8(10))
    # ex9
    sir = "abcde"
    print("Ex9")
    print(ex9(sir))
    # ex10
    n = 4
    print("Ex10")
    print(ex10(n))
