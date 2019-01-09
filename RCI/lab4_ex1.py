import sys
sys.setrecursionlimit(1500)


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


already_solved = []


def solve_inapoi(atoms, KB):
    # atoms = list(set(atoms))
    if len(atoms) == 0:
        already_solved.append((atoms, KB, "DA"))
        return "DA"
    # print("Atoms: ", atoms)
    # print("KB: ", KB)
    # print("already solved: ", already_solved)
    for c in KB:
        # print("C = ", c)
        # print("Pentru Solve: ", [opposite(atom) for atom in c if atom != atoms[0]] + atoms[1:])
        # print("==============================")
        # if atoms[0] in c:
        #     already_solved.append(atoms[0])
        #     new = [opposite(atom) for atom in c if atom != atoms[0]] + atoms[1:]
            # print("c: ", c)
            # print("new:", new)
            # print("=============")
            # if new[0] in already_solved:
                # print("BBB")
                # return "DA"
            # else:
            #     print("AAAA")
            #     return solve_inapoi([opposite(atom) for atom in c if atom != atoms[0]] + atoms[1:], KB)

        if atoms[0] in c and solve_inapoi([opposite(atom) for atom in c if atom != atoms[0]] + atoms[1:], KB) == "DA":
            return "DA"
    # print("CCC")
    return "NU"


if __name__ == "__main__":
    # Laborator 4 ex1
    with open("lab4_ex1_input.txt", "r") as file:
        KB = from_string_to_array(file.readline())
        propozitii_atomice = from_string_to_array_atomic_prop(file.readline())
    with open("lab4_ex1_output.txt", "w") as file:
        # a = solve_inapoi(propozitii_atomice, KB)
        # for el in propozitii_atomice:
        #     if el not in already_solved:
        #         file.write("NU")
        #         exit(1)
        # file.write("DA")
        file.write(solve_inapoi(propozitii_atomice, KB))
