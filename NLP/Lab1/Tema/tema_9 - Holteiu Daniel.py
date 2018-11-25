ALPHABET_LETTERS = [chr(el) for el in range(ord('a'), ord('z') + 1)] # all letterrs from a to z in a constant variable
NUMBER_OF_LETTERS = len(ALPHABET_LETTERS)


def get_matrice():
    new_matrix = [[0] * (NUMBER_OF_LETTERS + 1)] * (NUMBER_OF_LETTERS + 1)  # generate the beggining matrix(0 everywhere). Add 1 more column because the first one is the alphabet
    new_matrix = [[ALPHABET_LETTERS[i]] + new_matrix[i][1:] for i in range(NUMBER_OF_LETTERS)]  # change the first collumn.
    new_matrix = [[None] + ALPHABET_LETTERS] + new_matrix  # change the first row
    return new_matrix


def completeaza_matrice(my_list, matrix):
    for word in my_list:
        word_length = len(word)
        for i in range(word_length - 1):
            for j in range(i + 1, word_length):
                line = ord(word[i]) - ord('a') + 1
                column = ord(word[j]) - ord('a') + 1
                matrix[line][column] += 1
    return matrix


def eliminare_linii_coloane(matrix):
    # get rid of rows that contain only 0
    new_matrix = [row for row in matrix if row[1:].count(0) != len(row) - 1]
    # get rid of columns that contain only 0
    columns_to_delete = []
    new_number_of_rows = len(new_matrix)
    for i in range(NUMBER_OF_LETTERS + 1):  # check for every columns
        delete_column = True
        for j in range(1, new_number_of_rows):
            if new_matrix[j][i] != 0:
                delete_column = False
                break
        if delete_column:
            columns_to_delete.append(i)

    to_substract = 0
    for column in columns_to_delete:
        for row in new_matrix:
            row.pop(column - to_substract)
        to_substract += 1
    return new_matrix


def subpunctul_4(matrix, n):
    # daca perechile trebuie sa fie distincte pe pozitii (adica oricum as lua o pereche (a, b) si o pereche (c, d) atunci a != c si b != d)
    # atunci vor fi mereu distincte
    # Daca prin distincte se intelege fara perechi de forma (a, a) atunci la verificarea valorii din matrice sa fie
    # >= n se va face si verificarea ca matrix[i][0] != matrix[0][j]
    # avand in vedere ca nu inteleg contextul lui "distincte" aici, voi intelege ca distincte se refera la "fara perechi de forma (a, a)
    number_of_rows = len(matrix)
    number_of_columns = len(matrix[0])
    perechi = []
    for i in range(1, number_of_rows):
        for j in range(1, number_of_columns):
            if matrix[i][j] >= n and matrix[i][0] != matrix[0][j]:
                perechi.append((matrix[i][0], matrix[0][j]))
    return perechi


def afisare_matrice(matrix): # functie auxiliara pentru a afisa matricea intr-un format mai usor de citit
    for el in matrix:
        print(el)


if __name__ == "__main__":
    example_list = ["papagal", "pisica", "soarece", "bolovan", "soparla", "catel", "pasare"]

    # subpunctul 1
    matrix = get_matrice()
    print("Subpunctul 1")
    afisare_matrice(matrix)

    # subpunctul 2
    new_matrix = completeaza_matrice(example_list, matrix)
    print("Subpunctul 2")
    afisare_matrice(new_matrix)

    # subpunctul 3
    matrix_without_0 = eliminare_linii_coloane(new_matrix)
    print("Subpunctul 3")
    afisare_matrice(matrix_without_0)

    # subpunctul 4
    n = 2
    print("Subpunctul 4")
    perechi = subpunctul_4(matrix_without_0, n)
    print(perechi)



