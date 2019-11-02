"""
[Exercitiu laborator]
Identificator: python_determina_multimi
Creati o functie cu 3 parametri
calculeaza1(AuB,AiB,AmB)
Functia va avea rolul de a determina multimile A si B, avand in vedere ca parametrii reprezinta multimile A reunit cu B, A intersectat cu B si A-B.
Functia va returna rezultatul sub forma unui tuplu cu cele doua liste.
Creati o functie cu 3 parametri
calculeaza2(AiB,AmB,BmA)
Functia va avea rolul de gpca determina multimile A si B, avand in vedere ca primii 3 parametri reprezinta multimile A intersectat cu B, A-B si B-A.

"""

def calculeaza1(AuB, AiB, AmB):
    B = AuB - AmB
    A = AuB - (B - AiB)
    return A, B


def calculeaza2(AiB, AmB, BmA):
    A = AiB | AmB
    B = BmA | AiB
    return A, B


if __name__ == "__main__":
    print(calculeaza1({1, 2, 3, 4}, {1}, {2}))
    print(calculeaza2({1}, {2}, {3, 4}))
