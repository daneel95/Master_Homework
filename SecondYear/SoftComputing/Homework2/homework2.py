import copy

infinite = 9999  # not real infinite, but a decently big number compared to the size of 8 puzzle problem
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"


class EightPuzzleProblem:
    def __init__(self, matrix):
        self.matrix = matrix
        self.initial_state = EightPuzzleProblemState(self.matrix, 0, None)

    def get_initial_state(self):
        return self.initial_state

    def is_goal_achieved(self, node):
        return node.get_h_value() == 0


class EightPuzzleProblemState:
    def __init__(self, matrix, g_value, parent):
        self.parent = parent
        self.g_value = g_value
        self.matrix = matrix
        self.zero_i = -1
        self.zero_j = -1
        self.f_value = 0
        self.h_value = 0
        self.calculate_h_value(matrix)

    def calculate_h_value(self, matrix):
        # calculate heuristic function value
        h_value = 0
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                if matrix[i][j] == 0:
                    self.zero_i = i
                    self.zero_j = j
                state_current_value = matrix[i][j]
                expected_position = (int(state_current_value / len(matrix)), int(state_current_value % len(matrix)))
                h_value += abs(i - expected_position[0]) + abs(j - expected_position[1])
        self.h_value = h_value
        self.f_value = self.g_value + h_value

    def get_f_value(self):
        return self.f_value

    def get_h_value(self):
        return self.h_value

    def get_g_value(self):
        return self.g_value

    def get_matrix(self):
        return self.matrix

    def set_f_value(self, value):
        self.f_value = value

    def get_child_states(self):
        possible_states = [(self.zero_i - 1, self.zero_j),
                           (self.zero_i, self.zero_j + 1),
                           (self.zero_i + 1, self.zero_j),
                           (self.zero_i, self.zero_j - 1)]
        child_states = []
        for state in possible_states:
            if state[0] < 0 or state[0] >= len(self.matrix) or state[1] < 0 or state[1] >= len(self.matrix):
                continue

            child_state = copy.deepcopy(self.matrix)
            child_state[self.zero_i][self.zero_j] = child_state[state[0]][state[1]]
            child_state[state[0]][state[1]] = 0
            child_states.append(EightPuzzleProblemState(child_state, self.g_value + 1, self))

        return child_states


class Solution:
    def __init__(self):
        self.solution = []

    def add_to_solution(self, matrix):
        self.solution.append(matrix)

    def print_solution(self):
        output_file = "output.txt"
        out = open(output_file, "w")
        self.solution.reverse()
        for state in self.solution:
            write_matrix(state, out)
        out.write("Solution found in: " + str(len(self.solution) - 1) + " steps")  # 1 less step as the first matrix is the initial one
        out.close()


def recursive_best_first_search(problem):
    solution = Solution()
    result, f_value = RBFS(problem, problem.get_initial_state(), infinite, None, solution)
    if result == SUCCESS:
        solution.print_solution()


def RBFS(problem, node, f_limit, previous_state, solution):
    if problem.is_goal_achieved(node):
        # add the goal to the matrix
        solution.add_to_solution(node.get_matrix())
        return SUCCESS, node.get_f_value()

    # get successor states except for the previous one (except for the parent state)
    successors = node.get_child_states()
    for i, suc in enumerate(successors):
        if suc.get_matrix() == previous_state:
            successors.pop(i)

    # if there is no successor then there is a problem so just return failure
    if len(successors) == 0:
        return FAILURE, infinite

    # calculate the f value for children in regard to the parent node
    for suc in successors:
        suc.set_f_value(max(suc.get_g_value() + suc.get_h_value(), node.get_f_value()))

    while True:
        # sort successors by f value
        successors.sort(key=lambda k: k.get_f_value())
        # get the successor with the lowest f value
        best = successors[0]
        # if the best f value is bigger than the limit then we can't get a good solution in this way
        if best.get_f_value() > f_limit:
            return FAILURE, best.get_f_value()
        # if we have only one successor then the alternative limit can be set as f limit else just get the alternative
        # as second successor f value
        if len(successors) < 2:
            alternative = f_limit
        else:
            alternative = successors[1].get_f_value()

        # recursion
        result, new_f_value = RBFS(problem, best, min(f_limit, alternative), node.get_matrix(), solution)
        # change best node's value
        best.set_f_value(new_f_value)
        # if we found the way of solving the problem then we've got the solution so just stop here and end recursion
        if result != FAILURE:
            solution.add_to_solution(node.get_matrix())
            return result, new_f_value


def read_input():
    input_file = open('input.txt', 'r')
    matrix = []
    for line in input_file.read().splitlines():
        matrix.append([int(el) for el in line.split(',')])

    input_file.close()
    return matrix


def write_matrix(matrix, output_file):
    for el in matrix:
        output_file.write(str(el) + "\n")
    output_file.write("=========================\n")


if __name__ == "__main__":
    input_matrix = read_input()
    recursive_best_first_search(EightPuzzleProblem(input_matrix))
