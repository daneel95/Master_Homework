import sys
import operator


def make_array(input):
    list_to_return = []
    input = input[1:-1]
    while input.find('[') >= 0:
        open = input.find('[')
        close = input.find(']')
        my_list = input[open + 1:close].replace(' ', '').split(',')
        list_to_return.append(my_list)
        input = input[close + 1:]
    return list_to_return

def break_not(el):
    # el de forma n(A)
    return el[2:-1]


def create_not(el):
    # el de forma A
    return '{}{}{}'.format('n(', el, ')')


def opposite(el):
    if el[0:2] == 'n(':
        return break_not(el)
    return create_not(el)


class DP(object):
    def __init__(self, S):
        self.response = self.__DP(S)

    def __get_most_app_atom(self, S):
        atom_most_app = {
            "value": 0,
            "atom": None
        }
        strategy_dictionary = {}
        for clauza in S:
            for el in clauza:
                if el not in strategy_dictionary:
                    if el[0:2] != 'n(':
                        strategy_dictionary[el] = 0
                        strategy_dictionary[create_not(el)] = 0
                    else:
                        strategy_dictionary[el] = 0
                        strategy_dictionary[break_not(el)] = 0
                strategy_dictionary[el] = strategy_dictionary.get(el) + 1

        for key in strategy_dictionary:
            if strategy_dictionary.get(key) > atom_most_app.get("value"):
                atom_most_app["value"] = strategy_dictionary.get(key)
                atom_most_app["atom"] = key
        return atom_most_app.get("atom")

    def __SAT(self, S, atom):
        new_S = [clauza for clauza in S if atom not in clauza and opposite(atom) not in clauza]
        new_S_2 = [[el for el in clauza if el != opposite(atom)] for clauza in S if atom not in clauza and opposite(atom) in clauza]
        for clauza in new_S_2:
            if clauza not in new_S:
                new_S.append(clauza)
        return new_S

    def __DP(self, S):
        if not S:
            return "YES"
        if [] in S:
            return "NO"
        chosen_atom = self.__get_most_app_atom(S)
        if self.__DP(self.__SAT(S, chosen_atom)) == "YES":
            return "YES"
        else:
            return self.__DP(self.__SAT(S, opposite(chosen_atom)))


if __name__ == "__main__":
    with open("lab3_ex2_input.txt", "r") as file:
        to_read = file.read()
    my_list = make_array(to_read)
    dp = DP(my_list)
    with open("lab3_ex2_output.txt", "w") as file:
        file.write(dp.response)
