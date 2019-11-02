def subpunct_2(text):
    non_alpha_list = [character for character in text if character.isdigit() is False and character.isalpha() is False and character != '-']
    return list(set(non_alpha_list))


def subpunct_3(text, delimiters):
    text = text.lower()
    if not delimiters:
        return text

    text = text.split(delimiters.pop(0))
    for delim in delimiters:
        new_words = []
        for word in text:
            if word == "":
                continue
            new_words += word.split(delim)
        text = new_words
    # just a single instance of the same word
    text = list(set(text))
    try:
        empty_index = text.index("")
        text.pop(empty_index)
    except:
        pass
    return text


def subpunctul_5(words):
    nouns = [word for word in words if word.endswith('ul')]
    return nouns


def subpunctul_6(words):
    return [word for word in words if word.find('-') > 0]


if __name__ == "__main__":
    example_text = "Candva, demult, acum 1000 de ani traia o printesa intr-un castel. Si printesa intr-o zi auzi cum aparuse pe meleagurile sale un cufar fermecat din care iesea grai omenesc. Printesa curioasa strabatu 7 ulite si 7 piete; ajunse la cufar si vazu ca toti stateau la 100 metri distanta de el si se mirau. Din cufar intr-adevar se auzeau vorbe nedeslusite. Printesa curajoasa se duse sa-i vorbeasca. Il intreba cine e si ce dorinte are. Raspunsul fu: \"Sunt Ion am cazut in cufar si m-am ferecat din gresala. As dori sa ies.\". Printesa deschise cufarul si-l elibera pe Ion. \"Multumesc\" spuse Ion. Si astfel, povestea cufarului fermecat a fost deslusita."
    # subpunct 1
    text_length = len(example_text)
    print("Subpunctul 1")
    print(text_length)

    # subpunctul 2
    non_alpha_list = subpunct_2(example_text)
    print("Subpunctul 2")
    print(non_alpha_list)

    # subpunct 3
    words = subpunct_3(example_text, non_alpha_list)
    print("Subpunctul 3")
    print(words)

    # subpunctul 4 -> cerinta goala :)

    # subpunctul 5
    nouns = subpunctul_5(words)
    print("Subpunctul 5")
    print(nouns)

    # subpunctul 6
    cratima = subpunctul_6(words)
    print("Subpunctul 6")
    print(cratima)
