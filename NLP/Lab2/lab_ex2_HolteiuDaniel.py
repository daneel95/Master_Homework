def subsets(my_set):
    subsets = set()
    for el in my_set:
        aux_subsets = set()
        for el2 in subsets:
            try:
                el2 = list(el2)
            except:
                el2 = [el2]
            el2.append(el)
            aux_subsets.add(frozenset(el2))
        subsets = subsets | aux_subsets | frozenset([el])
    return subsets


def subpunct5(m1, m2):
    return [(a, b) for a in m1 for b in m2]


if __name__ == "__main__":
    subpunct1 = lambda lst: True if len(set(lst)) == 1 else False
    print(subpunct1([1, 1, 1]))
    subpunct2 = lambda sir: True if sir.isalpha() and len(set(sir.lower())) == ord('z') - ord('a') + 1 else False
    print(subpunct2("abcdefghijXXXXXklmnopqrstuvwXyz"))
    subpunct3 = lambda sir1, sir2: True if len(sir1) == len(sir2) and all([sir1.count(el) == sir2.count(el) for el in set(sir1)]) else False
    print(subpunct3("abc", "bac"))
    print(subsets([1, 2, 3, 4]))
    print(subpunct5([1, 2, 3], [4, 5]))


