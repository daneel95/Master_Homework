import os
import wikipedia
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import matplotlib.pyplot as plt


os.environ["JAVAHOME"] = "C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath"  # didn't have java in path on my local machine :)

model_path = "../stanford-postagger-full-2018-10-16/models/english-bidirectional-distsim.tagger"
jar_path = "../stanford-postagger-full-2018-10-16/stanford-postagger.jar"
tagger = StanfordPOSTagger(model_path, jar_path)


def ex1():
    page = wikipedia.page("Shrek")
    content = page.content
    words_in_text = word_tokenize(content)
    print("Title: " + page.title)
    print("First 200 words: ", words_in_text[:200])

    sentences = sent_tokenize(content)
    # get first 20 sentences (or maximum if not having 20)
    first_20_sentences = sentences[:min(20, len(sentences))]
    # word tokenize the sentence and apply tagger
    tagger_results = [tagger.tag(word_tokenize(el)) for el in first_20_sentences]
    print(tagger_results)

    return page


def list_of_words_for_tag(text, tag):
    # break it into sentences
    sentences = sent_tokenize(text)
    # for every sentence, get words (apply word_tokenize) and apply POS Tagger to get tags
    tagger_results = [tagger.tag(word_tokenize(el)) for el in sentences]
    # filter to get only the given tag
    return [el for sublist in tagger_results for (el, word_tag) in sublist if word_tag == tag]


def ex2(text, tags):
    return [el for tag in tags for el in list_of_words_for_tag(text, tag)]


def ex3(text):
    nouns_tags = ["NN", "NNS", "NNP", "NNPS"]
    verbs_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    number_of_words_in_text = get_number_of_words_in_text(text)
    nouns = ex2(text, nouns_tags)
    verbs = ex2(text, verbs_tags)
    print("Nouns: ", nouns)
    print("Verbs: ", verbs)
    print("Percentage of content words: ", (len(nouns) + len(verbs)) / number_of_words_in_text * 100, "%")


def get_number_of_words_in_text(text):
    return len(word_tokenize(text))


def ex4(text, n=5):
    print("Original word | POS | Simple lemmatization | Lemmatization with POS")
    lemma = WordNetLemmatizer()
    sentences = sent_tokenize(text)
    sentences = sentences[:min(n, len(sentences))]
    tagger_results = [tagger.tag(word_tokenize(el)) for el in sentences]
    tagger_results = [el for sublist in tagger_results for el in sublist]
    already_counted = []
    for word, tag in tagger_results:
        word_net_pos = get_wordnet_pos(tag)
        # Do nothing if not a knows (or lemmatizable word)
        if word_net_pos == '':
            continue
        lemmatization = lemma.lemmatize(word)
        lemmatization_with_pos = lemma.lemmatize(word, word_net_pos)
        if lemmatization != lemmatization_with_pos and (word, tag) not in already_counted:
            print_table_row(word, tag, lemmatization, lemmatization_with_pos)
            already_counted.append((word, tag))


def print_table_row(original_word, pos, lemmatization, lemmatization_with_pos):
    print(original_word + " | " + pos + " | " + lemmatization + " | " + lemmatization_with_pos)


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def ex5(text, maximum=5):
    sentences = sent_tokenize(text)
    tagger_results = [tagger.tag(word_tokenize(el)) for el in sentences]
    tagger_results = [el for sublist in tagger_results for el in sublist]
    pos_numbers = dict()
    for _, tag in tagger_results:
        if tag not in pos_numbers:
            pos_numbers[tag] = 1
        else:
            pos_numbers[tag] += 1

    # pos_numbers = pos_numbers[:min(maximum, len(pos_numbers))]
    pos_numbers = [(key, value) for key, value in pos_numbers.items()]
    pos_numbers.sort(key=lambda el: el[1], reverse=True)
    pos_numbers = pos_numbers[:min(maximum, len(pos_numbers))]
    keys = [key for key, _ in pos_numbers]
    values = [value for _, value in pos_numbers]

    plt.bar(keys, values)
    plt.show()

# Voi folosi un text mai scurt pentru teste. Pentru cum este conceputa cerinta, din pacate, se fac multe
# calcule oarecum, degeaba, asa ca voi folosi un text mai scurt pentru a nu astepta foarte mult.
# Daca se vrea rularea pe textul din wikipedia se va rula pe urmatorul text: page.content


TEST_TEXT = "This is my test text. With this test text I will test everything. This is great, amazing text." \
            " I will make this text great again! Why are you running?"

if __name__ == "__main__":
    print("Ex1")
    page = ex1()
    print("Ex3")
    # ex3(page.content)
    ex3(TEST_TEXT)
    print("Ex4")
    ex4(TEST_TEXT)
    print("Ex4")
    ex5(TEST_TEXT)
