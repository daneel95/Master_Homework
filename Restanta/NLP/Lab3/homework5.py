import os
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser


os.environ["JAVAHOME"] = "C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\javapath"  # didn't have java in path on my local machine :)

# !!! Se pare ca versiunea veche (stanford parser) a devenit deprecated. Noua versiune este stanford-corenlp
models_jar_path = "../stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2-models.jar"
jar_path = "../stanford-corenlp-full-2018-10-05/stanford-corenlp-3.9.2.jar"
depencency_parser = StanfordDependencyParser(path_to_jar=jar_path, path_to_models_jar=models_jar_path)
constituent_parser = StanfordParser(path_to_jar=jar_path, path_to_models_jar=models_jar_path)


if __name__ == "__main__":
    f = open("sentences.txt", "r")
    g = open("results.txt", "w")
    for i, sentence in enumerate(f.readlines()):
        if sentence[-1] == "\n":
            sentence = sentence[:-1]
        g.write("Sentence - number [{}]\n".format(i + 1))
        g.write("[{}]\n".format(sentence))
        # constituent parser
        g.write("[\n")
        sentence_tree = constituent_parser.raw_parse_sents((sentence,))
        tree = list(list(sentence_tree)[0])[0]
        g.write(str(tree) + "\n")
        g.write("]\n")
        # dependency parser
        g.write("[\n")
        dependencies = depencency_parser.raw_parse(sentence)
        dep = next(dependencies)
        for el in list(dep.triples()):
            g.write("{}({}-{}, {}-{})\n".format(el[1], el[0][0], 0, el[2][0], 0))
        g.write("]\n")
        g.write("---------------------------------------------\n")
