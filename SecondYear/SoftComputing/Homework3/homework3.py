import operator as op
from functools import reduce
import random

MAX_NUMBER_OF_GENERATIONS = 10000  # choose a number here
SMALL_NUMBER_PROBABILITY = 0.01


class NQueenState:
    def __init__(self, state):
        self.state = state
        self.fitness_function_value = self.calculate_fitness_function()

    def calculate_fitness_function(self):
        return self.calculate_on_rows() + self.calculate_on_principal_diagonal() + self.calculate_on_secondary_diagonal()

    def calculate_on_rows(self):
        counter = [0 for _ in range(len(self.state))]
        for position in self.state:
            counter[position] += 1

        attacking_queens_on_rows = 0
        for el in counter:
            attacking_queens_on_rows += self.calculate_combinations_of_2(el)

        return attacking_queens_on_rows

    def calculate_on_principal_diagonal(self):
        counter = dict()
        for i, position in enumerate(self.state):
            key = position - i
            if key in counter:
                counter[key] = counter[key] + 1
            else:
                counter[key] = 1

        attacking_queens_on_principal_diagonal = 0
        for el in counter.values():
            attacking_queens_on_principal_diagonal += self.calculate_combinations_of_2(el)

        return attacking_queens_on_principal_diagonal

    def calculate_on_secondary_diagonal(self):
        counter = [0 for _ in range(len(self.state) * 2)]
        for i, position in enumerate(self.state):
            counter[position + i] += 1

        attacking_queens_on_secundary_diagonal = 0
        for el in counter:
            attacking_queens_on_secundary_diagonal += self.calculate_combinations_of_2(el)

        return attacking_queens_on_secundary_diagonal

    def calculate_combinations_of_2(self, n):
        # not combinations for n == 0 and n == 1
        if n == 0 or n == 1:
            return 0
        r = min(2, n)
        numerator = reduce(op.mul, range(n, n - r, -1), 1)
        denominator = reduce(op.mul, range(1, r + 1), 1)

        return int(numerator / denominator)

    def get_fitness_function_value(self):
        return self.fitness_function_value

    def get_state(self):
        return self.state


def create_random_population(n):
    population_size = (n * n) // 2
    population = [generate_random_individ(n) for _ in range(population_size)]

    return population


def generate_random_individ(n):
    random_individ = []
    for _ in range(n):
        random_individ.append(random.randint(0, n - 1))

    return NQueenState(random_individ)


def genetic_algorithm(population):
    current_generation = 1
    global_best_individ = population[0]
    while current_generation < MAX_NUMBER_OF_GENERATIONS:
        new_population = []
        for _ in range(len(population)):
            x = population[random.randint(0, len(population) - 1)].get_state()
            y = population[random.randint(0, len(population) - 1)].get_state()
            child = reproduce(x, y)
            if random.random() <= SMALL_NUMBER_PROBABILITY:
                child = mutate(child)
            new_population.append(NQueenState(child))

        best_indiv = get_best_individual(new_population)
        if best_indiv.get_fitness_function_value() == 0:
            return best_indiv

        if best_indiv.get_fitness_function_value() < global_best_individ.get_fitness_function_value():
            global_best_individ = best_indiv

        print("Generation: " + str(current_generation) + " with best fitness function value: " + str(best_indiv.get_fitness_function_value()))

        current_generation += 1
        population = new_population

    return global_best_individ


def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)

    return x[:c + 1] + y[c + 1:]


def mutate(child):
    new_child = []
    for el in child:
        if el not in new_child:
            new_child.append(el)
    for i in range(len(child)):
        if i not in new_child:
            new_child.append(i)

    left_index = random.randint(0, len(child) // 2)
    right_index = random.randint(len(child) // 2, len(child) - 1)
    new_child[left_index], new_child[right_index] = new_child[right_index], new_child[left_index]

    return new_child


def get_best_individual(population):
    best_indiv = population[0]
    for indiv in population:
        if indiv.get_fitness_function_value() < best_indiv.get_fitness_function_value():
            best_indiv = indiv

    return best_indiv


def print_state_as_matrix(solution):
    out_file = open("output.txt", "w")
    state = solution.get_state()
    out_file.write("Best fitness value: " + str(genetic_algorithm_solution.get_fitness_function_value()) + "\n")
    out_file.write("Found state: " + str(state) + "\n")
    matrix = [[0 for _ in range(len(state))] for _ in range(len(state))]
    for i, j in enumerate(state):
        matrix[j][i] = "Q"

    for el in matrix:
        out_file.write(str(el) + "\n")
    out_file.close()


if __name__ == "__main__":
    n = int(input("Insert value of n:"))
    initial_population = create_random_population(n)
    genetic_algorithm_solution = genetic_algorithm(initial_population)
    print_state_as_matrix(genetic_algorithm_solution)
