from nltk.tag.stanford import StanfordPOSTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
# from nltk.book import text2
import nltk
import time
import matplotlib.pyplot as plt
import re
import os
import shutil
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from nltk.draw import TreeView
from cairosvg import svg2png
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

STANFORD_PARSER = "/Users/holteiu/Desktop/Master_Homework/NLP/jars"
STANFORD_MODELS = "/Users/holteiu/Desktop/Master_Homework/NLP/jars"
PARSER_CONSTITUENTI_MODEL_PATH = "/Users/holteiu/Desktop/Master_Homework/NLP/jars/englishPCFG.ser.gz"
STANFORD_PARSER_DEPENDENTE = STANFORD_PARSER + "/stanford-parser.jar"
STANFORD_MODELS_DEPENDENTE = STANFORD_MODELS + "/stanford-parser-3.9.2-models.jar"

os.environ['STANFORD_PARSER'] = STANFORD_PARSER
os.environ['STANFORD_MODELS'] = STANFORD_MODELS
path_to_gs = "/usr/local/Cellar/ghostscript/9.26/bin/"
os.environ['PATH'] += ":{}".format(path_to_gs) # add ghostscript to PATH

parser_constituenti = StanfordParser(model_path=PARSER_CONSTITUENTI_MODEL_PATH)
parser_dependente = StanfordDependencyParser(path_to_jar=STANFORD_PARSER_DEPENDENTE, path_to_models_jar=STANFORD_MODELS_DEPENDENTE)


# model_path = "/Users/holteiu/Desktop/Master_Homework/NLP/stanford-postagger-full-2018-10-16/models/english-bidirectional-distsim.tagger"
# jar_path = "/Users/holteiu/Desktop/Master_Homework/NLP/stanford-postagger-full-2018-10-16/stanford-postagger.jar"
# tagger = StanfordPOSTagger(model_path, jar_path)

POSSIBLE_COMMANDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
folder_reg_expression = "((?![ .<>:\"/\\|?*]).)((?![<>:\"/\\|?*]).)*((?<![ .])\\)?)*$"
phrase_reg_expression = "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"


def print_commands():
    commands = """1) Analiza sintactica bazata pe gramatici de constituenti.
2) Analiza sintactica bazata pe gramatici de dependente.
3) Afiseaza stem-urile impreuna cu cuvintele asociate.
4) Afiseaza cuvintele in forma lor din dictionar, fara repetitii.
5) Pentru un cuvant dat afisati cuvintele din text care ar putea fi inrudite cu el. 
6) Afiseaza cuvintele cu un singur sens.
7) Afiseaza cuvintele polisemantice impreuna cu numarul de sensuri pe care il au.
8) Cel mai probabil sens.
9) Afiseaza relatiile intre synset-urile din text. 
10) Iesire.
Optiunea dumneavoastra este (introduceti un numar de la 1 la 10):"""
    print(commands)


def print_incorrect_command():
    print("Comanda incorecta, reintroduceti optiunea:")


def verify_folder_name_is_valid(folder_name):
    return re.match(folder_reg_expression, folder_name)


def command_1(text):
    output_folder = input("Introduceti numele folderului de output (default este analiza_constituenti): ")
    output_folder = "analiza_constituenti" if output_folder == "" else output_folder
    # verify if output folder is valid

    folder_name_validity = verify_folder_name_is_valid(output_folder)
    while not folder_name_validity:
        output_folder = input("Nume invalid. Introduceti numele folderului de output (default este analiza_constituenti): ")
        output_folder = "analiza_constituenti" if output_folder == "" else output_folder
        folder_name_validity = verify_folder_name_is_valid(output_folder)

    directory_exists = os.path.isdir(output_folder)
    if directory_exists:
        user_answer = ""
        while user_answer not in ["da", "nu"]:
            user_answer = input("Folderul exista deja. Doriti suprascrierea continutului lui? (da/nu). ")
        if user_answer == "nu":
            command_1()
            return
        else:
            shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    # creare fisier arborescent si popularea lui
    with open(output_folder + "/arbori_fraze.txt", "w") as file:
        phrases = re.split(phrase_reg_expression, text)
        for i, phrase in enumerate(phrases):
            phrase_tree = parser_constituenti.raw_parse_sents((phrase,))
            tree = list(list(phrase_tree)[0])[0]
            sentences_number = len([el for el in tree.subtrees(filter=lambda x: x.label() == "S")])
            file.write("Fraza {}: {}\n".format(i + 1, phrase))
            file.write("Numar propozitii: {}\n".format(sentences_number))
            file.write(str(tree))
            file.write("\n")

    # creare folder arbori_fraze + populare
    arbori_fraze_folder_path = output_folder + "/arbori_fraze"
    os.makedirs(arbori_fraze_folder_path)

    # Codul de jos functioneaza pe macos (dupa brew install imagemagick).
    # Nu stiu daca este functional pe windows. In teorie ar trebuii sa functioneze si pe linux

    phrases = re.split(phrase_reg_expression, text)
    for i, phrase in enumerate(phrases):
        phrase_tree = parser_constituenti.raw_parse_sents((phrase,))
        tree = list(list(phrase_tree)[0])[0]
        TreeView(tree)._cframe.print_to_file(arbori_fraze_folder_path + "/fraza_{}.ps".format(i))
        os.system('convert {} {}'.format(arbori_fraze_folder_path + "/fraza_{}.ps".format(i),
                                         arbori_fraze_folder_path + "/fraza_{}.png".format(i)))
        os.remove(arbori_fraze_folder_path + "/fraza_{}.ps".format(i))


def command_2(text):
    output_folder = input("Introduceti numele folderului de output (default este analiza_dependente): ")
    output_folder = "analiza_dependente" if output_folder == "" else output_folder
    folder_name_validity = verify_folder_name_is_valid(output_folder)
    while not folder_name_validity:
        output_folder = input("Nume invalid. Introduceti numele folderului de output (default este analiza_dependente): ")
        output_folder = "analiza_dependente" if output_folder == "" else output_folder
        folder_name_validity = verify_folder_name_is_valid(output_folder)

    directory_exists = os.path.isdir(output_folder)
    if directory_exists:
        user_answer = ""
        while user_answer not in ["da", "nu"]:
            user_answer = input("Folderul exista deja. Doriti suprascrierea continutului lui? (da/nu). ")
        if user_answer == "nu":
            command_2()
            return
        else:
            shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    # creare fisier arborescent si popularea lui
    with open(output_folder + "/dependente_fraze.txt", "w") as file:
        phrases = re.split(phrase_reg_expression, text)
        for i, phrase in enumerate(phrases):
            dependente = parser_dependente.raw_parse(phrase)
            dep = next(dependente)
            file.write("Fraza {}: {}\n".format(i + 1, phrase))
            file.write("Numar dependente: {}\n".format(len(list(dep.triples()))))
            file.write("Dependente:\n")
            for el in list(dep.triples()):
                # Nu m-am chinuit foarte mult sa gasesc pozitiile cuvintelor in text. Pot sa se repete (si nu stiu despre care din ele este vorba).
                # Pot sa fie cuvinte de forma "don't" care sunt, de fapt, "do" si "n't".
                file.write("{}({}-{}, {}-{})\n".format(el[1], el[0][0], 0, el[2][0], 0))
            file.write("\n")

    # creare folder arbori_fraze + populare
    arbori_fraze_folder_path = output_folder + "/dependente_fraze"
    os.makedirs(arbori_fraze_folder_path)

    phrases = re.split(phrase_reg_expression, text)
    for i, phrase in enumerate(phrases):
        dependente = parser_dependente.raw_parse(phrase)
        dep = next(dependente)
        svg_repr = dep._repr_svg_()
        svg2png(bytestring=svg_repr, write_to=arbori_fraze_folder_path + "/fraza_{}.png".format(i))


def command_3(text):
    words = re.split(r"[\s\.,\?!:]", text)
    words = list(filter(lambda el: el != "", words))
    ps = PorterStemmer()
    stems_dictionary = {}
    for i, word in enumerate(words):
        stem = ps.stem(word)
        if stems_dictionary.get(stem):
            stems_dictionary[stem].append((word, i))
        else:
            stems_dictionary[stem] = [(word, i)]
    stem_list = [el for el in stems_dictionary]
    stem_list.sort()
    with open("command_3_results.txt", "w") as file:
        for el in stem_list:
            file.write("{}: {}\n".format(el, ' '.join(["{}({})".format(val[0], val[1]) for val in stems_dictionary[el]])))


def command_4(text):
    words = re.split(r"[\s\.,\?!:]", text)
    words = list(filter(lambda el: el != "", words))
    lemma = WordNetLemmatizer()
    lemma_dictionary = {}
    for i, word in enumerate(words):
        word_lemma = lemma.lemmatize(word)
        if lemma_dictionary.get(word_lemma):
            lemma_dictionary[word_lemma].append((word, i))
        else:
            lemma_dictionary[word_lemma] = [(word, i)]
    lemma_list = [el for el in lemma_dictionary]
    lemma_list.sort()
    with open("command_4_results.txt", "w") as file:
        for el in lemma_list:
            file.write("{}: {}\n".format(el, ' '.join(["{}({})".format(val[0], val[1]) for val in lemma_dictionary[el]])))


if __name__ == "__main__":
    with open("input_text.txt", "r") as file:
        text = file.read()
    while True:
        print_commands()
        command = input()
        while command not in POSSIBLE_COMMANDS:
            print_incorrect_command()
            command = input()
        if command == "10":
            break
        if command == "1":
            command_1(text)
        if command == "2":
            command_2(text)
        if command == "3":
            command_3(text)
        if command == "4":
            command_4(text)
