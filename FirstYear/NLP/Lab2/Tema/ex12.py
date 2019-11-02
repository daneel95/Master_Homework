import re


def functie(file_name):
    with open(file_name, "r+") as file:
        data = file.readlines()
        new_data = []
        for el in data:
            if el == "\n":
                continue
            new_data.append(re.sub(' +', ' ', el))
        file.seek(0)
        file.truncate(0)
        file.write(''.join(new_data))


if __name__ == "__main__":
    functie("ex12_input.txt")
