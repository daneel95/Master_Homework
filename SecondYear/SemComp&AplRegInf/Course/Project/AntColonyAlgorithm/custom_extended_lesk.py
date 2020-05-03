from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize


# This is not a Lesk algorithm as "in a book". All it does is calculate the overlaps between 2 senses
# that were encoded using indexes.
# Lesk algorithm is called for a word and a sentence and returns the best sense according to the overlaps, which
# this class does not do.
class CustomExtendedLesk:
    def calculate_value(self, encoded_sense_1, encoded_sense_2):
        # do not take into account the 0 values as 0 is not encoded to anything and is a "null" value
        return len([el for el in encoded_sense_1 if el in encoded_sense_2 and el > 0])


# WILL NOT SUPPORT CAN'T AND STUFF WITH COMMA. THEY WILL BE SKIPPED FROM PARSING
class WordsEncoder:
    def __init__(self, dictionary=None):
        print("Initializing words encoder!")
        self.__encoding_dictionary = self.__create_encoding_dictionary(dictionary)

    def __create_encoding_dictionary(self, dictionary=None):
        encoding_value = 1
        encoding_dictionary = {}
        # if no dictionary is mentioned use the whole wordnet dictionary (all existing synsets)
        # If it is mentioned (recommended as it reduces the size of encoding dictionary) use it.
        if dictionary is None:
            synsets = wn.all_synsets()
        else:
            synsets = dictionary
        for ss in synsets:
            for lemma in ss.lemmas():
                if lemma.name() not in encoding_dictionary:
                    encoding_dictionary[lemma.name().lower()] = encoding_value
                    encoding_value += 1

        return encoding_dictionary

    # will not support unknown words or words such as "can't" or "I'm" -> change them to "can not" and "I am"
    def __encode_word(self, word):
        if word.lower() in self.__encoding_dictionary:
            return self.__encoding_dictionary[word.lower()]

        return None

    def get_definition_vector(self, sentence):
        words = word_tokenize(sentence)
        definition_vector = []
        for w in words:
            encoded_word = self.__encode_word(w)
            if encoded_word is not None:
                definition_vector.append(encoded_word)

        definition_vector.sort()

        return definition_vector
