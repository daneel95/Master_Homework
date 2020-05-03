import math
from constants import E_0, DELTA, L_V
from enum import Enum


class NodeType(Enum):
    NORMAL = 1
    NEST = 2


class EdgeType(Enum):
    NORMAL = 1
    BRIDGE = 2


class Node:
    # text can be either a text, sentence, word or definition of word
    # neighbours must be a list of tuples containing: (node, edge)
    def __init__(self, text, neighbours_beneath=None, previous_neighbours=None, node_type=NodeType.NORMAL, words_encoder=None):
        if neighbours_beneath is None:
            neighbours_beneath = list()
        # this needs to be a list because we can create new edges from any node to a leaf which will have, for
        # some time, more than one previous node
        if previous_neighbours is None:
            previous_neighbours = list()
        self.text = text
        self.neighbours_beneath = neighbours_beneath
        self.previous_neighbours = previous_neighbours
        self.node_type = node_type
        self.energy = E_0
        # Only nests have their odour vector calculated on initialization
        if node_type == NodeType.NEST:
            self.odour = words_encoder.get_definition_vector(text)
        else:
            self.odour = [0 for _ in range(L_V)]

    def add_neighbour_beneath(self, neighbour):
        self.neighbours_beneath.append(neighbour)

    def add_previous_node(self, previous_neighbour):
        self.previous_neighbours.append(previous_neighbour)

    def get_text(self):
        return self.text

    def get_energy(self):
        return self.energy

    def take_energy(self, value):
        if self.energy >= value:
            self.energy -= value
            return value

        # I can extract as much energy as possible until I hit 0
        to_extract = self.energy
        self.energy = 0

        return to_extract

    def deposit_energy(self, value):
        self.energy += value

    # if it's not a leaf make the probability 0
    def calculate_ant_generation_probability(self):
        if not self.is_nest():
            return 0.0

        if self.energy == 0:
            return 0.0

        return (math.atan(self.energy) / math.pi) + 0.5

    def is_nest(self):
        return self.node_type == NodeType.NEST

    def get_neighbours_beneath(self):
        return self.neighbours_beneath

    def get_neighbours_previous(self):
        return self.previous_neighbours

    def set_neighbours_beneath(self, neighbours_beneath):
        self.neighbours_beneath = neighbours_beneath

    def set_neighbours_previous(self, neighbours_previous):
        self.previous_neighbours = neighbours_previous

    def get_neighbours(self, omit=None):
        neighbours = self.neighbours_beneath + self.previous_neighbours
        if omit is not None:
            to_ommit = [el for el in neighbours if el[0] == omit]
            if len(to_ommit) > 0:
                del to_ommit[0]
        return neighbours

    # should be used only for root
    def get_all_neighbours_recursive(self):
        if len(self.neighbours_beneath) == 0:
            return list()

        if self.is_nest():
            return self.neighbours_beneath

        recursive_neighbours = []
        for n, _ in self.neighbours_beneath:
            recursive_neighbours += n.get_all_neighbours_recursive()

        return self.neighbours_beneath + recursive_neighbours

    def get_nodes(self):
        # get nodes beneath and above the current node + current node
        return [el[0] for el in self.neighbours_beneath] + [el[0] for el in self.previous_neighbours] + [self]

    # should be used only for root
    def get_nodes_recursive(self):
        return [el[0] for el in self.get_all_neighbours_recursive()] + [self]

    def get_edges(self):
        # get edges beneath and above the current node
        return [el[1] for el in self.neighbours_beneath] + [el[1] for el in self.previous_neighbours]

    # should be used only for root
    def get_edges_recursive(self):
        return [el[1] for el in self.get_all_neighbours_recursive()]

    def get_nests_recursive(self):
        if self.is_nest():
            return [self]

        nests = []
        for n, _ in self.neighbours_beneath:
            nests += n.get_nests_recursive()

        return nests

    def get_odour(self):
        return self.odour

    def set_odour(self, odour):
        if not self.is_nest():
            self.odour = odour

    # return the whole subtree from beneath it :)
    def __str__(self):
        return self.__get_string("", 0)

    def __get_string(self, string, spaces):
        # string += n.get_text() + " -- " + e.get_test()
        string += "".join([" " for _ in range(spaces)])
        string += self.text + " -- " + str(self.odour)
        string += "\n"
        if spaces == 0:
            spaces = 1
        for n, e in self.neighbours_beneath:
            string = n.__get_string(string, spaces * 2)

        return string


class Edge:
    def __init__(self, edge_type=EdgeType.NORMAL):
        self.pheromone = 0
        self.edge_type = edge_type

    def get_pheromone(self):
        return self.pheromone

    def increase_pheromone(self, value):
        self.pheromone += value

    # This will never hit 0  except for the time when it hits floating point limit
    def evaporate(self):
        self.pheromone = self.pheromone * (1 - DELTA)

    def get_edge_type(self):
        return self.edge_type

    def is_bridge(self):
        return self.edge_type == EdgeType.BRIDGE


def get_nests(root):
    return root.get_nests_recursive()


def get_word_nodes(root):
    all_nodes = root.get_nodes_recursive()
    word_nodes = []
    for node in all_nodes:
        if node.is_nest():
            continue

        neighbours_beneath = node.get_neighbours_beneath()
        if neighbours_beneath[0][0].is_nest():
            word_nodes.append(node)

    return word_nodes
