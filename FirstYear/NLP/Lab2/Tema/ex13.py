import itertools


def comanda1():
    with open("input.txt", "r") as file:
        data = file.readlines()
    with open("rezultat_1.txt", "w") as file:
        file.write(''.join(data))


def comanda2(tip):
    with open("input.txt", "r") as file:
        data = file.readlines()
        data = [el.strip().split(" ") for el in data]
        data = list(itertools.chain.from_iterable(data))
    if tip == "asc":
        data = sorted(data)
    elif tip == "desc":
        data = sorted(data)[::-1]
    data = "\n".join(data)
    with open("rezultat_2.txt", "w") as file:
        file.write(data)


def comanda3(lin1, lin2):
    if lin1 > lin2:
        print("Linii gresite. (lin1 > lin2)")
        return -1
    with open("input.txt", "r") as file:
        data = file.readlines()
    if len(data) < lin2 + 1:
        print("Nu exista atat de multe linii.")
        return -1
    lines_to_write = []
    for i in range(lin1, lin2 + 1):
        lines_to_write.append("{}) {}".format(i, data[i]))
    with open("rezultat_3.txt", "w") as file:
        file.write("".join(lines_to_write))


def log_comanda(comanda):
    with open("log.txt", "a") as file:
        file.write(comanda + "\n")


if __name__ == "__main__":
    while True:
        comanda = input("Introduceti numarul comenzii [1 - 4]: ")
        if comanda not in ['1', '2', '3', '4']:
            print("Comanda gresita.")
            continue

        if comanda == '1':
            comanda1()
            log_comanda(comanda)
        if comanda == '2':
            tip = input("Introduceti tipul de sortare [ord, asc, desc]: ")
            if tip not in ['ord', 'asc', 'desc']:
                print("Tip gresit.")
                continue
            comanda2(tip)
            log_comanda(comanda + " - {}".format(tip))
        if comanda == '3':
            lin1 = input("Introduceti linia de inceput: ")
            lin2 = input("Introduceti linia de sfarsit: ")
            try:
                lin1 = int(lin1)
                lin2 = int(lin2)
                if comanda3(lin1, lin2) == -1:
                    continue
                log_comanda(comanda + " : {} - {}".format(lin1, lin2))
            except:
                print("Linii gresite.")
                continue
        if comanda == '4':
            log_comanda(comanda)
            log_comanda("##############################################")
            break
