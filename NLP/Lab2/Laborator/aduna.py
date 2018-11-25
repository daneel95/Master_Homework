import sys


def aduna(*args):
    suma = 0
    for nr in args:
        try:
            suma += int(nr)
        except ValueError:
            return "Nu se poate face suma."
    return suma


if __name__ == "__main__":
    args = sys.argv
    print(aduna(*args[1:]))
