if __name__ == "__main__":
    with open("ex11_input.txt", "r") as file:
        my_list = []
        for line in file:
            line = line.split(':')
            nr = int(line[0])
            name = line[1].strip()
            try:
                my_list[nr] = name
            except IndexError:
                my_list = my_list + [""] * (nr - len(my_list) + 1)
                my_list[nr] = name
        print(my_list)
