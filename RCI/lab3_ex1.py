def break_not(el):
    # el de forma n(A)
    return el[2:-1]


def create_not(el):
    # el de forma A
    return '{}{}{}'.format('n(', el, ')')


def from_string_to_array(input):
    list_to_return = []
    input = input[1:-1]
    while input.find('[') >= 0:
        open = input.find('[')
        close = input.find(']')
        my_list = input[open + 1:close].replace(' ', '').split(',')
        list_to_return.append(my_list)
        input = input[close + 1:]
    return list_to_return


if __name__ == '__main__':
    # [[w,s,!p], [a,!w,r,t], [q]] -> [[a, s, r, t, !p], [q]]
    # to_read = "[[w, s, n(p)], [a,n(w),r,t],[q]]"
    # to_read = "[[n(q)],[q]]"
    # to_read = "[[n(q), n(p)],[q, p]]"
    with open("lab3_ex1_input.txt", "r") as file:
        to_read = file.read()
    my_list = from_string_to_array(to_read)
    doable = True
    pas = 0
    message_to_show = ""
    while(doable):
        if [] in my_list:
            message_to_show = "NU POATE FI SATISFACUT"
            break
        doable = False
        pas += 1
        print("La pasul {} sirul este: {}".format(pas, my_list))
        indexes_to_eliminate = []
        new_list = []
        for rezolvant, index in zip(my_list, range(len(my_list))):
            for rezolvant_next, index2 in zip(my_list[index + 1:], range(index + 1, len(my_list))):
                for el in rezolvant:
                    if el[0:2] == 'n(' and break_not(el) in rezolvant_next:
                        copy_rezolvant = rezolvant[:]
                        copy_rezolvant.pop(copy_rezolvant.index(el))
                        copy_rezolvant_next = rezolvant_next[:]
                        copy_rezolvant_next.pop(copy_rezolvant_next.index(break_not(el)))
                        new_list.append(list(set(copy_rezolvant + copy_rezolvant_next)))
                        indexes_to_eliminate.append(index)
                        indexes_to_eliminate.append(index2)
                        doable = True
                    elif create_not(el) in rezolvant_next:
                        copy_rezolvant = rezolvant[:]
                        copy_rezolvant.pop(copy_rezolvant.index(el))
                        copy_rezolvant_next = rezolvant_next[:]
                        copy_rezolvant_next.pop(copy_rezolvant_next.index(create_not(el)))
                        new_list.append(list(set(copy_rezolvant + copy_rezolvant_next)))
                        indexes_to_eliminate.append(index)
                        indexes_to_eliminate.append(index2)
                        doable = True
        indexes_to_eliminate = list(set(indexes_to_eliminate))
        indexes_to_eliminate = indexes_to_eliminate[::-1]
        for index in indexes_to_eliminate:
            my_list.pop(index)
        my_list = my_list + new_list
        if not doable:
            message_to_show = "SATISFACUT"
    print("Sirul final: {}".format(my_list))
    with open("lab3_ex1_output.txt", "w") as file:
        file.write(message_to_show)
