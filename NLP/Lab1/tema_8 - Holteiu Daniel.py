def subpunct_1(my_list):
    word = input("Insert a word: ")
    try:
        my_list.pop(my_list.index(word))
    except:
        pass
    finally:
        my_list.append(word)
        return my_list


def subpunct_2(my_list):
    # Split by comma and make sure we get rid of spaces before and after the word
    new_list = []
    for text in my_list:
        for word in text.split(','):
            new_list.append(word.strip())
    return new_list


def subpunct_3(character, words_list):
    return [word for word in words_list if character in word]


if __name__ == "__main__":
    example_list = ["margareta", "crizantema", "lalea", " zorea , violeta, orhidee", "trandafir", "gerbera , iasomie", "iris", "crin "]

    # subpunct 1
    new_list = subpunct_1(example_list)
    print("Subpunctul 1")
    print(new_list)

    # subpunctul 2
    new_list = subpunct_2(example_list)
    print("Subpunctul 2")
    print(new_list)

    # subpunctul 3
    words_with_character = subpunct_3('m', new_list)
    print("Subpunctul 3")
    print(words_with_character)

    # subpunctul 4
    sorted_list = sorted(new_list)
    reverse_list = sorted_list[::-1]
    print("Subpunctul 4")
    print(sorted_list)
    print(reverse_list)

