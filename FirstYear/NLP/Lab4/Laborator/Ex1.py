from nltk.book import text2
import nltk
import time


def ex2(text):
    start_time = time.time()
    words_in_text = [el for el in text if el.isalpha() or el.isdigit()]
    print(len(words_in_text))
    print("Duration: {}".format((time.time() - start_time) * 1000))


def ex4(text):
    start_time = time.time()
    vocabulary = text.vocab()
    no_numbers_or_punctuation_vocabulary = [el for el in vocabulary if el.isalpha()]
    print(len(no_numbers_or_punctuation_vocabulary))
    print("Duration: {}".format((time.time() - start_time) * 1000))


def ex5(text, L):
    start_time = time.time()
    words_in_text = [el for el in text if el.isalpha() or el.isdigit()]
    words_counter = 0
    for el in words_in_text:
        words_counter += 1 if len(el) == L else 0
    print("Duration: {}".format((time.time() - start_time) * 1000))
    return words_counter


def ex6(text, N, L):
    start_time = time.time()
    vocabulary = text.vocab()
    no_punctuation_vocabulary = [el for el in vocabulary if el.isalpha()]
    no_punctuation_vocabulary.sort()
    words_starting_with_L = [el for el in no_punctuation_vocabulary if el[0] == L]
    print(words_starting_with_L[0:N])
    print("Duration: {}".format((time.time() - start_time) * 1000))


def ex7(text):
    # voi presupune ca daca un cuvant apare de mai multe ori in text il voi afisa doar o data
    start_time = time.time()
    vocabulary = text.vocab()
    no_punctuation_vocabulary = [el for el in vocabulary if el.isalpha() or el.isdigit()]
    words_dictionary = {key: len(key) for key in no_punctuation_vocabulary}
    min_length = min(words_dictionary.values())
    max_length = max(words_dictionary.values())
    longest_words = [el for el in words_dictionary if words_dictionary.get(el) == max_length]
    shortest_words = [el for el in words_dictionary if words_dictionary.get(el) == min_length]
    print(longest_words)
    print(shortest_words)
    print("Duration: {}".format((time.time() - start_time) * 1000))


def ex8(text, N):
    start_time = time.time()
    vocabulary = text.vocab()
    no_punctuation_vocabulary = [el for el in vocabulary if el.isalpha() or el.isdigit()]
    words_with_frequency = [(el, text.count(el)) for el in no_punctuation_vocabulary]
    words_with_frequency = sorted(words_with_frequency, key=lambda el: el[1], reverse=True)
    print(words_with_frequency[0:N])
    print("Duration: {}".format((time.time() - start_time) * 1000))


def ex9(text):
    start_time = time.time()
    words_in_text = [el for el in text if el.isalpha() or el.isdigit()]
    print(sum([len(el) for el in words_in_text]) / float(len(words_in_text)))
    print("Duration: {}".format((time.time() - start_time) * 1000))


def ex10(text):
    start_time = time.time()
    vocabulary = text.vocab()
    no_punctuation_vocabulary = [el for el in vocabulary if el.isalpha() or el.isdigit()]
    words_with_frequency = [(el, text.count(el)) for el in no_punctuation_vocabulary]
    print([el[0] for el in words_with_frequency if el[1] == 1])
    print("Duration: {}".format((time.time() - start_time) * 1000))


if __name__ == "__main__":
    print("Ex2")
    ex2(text2)
    print("Ex3")
    start_time = time.time()
    print(text2.name)
    print("Duration: {}".format((time.time() - start_time) * 1000))
    print("Ex4")
    ex4(text2)
    print("Ex5")
    print(ex5(text2, 5))
    print("Ex6")
    ex6(text2, 10, "a")
    print("Ex7")
    ex7(text2)
    print("Ex8")
    ex8(text2, 10)
    print("Ex9")
    ex9(text2)
    print("Ex10")
    ex10(text2)
    print("Ex11")
    start_time = time.time()
    text2.collocations()
    print("Duration: {}".format((time.time() - start_time) * 1000))
