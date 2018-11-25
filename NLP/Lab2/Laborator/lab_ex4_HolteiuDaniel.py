def ex1(sir):
    return sorted(sir, key=lambda el: str(el))


def ex2(sir):
    return sorted(sir, key=lambda el: str(el)[::-1])


def ex3(sir):
    return sorted(sir, key=lambda el: len(str(el)))


def ex4(sir):
    return sorted(sir, key=lambda el: len(set(list(str(el)))))


def ex5(sir):
    return sorted(sir, key=lambda el: eval(el))


if __name__ == "__main__":
    example_list = [5, 10, 2, 3, 15, 11, 4, 300, 22, 11, 1, 111]
    # ex1
    print("Ex1")
    print(ex1(example_list))
    # ex2
    print("Ex2")
    print(ex2(example_list))
    # ex3
    print("Ex3")
    print(ex3(example_list))
    # ex4
    print("Ex4")
    print(ex4(example_list))
    # ex5
    example_expression_list = ['1+2+3', '2-5', '3+4', '5*10']
    print("Ex5")
    print(ex5(example_expression_list))
