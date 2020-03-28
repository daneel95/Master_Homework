import wikipedia
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from pycontractions import Contractions
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from num2words import num2words

stop_words = set(stopwords.words('english'))


def ex1():
    page = wikipedia.page("Shrek")
    content = page.content
    words_in_text = word_tokenize(content)
    print("Title: " + page.title)
    print("First 200 words: ", words_in_text[:200])

    return page, words_in_text  # for later usage :)


def ex2(text):
    # it is 3 GB :) takes a lot of time to load
    print("Loading Contractions.... ")
    cont = Contractions('../GoogleNews-vectors-negative300.bin')

    new_text = list(cont.expand_texts([text]))[0]
    print(new_text)

    return new_text


def ex3(page):
    content = page.content
    words_in_text = word_tokenize(content)
    l_words = [el.lower() for el in words_in_text if el.isalpha() or el.isdigit()]
    print("First 50 words of l_words: ", l_words[:50])

    return l_words


def ex4(l_words):
    print("Number of words in l_words before: ", len(l_words))
    without_stop_words = [el for el in l_words if el not in stop_words]
    print("Number of words in l_words after: ", len(without_stop_words))

    return without_stop_words


def ex5(page):
    tokenizer = RegexpTokenizer(r'[^.]\s([A-Z]\w+)')
    text = page.content
    lnm = tokenizer.tokenize(text)
    print("First 5 words in tokenizer: ", lnm[:min(5, len(lnm))])

    return lnm


def ex6(l_words, lnm):
    new_l_words = [el for el in l_words if el.capitalize() not in lnm]
    print("First 50 words in new_l_words: ", new_l_words[:min(50, len(new_l_words))])

    return new_l_words


def ex7(l_words):
    snowball_stemmer = SnowballStemmer("english")
    stemmer_results = [snowball_stemmer.stem(el) for el in l_words]
    print("Snowball Stemmer results: ", stemmer_results)


def ex8(l_words):
    lemma = WordNetLemmatizer()
    lemmatizer_results = [lemma.lemmatize(el) for el in l_words]
    print("Lemmatizer results: ", lemmatizer_results)


def ex9(l_words, n=10):
    number_of_changes = 0
    new_l_words = []
    already_printed = False
    for i in range(len(l_words)):
        if l_words[i].isdigit():
            new_l_words.append(num2words(l_words[i]))
            number_of_changes += 1
        else:
            new_l_words.append(l_words[i])

        if not already_printed and number_of_changes == n:
            already_printed = True
            print("Portion of list that contains first n = ", n, " changes is: ", new_l_words)

    print("Number of changes: ", number_of_changes)
    if not already_printed:
        print("Printing whole list because there were not n=", n, " changes. ", new_l_words)

    return new_l_words


def ex10(page, w):
    text = page.content
    inflexions = get_inflexions(text, w)

    return inflexions


def get_inflexions(text, w):
    inflexions = []
    sentences = sent_tokenize(text)
    snowball_stemmer = SnowballStemmer("english")
    stemmed_w = snowball_stemmer.stem(w)
    for sent in sentences:
        words_in_sentence = word_tokenize(sent)
        words_in_sentence = [el.lower() for el in words_in_sentence if el.isalpha() or el.isdigit()]
        stemmed_words_in_sentence = [(el, snowball_stemmer.stem(el)) for el in words_in_sentence]
        inflexions = inflexions + [el for (el, stem) in stemmed_words_in_sentence if stem == stemmed_w]

    print(inflexions)
    return inflexions


if __name__ == "__main__":
    # print("Test")
    print("Ex1")
    page, words_in_text = ex1()
    # print("Ex2")
    # ex2("I'm trying. He's well. We're good!")  # commenting this as in takes a lot of time
    print("Ex3")
    l_words = ex3(page)
    print("Ex4")
    l_words_no_stop_words = ex4(l_words)
    print("Ex5")
    lnm = ex5(page)
    print("Ex6")
    l_words_without_entity_names = ex6(l_words_no_stop_words, lnm)
    print("Ex7")
    ex7(l_words_without_entity_names)
    print("Ex8")
    ex8(l_words_without_entity_names)

    # The stemmer cuts the end or the beggining of the word by looking into a list of common prefixes and suffixes
    # that can be found into a word (example -ing, -es etc.)
    # On the other hand, lemmatizer, takes into consideration the morphological analysis of the words
    # An example: the word voices from printed example above:
    # Stemmer removes -es suffix => "voices" transforms into "voic"
    # On the other hand Lemmatizer does a morphological analysis so => "voices" transforms into "voice"

    print("Ex9")
    l_words_transformed_numbers = ex9(l_words_without_entity_names)
    print("Ex10")
    inflexions = ex10(page, "directing")
