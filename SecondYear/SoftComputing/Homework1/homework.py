import copy

FAILURE = "Failure"
CUTOFF = "Cutoff"
SUCCESS = "Success"


# 0 - normal tile
# 1 - walls
# 2 - goal
class RobotProblem:
    def __init__(self, maze):
        self.maze = maze
        self.initial_state = (int(len(maze) / 2), int(len(maze[0]) / 2))
        self.actions = ['N', 'E', 'S', 'W']  # the possible actions

    def is_goal_achieved(self, state):
        if self.maze[state[0]][state[1]] == 2:
            return True
        return False

    def get_initial_state(self):
        return self.initial_state

    def get_actions(self, state):
        x = state[0]
        y = state[1]
        possible_actions = []

        # get the possible actions trying 1 by 1
        if x > 0 and self.maze[x - 1][y] != 1:
            possible_actions.append('N')
        if y < len(self.maze[0]) - 1 and self.maze[x][y + 1] != 1:
            possible_actions.append('E')
        if x < len(self.maze) - 1 and self.maze[x + 1][y] != 1:
            possible_actions.append('S')
        if y > 0 and self.maze[x][y - 1] != 1:
            possible_actions.append('W')

        return possible_actions

    def get_child_node(self, state, action):
        if action == 'N':
            return state[0] - 1, state[1]
        if action == 'E':
            return state[0], state[1] + 1
        if action == 'S':
            return state[0] + 1, state[1]
        if action == 'W':
            return state[0], state[1] - 1

    def is_initial_state_blocked(self):
        return self.maze[self.initial_state[0]][self.initial_state[1]] == 1

    def get_target(self):
        for i, row in enumerate(self.maze):
            exit = row.index(2)
            if exit != -1:
                return i, exit


class Solution:
    def __init__(self):
        self.child_to_parent = dict()

    def add_child_and_parent(self, child, parent):
        self.child_to_parent[child] = parent

    def compute_solution(self, node, initial_state):
        solution = [node]
        while self.child_to_parent[node] != initial_state:
            solution.append(self.child_to_parent[node])
            node = self.child_to_parent[node]

        solution.append(initial_state)  # add the initial state too
        solution.reverse()

        return solution


def write_matrix(matrix, output_file):
    for el in matrix:
        output_file.write(str(el) + '\n')


def pretty_print_solution(problem, solution, output_file):
    if solution == FAILURE:
        output_file.write(FAILURE)
        return
    problem_maze = problem.maze
    for i, state in enumerate(solution):
        problem_maze[state[0]][state[1]] = 'R'
        write_matrix(problem_maze, output_file)
        output_file.write("=====================================\n")
        problem_maze[state[0]][state[1]] = 'P' + str(i)


def BFS(problem):
    if problem.is_initial_state_blocked():
        return FAILURE

    state = problem.get_initial_state()
    if problem.is_goal_achieved(state):
        return [state]

    frontier = [state]
    explored = []
    solution = Solution()  # just for computing the solution

    while True:
        if len(frontier) == 0:
            return FAILURE

        state = frontier.pop(0)
        explored.append(state)
        for action in problem.get_actions(state):
            child = problem.get_child_node(state, action)
            if child in explored or child in frontier:
                continue

            solution.add_child_and_parent(child, state)
            if problem.is_goal_achieved(child):
                return solution.compute_solution(child, problem.get_initial_state())

            frontier.append(child)


def iterative_deepening_search(problem):
    for depth in range(0, len(problem.maze) * len(problem.maze)):
        solution = Solution()
        result = DLS(problem, depth, solution)
        if result == SUCCESS:
            print("Solution found for depth = " + str(depth))
            return solution.compute_solution(problem.get_target(), problem.get_initial_state())

    return FAILURE


def DLS(problem, limit, solution):
    return recursive_DLS(problem.get_initial_state(), problem, limit, [], solution)


def recursive_DLS(node, problem, limit, visited, solution):
    if problem.is_goal_achieved(node):
        return SUCCESS

    if limit == 0:
        return CUTOFF

    visited.append(node)
    cutoff_occurred = False
    for action in problem.get_actions(node):
        child = problem.get_child_node(node, action)
        if child in visited:
            continue

        result = recursive_DLS(child, problem, limit - 1, visited, solution)
        if result == CUTOFF:
            cutoff_occurred = True
        elif result == SUCCESS:
            solution.add_child_and_parent(child, node)
            return result

    if cutoff_occurred:
        return CUTOFF

    return FAILURE


def apply_and_write_bfs_result(problem):
    print("Writing BFS results")
    bfs_solution = BFS(problem)
    output_file = open("BFS_output.txt", "w")
    pretty_print_solution(problem, bfs_solution, output_file)
    output_file.close()


def apply_and_write_iterative_deepening_search(problem):
    print("Printing DLS results")
    dls_solution = iterative_deepening_search(problem)
    output_file = open("DLS_output.txt", "w")
    pretty_print_solution(problem, dls_solution, output_file)
    output_file.close()


def read_input():
    input_file = open('input.txt', 'r')
    maze = []
    for line in input_file.read().splitlines():
        maze.append([int(el) for el in line.split(',')])

    input_file.close()
    return maze


def write_output(output, output_file):
    out = open(output_file, "w")
    out.write(output)
    out.close()


if __name__ == "__main__":
    input_array = read_input()
    apply_and_write_bfs_result(RobotProblem(copy.deepcopy(input_array)))
    apply_and_write_iterative_deepening_search(RobotProblem(copy.deepcopy(input_array)))
