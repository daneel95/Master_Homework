from nltk.tag.stanford import StanfordPOSTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
import time


model_path = "/Users/holteiu/Desktop/Master_Homework/NLP/stanford-postagger-full-2018-10-16/models/english-bidirectional-distsim.tagger"
jar_path = "/Users/holteiu/Desktop/Master_Homework/NLP/stanford-postagger-full-2018-10-16/stanford-postagger.jar"
tagger = StanfordPOSTagger(model_path, jar_path)
stop_words = set(stopwords.words('english'))


def ex1(text):
    start_time = time.time()
    tokens = nltk.word_tokenize(text)
    print((time.time() - start_time) * 1000)
    with open("out.txt", "w") as file:
        file.write(str(tokens))


def ex2(text):
    start_time = time.time()
    sentences = sent_tokenize(text)
    print((time.time() - start_time) * 1000)
    with open("out.txt", "a") as file:
        file.write("\n")
        file.write(str(len(sentences)))
    return sentences


def ex3(sentences):
    start_time = time.time()
    tokenizer = RegexpTokenizer(r'\w+')
    verbs_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    nouns_tags = ["NN", "NNS", "NNP", "NNPS"]
    with open("out.txt", "a") as file:
        file.write("\n")
        for sentence in sentences:
            file.write("=========================\n")  # a separator between sentences analysis
            file.write("1. Propozitie: {}".format(sentence))
            tokens = tokenizer.tokenize(sentence) # words
            file.write("2. Numarul de cuvinte este {}\n".format(len(tokens)))
            file.write("3. Numarul de stopwords este {}\n".format(len([el for el in tokens if el in stop_words])))
            file.write("4. Cuvintele care nu sunt stop words: {}\n".format(str([el for el in tokens if el not in stop_words])))
            morphologic_analysis = tagger.tag(tokens)
            file.write("5. Analiza morfologica a propozitiei: {}\n".format(morphologic_analysis))
            # din cerinta am inteles ca substantivele si verbele sunt cuvintele tematice
            thematic_words = [el for el in morphologic_analysis if el[1] in verbs_tags or el[1] in nouns_tags]
            file.write("6. Procentul de cuvinte tematice {}%\n".format(len(thematic_words) / float(len(morphologic_analysis)) * 100))
    print((time.time() - start_time) * 1000)


if __name__ == "__main__":
    with open("in.txt", "r") as file:
        text = file.read()
    print("Ex1")
    ex1(text)
    print("Ex2")
    sentences = ex2(text)
    print("Ex3")
    ex3(sentences)


