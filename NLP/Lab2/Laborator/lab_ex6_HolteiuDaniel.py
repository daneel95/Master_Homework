class NotMatrix(Exception):
    def __init__(self, message, errors={}):
        super().__init__(message)
        self.errors = errors


def rezolva(fisier="ex6.txt"):
    try:
        file = open(fisier, "r")
        my_matrix = [el.split(' ') for el in file.read().splitlines() if el]
        my_matrix = [[int(el) for el in row] for row in my_matrix]
        if not all(len(el) == len(my_matrix[0]) for el in my_matrix):
            raise NotMatrix("Nu este matrice")
        return sum([sum(el) for el in my_matrix])
        file.close()
    except FileNotFoundError:
        raise IOError("Fisierul nu a fost gasit")
    except ValueError:
        raise ValueError("Matricea nu este formata din numere")


if __name__ == "__main__":
    # Rulare coredta
    try:
        print(rezolva())
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)
    except NotMatrix as e:
        print(e)
    except:
        print("Another error")

    # Rulare cu fisier inexistent
    try:
        print(rezolva("nu_exista"))
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)
    except NotMatrix as e:
        print(e)
    except:
        print("Another error")


    # Rulare cu elemente care nu sunt numere
    try:
        print(rezolva("ex6_exceptie_value_error.txt"))
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)
    except NotMatrix as e:
        print(e)
    except:
        print("Another error")


    # Rulare cu exceptie custom
    try:
        print(rezolva("ex6_exceptie_custom.txt"))
    except IOError as e:
        print(e)
    except ValueError as e:
        print(e)
    except NotMatrix as e:
        print(e)
    except:
        print("Another error")
