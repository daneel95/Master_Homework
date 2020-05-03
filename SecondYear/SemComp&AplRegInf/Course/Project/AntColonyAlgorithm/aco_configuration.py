from custom_extended_lesk import CustomExtendedLesk


class ACOConfiguration:
    def __init__(self, word_nodes):
        self.__word_nodes = word_nodes
        self.__best_word_senses = self.__get_best_senses()
        self.__global_score = self.__calculate_global_score()

    def __get_best_senses(self):
        best_words_senses = []
        for word_node in self.__word_nodes:
            senses = word_node.get_neighbours_beneath()
            max_energy = -1
            best_sense = None
            for s, _ in senses:
                if s.get_energy() > max_energy:
                    max_energy = s.get_energy()
                    best_sense = s
            best_words_senses.append((word_node, best_sense))

        return best_words_senses

    def __calculate_global_score(self):
        ext_lesk = CustomExtendedLesk()
        global_score = 0
        for _, sense in self.__best_word_senses:
            sense_odour = sense.get_odour()
            for _, s in self.__best_word_senses:
                if s != sense:
                    global_score += ext_lesk.calculate_value(sense_odour, s.get_odour())
        return global_score

    def get_best_word_senses(self):
        return self.__best_word_senses

    def get_global_score(self):
        return self.__global_score
