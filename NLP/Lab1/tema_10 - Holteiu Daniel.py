def create_dictionary():
    return {"vocale": "aeiou", "consoane": "bcdfghjklmnpqrstvxyz", "cifre": "0123456789"}


def subpunct_2(my_list):
    dictionary = {}
    for el in my_list:
        parts = el.split('-')
        unsplit_word = ''.join(parts)
        for pt in parts:
            if dictionary.get(pt) is None:  # if the element is not yet in the dictionary create the key and add the current word
                dictionary[pt] = [unsplit_word]
            else:
                dictionary[pt].append(unsplit_word)
    return dictionary


def subpunct_3(my_dictionary):
    eliminated_keys = []
    for key in my_dictionary:
        if any(char.isdigit() for char in key):
            eliminated_keys.append(key)
    for key in eliminated_keys:
        del my_dictionary[key]
    return my_dictionary, eliminated_keys


def subpunct_5(my_dictionary):
    silables = []
    auxiliar_dictionary = create_dictionary()
    for key in my_dictionary:
        if len(key) != 3:
            continue
        if key[0] in auxiliar_dictionary.get('consoane') and key[1] in auxiliar_dictionary.get('vocale') and key[2] in auxiliar_dictionary.get('consoane'):
            silables.append(key)
    return silables


if __name__ == "__main__":
    example_list = ["co-pa-cel", "pa-pu-cel", "a-bac", "021-220-20-10", "1-pi-tic", "go-go-nea", "tip-til", "123-456", "a-co-lo", "lo-go-ped", "pa-pa-gal", "co-co-starc"]

    # subpunctul 1
    dictionary = create_dictionary()
    print("Subpunctul 1")
    print(dictionary)

    # subpunctul 2
    new_dictionary = subpunct_2(example_list)
    print("Subpunctul 2")
    print(new_dictionary)

    # subpunctul 3
    new_dictionary, eliminated_keys = subpunct_3(new_dictionary)
    print("Subpunctul 3")
    print(eliminated_keys)

    # subpunct 4
    print("Subpunctul 4")
    print(len(new_dictionary))

    # subpunct 5
    silables = subpunct_5(new_dictionary)
    print("Subpunctul 5")
    print(silables)
