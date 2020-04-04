from nltk.corpus import wordnet


# Din ce am inteles eu, gloss se refera la "marcajul" sensului cuvantului respectiv.
# Spre exemplu: school.v.01
# In principal din clasa Synset se pot scoate mai mult lucruri, spre exemplu definitia, partea de vorbire etc.
def ex1(word):
    synsets = wordnet.synsets(word)
    print("Glosses for word: " + word)
    for el in synsets:
        print(el.name())


# Din ce am inteles dupa ce am cautat internetul :)
# Se pare ca cele 2 cuvinte trebuiesc cautat in "lemmas". Daca sunt amandoua in acelasi set de cuvinte (lemmas)
# Atunci putem spune ca sunt sinonime.
# Probabil nu este 100% necesara cautare in ambele synset-uri.
def ex2(word1, word2):
    synsets_word1 = wordnet.synsets(word1)
    synsets_word2 = wordnet.synsets(word2)

    glosses_for_synonyms = []
    for synset in synsets_word1:
        synonym = check_words_in_synset(synset, word1, word2)
        if synonym is not None:
            glosses_for_synonyms.append(synset.name())

    for synset in synsets_word2:
        synonym = check_words_in_synset(synset, word1, word2)
        if synonym is not None:
            glosses_for_synonyms.append(synset.name())

    glosses_for_synonyms = set(glosses_for_synonyms)
    if len(glosses_for_synonyms) == 0:
        print("No synonym found!")
        return False

    print("All glosses for synonyms: ", glosses_for_synonyms)
    return True


def check_words_in_synset(synset, word1, word2):
    lemma_names = synset.lemma_names()
    if word1 in lemma_names and word2 in lemma_names:
        return synset

    return None


def ex3(synset):
    holonyms = synset.substance_holonyms() + synset.part_holonyms() + synset.member_holonyms()
    meronyms = synset.substance_meronyms() + synset.part_meronyms() + synset.member_meronyms()

    return holonyms, meronyms


# Sper ca am inteles corect. Am printat toate path-urile de hipernime (in reverse pentru ca am plecat de la cuvant
# si m-am dus catre root). Se pare
def ex4(synset):
    hypernyms_paths = synset.hypernym_paths()
    for i, path in enumerate(hypernyms_paths):
        path = [syn.name() for syn in path]
        print("Path", i + 1, ":", path[::-1])


def ex5(synset1, synset2):
    distances_synset1 = synset1.hypernym_distances()
    distances_synset2 = synset2.hypernym_distances()
    minimum_distance = 9999999999  # A big number
    hypernyms_with_minimum_distance = []
    # Iteram si verificam ca cele 2 hipernime sa fie egale (vorbim de d1(k) si d2(k)
    # unde k, dupa cate pot intelege din cerinta, este acelasi hipernim)
    for hyper1, d1 in distances_synset1:
        for hyper2, d2 in distances_synset2:
            if hyper1.name() == hyper2.name():
                if d1 + d2 == minimum_distance:
                    hypernyms_with_minimum_distance.append(hyper1)
                if d1 + d2 < minimum_distance:
                    minimum_distance = d1 + d2
                    hypernyms_with_minimum_distance = [hyper1]

    print("Distanta minima (d1 + d2): ", minimum_distance)
    print("Hypernimele cu distanta minima: ", hypernyms_with_minimum_distance)


def ex6(synset, synsets_list):
    if len(synsets_list) < 5:
        print("Synset list must contain at least 5 elements. It has: ", len(synsets_list))
        return None

    synsets_list.sort(key=lambda el: synset.path_similarity(el))

    return synsets_list


# Nu stiu daca am inteles corect, dar eu am inteles in felul urmator
# Se dau 2 synset-uri (synset1 si synse2) si un alt synset (initial_synset)
# Functia ex7 va returna True daca cele 2 synset-uri (synset1 si synset2) sunt in lista de meronyme indirecte ale
# lui initial_synset. Altfel False.
def ex7(initial_synset, synset1, synset2):
    indirect_meronyms = calculate_all_indirect_meronyms(initial_synset)
    return synset1.name() in indirect_meronyms and synset2.name() in indirect_meronyms


def calculate_all_indirect_meronyms(synset):
    _, meronyms = ex3(synset)
    if len(meronyms) == 0:
        return []

    next_meronyms = []
    for el in meronyms:
        next_meronyms += calculate_all_indirect_meronyms(el)

    return [el.name() for el in meronyms] + next_meronyms


def ex8(word):
    synsets = wordnet.synsets(word)
    synonyms = []
    antonyms = []
    for syn in synsets:
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())

    print("Synonyms: ", set(synonyms))
    print("Antonyms: ", set(antonyms))


if __name__ == "__main__":
    print("Ex1")
    ex1("school")
    print("Ex2")
    ex2("happy", "glad")
    print("Ex3")
    synset = wordnet.synset('tree.n.01')
    holonyms, meronyms = ex3(synset)  # Am ales ca exemplu: "tree.n.01" <-- contine mai multe tipuri de moronime
    print("Holonyms: ", holonyms)
    print("Meronyms: ", meronyms)
    print("Substrance Holonyms: ", synset.substance_holonyms())
    print("Part Holonyms: ", synset.part_holonyms())
    print("Member Holonyms: ", synset.member_holonyms())
    print("Substrance Meronyms: ", synset.substance_meronyms())
    print("Part Meronyms: ", synset.part_meronyms())
    print("Member Meronyms: ", synset.member_meronyms())
    print("Ex4")
    synset = wordnet.synset('apple.n.01')
    ex4(synset)
    print("Ex5")
    synset1 = wordnet.synset('tree.n.01')
    synset2 = wordnet.synset('apple.n.01')
    ex5(synset1, synset2)
    print("Ex6")
    synset_entry = wordnet.synsets("cat")[0]
    synsets_list = [wordnet.synsets("animal")[0], wordnet.synsets("tree")[0], wordnet.synsets("house")[0],
                    wordnet.synsets("object")[0], wordnet.synsets("public_school")[0], wordnet.synsets("mouse")[0]]
    sorted_synsets = ex6(synset_entry, synsets_list)
    print(sorted_synsets)
    print("Ex7")
    print("Ex7 answer: ", ex7(wordnet.synset('tree.n.01'), wordnet.synset('sapwood.n.01'), wordnet.synset('stump.n.01')))
    print("Ex7 answer: ", ex7(wordnet.synset('tree.n.01'), wordnet.synsets('cat')[0], wordnet.synsets('dog')[0]))
    print("Ex8")
    ex8("beautiful")

