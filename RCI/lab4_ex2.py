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


def from_string_to_array(input):
    list_to_return = []
    input = input[1:-1]
    while input.find('[') >= 0:
        open = input.find('[')
        close = input.find(']')
        my_list = input[open + 1:close].replace(' ', '').split(',')
        list_to_return.append(my_list)
        input = input[close + 1:]
    return list_to_return


def from_string_to_array_atomic_prop(input):
    return input[1:-1].replace(' ', '').split(',')


def get_all_atoms(my_list):
    atoms = []
    for clause in my_list:
        for atom in clause:
            if atom[0:2] == 'n(':
                atom_aux = opposite(atom)
            else:
                atom_aux = atom
            if atom_aux not in atoms:
                atoms.append(atom_aux)
    return atoms


def verifica_atom_marcat(atom, propozitii_atomice_marcate):
    return (atom, True) in propozitii_atomice_marcate


def verificare_clauza_pas2(clauza, propozitii_atomice_marcate):
    for atom in clauza:
        if atom[0:2] == 'n(':
            if not verifica_atom_marcat(opposite(atom), propozitii_atomice_marcate):
                return False
        else:
            if verifica_atom_marcat(atom, propozitii_atomice_marcate):
                return False
    return True


def get_positive_atom(clauza):
    return [el for el in clauza if el[0:2] != 'n('][0]


def verifica_toate_marcate(propozitii_atomice_marcate, propozitii_atomice):
    for el in propozitii_atomice:
        if (el, True) not in propozitii_atomice_marcate:
            return False
    return True
    # return all([atom_marcat[1] for atom_marcat in propozitii_atomice_marcate])


def solve_inainte(propozitii_atomice, KB):
    # marcam (ca rezolvate sau nerezolvate) tot ce se poate - pas initial
    propozitii_atomice_marcate = []
    # for atom in propozitii_atomice:
    #     propozitii_atomice_marcate.append((atom, [atom] in KB))
    for clauza in KB:
        for atom in clauza:
            atom = atom if 'n(' not in atom else opposite(atom)
            if (atom, False) not in propozitii_atomice_marcate:
                propozitii_atomice_marcate.append((atom, False))

    while(True):
        # pasul 1
        # print("Propozitii atomice marcate: ", propozitii_atomice_marcate)
        if verifica_toate_marcate(propozitii_atomice_marcate, propozitii_atomice):
            return "DA"

        for_complete = True
        # pasul 2
        for clauza in KB:
            # print("Verific clauza: ", clauza)
            # print("Deja pozitive: ", propozitii_atomice_marcate)
            # print("=========================")
            if verificare_clauza_pas2(clauza, propozitii_atomice_marcate):
                # print("+++++++++++++++++")
                # print(clauza, propozitii_atomice_marcate)
                # print("Verificare reusita, marchez")
                positive_atom = get_positive_atom(clauza)
                index_to_mark = propozitii_atomice_marcate.index((positive_atom, False))
                propozitii_atomice_marcate[index_to_mark] = (positive_atom, True)
                for_complete = False
                break
        # print(KB, propozitii_atomice_marcate)
        if not for_complete:
            continue
        return "NU"

    # return "NO"


if __name__ == "__main__":
    # Laborator 4 ex2
    with open("lab4_ex2_input.txt", "r") as file:
        KB = from_string_to_array(file.readline())
        propozitii_atomice = from_string_to_array_atomic_prop(file.readline())

    with open("lab4_ex2_output.txt", "w") as file:
        file.write(solve_inainte(propozitii_atomice, KB))
