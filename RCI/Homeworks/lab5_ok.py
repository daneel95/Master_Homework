counter = 0
cubes = []


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

    file_to_write = open("lab_5_output.txt", "w")
    print_working_memory(file=file_to_write)

    while True:
        rule1_result = rule1()
        if rule1_result:
            print_working_memory(regula=1, cube=rule1_result, file=file_to_write)
            modify_rule1(rule1_result)
            continue
        rule2_result = rule2()
        if rule2_result:
            print_working_memory(regula=2, file=file_to_write)
            modify_rule2(rule2_result, counter)
            continue
        break

    print_working_memory(file=file_to_write)
    file_to_write.close()


