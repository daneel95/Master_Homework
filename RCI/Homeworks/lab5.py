# wm = {"counter": 0,
#       "cubes": []}
# rules = []
# 
# 
# class Cube(object):
#     def __init__(self, name, size, position):
#         self.name = name
#         self.size = size
#         self.position = position
# 
#     def __str__(self):
#         return "({}, {})".format(self.name, self.position)
# 
#     def get_value(self, of_what):
#         if of_what == "name":
#             return self.name
#         if of_what == "size":
#             return self.size
#         if of_what == "position":
#             return self.position
#         return False
# 
# 
# class Condition(object):
#     def __init__(self, condition):
#         self.condition = condition
#         self.i = 0
#         self.n = ""
#         self.s = ""
#         self.break_condition()
# 
#     def break_condition(self):
#         self.condition = [el.split(":") for el in self.condition.split(" ")]
#         self.who = self.condition[0][0]
#         self.condition = self.condition[1:]
# 
#     def verify(self, cube, counter):
#         if self.who == "counter":
#             return "counter", True
# 
# 
# class Rule(object):
#     def __init__(self, index, preconditions, conditions, executions):
#         self.index = index
#         self.preconditions = preconditions
#         self.conditions = conditions
#         self.executions = executions
# 
# 
# def use_format(el, cube):
#     return el.format(counter=wm["counter"], name="'{}'".format(cube.name), size=cube.size, position="'{}'".format(cube.position))
# 
# 
# if __name__ == "__main__":
#     with open("lab_5_input.txt", "r") as file:
#         wm_len = int(file.readline())
#         for _ in range(wm_len):
#             wm_input = file.readline()[:-1]
#             wm_input = wm_input.split(" ")
#             wm_input = [el.split(":") for el in wm_input]
#             type_of_memory = wm_input[0][0]
#             if type_of_memory == "counter":
#                 wm[type_of_memory] = int(wm_input[1][1])
#             else:
#                 wm["cubes"].append(Cube(wm_input[1][1], wm_input[2][1], wm_input[3][1]))
# 
#         number_of_rules = int(file.readline())
#         for i in range(number_of_rules):
#             numbers = file.readline()[:-1].split(" ")
#             number_of_pre = int(numbers[0])
#             number_of_conditions = int(numbers[1])
#             number_of_execs = int(numbers[2])
#             preconditions = []
#             conditions = []
#             executions = []
#             for _ in range(number_of_pre):
#                 precondition = file.readline()[:-1].split("--")
#                 preconditions += precondition
#             for _ in range(number_of_conditions):
#                 condition = file.readline()[:-1].split("--")
#                 conditions += condition
#             for _ in range(number_of_execs):
#                 execution = file.readline()[:-1].split("--")
#                 executions += execution
#             rules.append(Rule(i, preconditions, conditions, executions))
#     print(rules)
# 
#     while(True):
#         for rule in rules:
#             preconditions = rule.preconditions
#             conditions = rule.conditions
#             executions = rule.executions
#             # exec all preconditions if we can
#             if preconditions:
#                 for initial_cube in wm["cubes"]:
#                     for el in preconditions:
#                         print(el)
#                         exec(use_format(el, initial_cube))
#                     preconditions_validations = [eval(use_format(el, initial_cube)) for el in preconditions if eval(use_format(el, initial_cube)) is not None]
#                     if all(preconditions_validations):
#                         for other_cube in wm["cubes"]:
#                             for condition in conditions:
#                                 exec(use_format(condition, other_cube))
#                             conditions_validations = [[eval(use_format(el, initial_cube)) for el in conditions if eval(use_format(el, initial_cube)) is not None]]
#                             if all(conditions_validations):
#                                 pass
# 
#

counter = 0
cubes = []
rules = []


class Cube(object):
    def __init__(self, name, size, position):
        self.name = name
        self.size = size
        self.position = position

    def __str__(self):
        return "cube   name: {},  size: {},  position: {}".format(self.name, self.size ,self.position)

    def set_name(self, name):
        self.name = name

    def set_size(self, size):
        self.size = size

    def set_position(self, position):
        self.position = position

    def get_value(self, of_what):
        if of_what == "name":
            return self.name
        if of_what == "size":
            return self.size
        if of_what == "position":
            return self.position
        return False


def print_working_memory(regula=None, cube=None, file=None):
    file.write("Regula {} ".format(regula)) if regula else ""
    if regula == 1:
        file.write("--> n = {}, s = {}".format(cube.get_value("name"), cube.get_value("size")))
    if regula == 2:
        file.write("--> i = {}".format(counter))
    file.write("\n1. counter   value: {}\n".format(counter))
    for index, cube in enumerate(cubes):
        file.write("{}. {}\n".format(index + 2, cube))
    file.write("--------------------------------------------\n")


def rule1():
    for cube in cubes:
        s = cube.get_value("size")
        if cube.get_value("position") == "heap":
            broken = False
            for second_cube in cubes:
                if (second_cube.get_value("position") == "heap" and second_cube.get_value("size") > s) or second_cube.get_value("position") == "hand":
                    broken = True
                    break
            if broken:
                continue
            return cube
    return None


def modify_rule1(cube):
    cube.set_position("hand")


def rule2():
    for cube in cubes:
        if cube.get_value("position") == "hand":
            return cube
    return None


def modify_rule2(cube, i):
    global counter
    cube.set_position(i)
    counter = i + 1


if __name__ == "__main__":
    with open("lab_5_input_ok.txt", "r") as file:
        counter = int(file.readline()[:-1])
        number_of_cubes = int(file.readline()[:-1])
        for _ in range(number_of_cubes):
            cube_info = file.readline()[:-1].split(" ")
            cubes.append(Cube(cube_info[0], int(cube_info[1]), cube_info[2]))


