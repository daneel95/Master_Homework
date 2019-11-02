from nltk.tag.stanford import StanfordPOSTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
# from nltk.book import text2
import nltk
import time
import matplotlib.pyplot as plt


model_path = "/Users/holteiu/Desktop/Master_Homework/NLP/stanford-postagger-full-2018-10-16/models/english-bidirectional-distsim.tagger"
jar_path = "/Users/holteiu/Desktop/Master_Homework/NLP/stanford-postagger-full-2018-10-16/stanford-postagger.jar"
tagger = StanfordPOSTagger(model_path, jar_path)


def ex1():
    start_time = time.time()
    text = "I saw a cat running after a mouse"
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    morphologic_analysis = tagger.tag(tokens)
    print(morphologic_analysis)
    print("Duration: {}".format((time.time() - start_time) * 1000))


def aux_function(parte_vorbire, text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    morphologic_analysis = tagger.tag(tokens)
    return [el[0] for el in morphologic_analysis if el[1] == parte_vorbire]


def ex2(parte_vorbire, text):
    start_time = time.time()
    words_from_text = aux_function(parte_vorbire, text)
    print("Duration: {}".format((time.time() - start_time) * 1000))
    return words_from_text


def ex3(parti_de_vorbire, text):
    start_time = time.time()
    words = []
    for parte_vorbire in parti_de_vorbire:
        words = words + aux_function(parte_vorbire, text)
    print("Duration: {}".format((time.time() - start_time) * 1000))
    return words


def ex4(N, text):
    start_time = time.time()
    parti_de_vorbire = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS",
                        "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "TO",
                        "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]

    my_dictionary = {}

    for parte_vorbire in parti_de_vorbire:
        my_dictionary[parte_vorbire] = len(aux_function(parte_vorbire, text))

    my_list = [(key, value) for key, value in my_dictionary.items()]
    my_list = sorted(my_list, key=lambda el: el[1], reverse=True)
    my_list = my_list[0:N]
    plt.bar([el[0] for el in my_list], [el[1] for el in my_list], color="g")
    plt.show()

    print("Duration: {}".format((time.time() - start_time) * 1000))


if __name__ == "__main__":
    with open("in.txt", "r") as file:
        text = file.read()
    print("Ex1")
    ex1()
    print("Ex2")
    print(ex2("NN", text))
    print("Ex3")
    print(ex3(["VB", "NN"], text))
    print("Ex4")
    ex4(10, text)

