from constants import OMEGA, E_MAX, E_A, DELTA_V, L_V
from enum import Enum
from custom_extended_lesk import CustomExtendedLesk
import random


THETA = 0.6  # never mentioned in the paper / course. It must be positive real number


class AntState(Enum):
    EXPLORATION = 1
    RETURN = 2


class Ant:
    def __init__(self, parent_node, root):
        self.life_cycle = OMEGA
        self.parent_node = parent_node
        self.current_node = parent_node
        self.root = root  # this is for interrogating the whole graph.
        self.energy = parent_node.take_energy(1)  # use 1 energy unit for parent to generate an ant
        self.ant_state = AntState.EXPLORATION
        self.odour = parent_node.get_odour()
        self.previous_node = None

    def get_previous_node(self):
        return self.previous_node

    def set_previous_node(self, previous_node):
        self.previous_node = previous_node

    def is_alive(self):
        return self.life_cycle > 0

    def decrease_life_cycle(self):
        self.life_cycle -= 1

    def get_parent_node(self):
        return self.parent_node

    def get_energy(self):
        return self.energy

    def set_current_node(self, node):
        self.current_node = node

    def get_current_node(self):
        return self.current_node

    def set_ant_state(self, state):
        self.ant_state = state

    def get_ant_state(self):
        return self.ant_state

    def transition_probabilities(self, node_edge_pairs):
        denominator = 0
        for nd, ed in node_edge_pairs:
            # won't accept negative eval values so we say that it is 0
            denominator += max(0., self.__eval(nd, ed, node_edge_pairs))

        # If all the eval values are negative or 0 it means we choose equally random to go to a node through an edge
        if denominator == 0:
            return [1.0 / len(node_edge_pairs)] * len(node_edge_pairs)

        probabilities = []
        # if the eval value is < 0 then something is really bad there and the probability will be
        # negative, which is not possible. So the probability assigned to that given node / edge will be 0.0
        for nd, ed in node_edge_pairs:
            prob = max(0.0, self.__eval(nd, ed, node_edge_pairs)) / float(denominator)
            probabilities.append(prob)

        return probabilities

    def return_mode_probability(self):
        return float(self.energy) / E_MAX

    def __eval(self, node, edge, node_edge_pairs):
        return float(self.__eval_node(node, node_edge_pairs=node_edge_pairs) + self.__eval_edge(edge))

    def __eval_node(self, node, node_edge_pairs):
        if self.ant_state == AntState.EXPLORATION:
            return self.__eval_node_exploration(node, node_edge_pairs=node_edge_pairs)

        if self.ant_state == AntState.RETURN:
            return self.__eval_node_return(node, node_edge_pairs=node_edge_pairs)

    def __eval_node_exploration(self, node, node_edge_pairs):
        denominator = 0
        for nd, _ in node_edge_pairs:
            denominator += nd.get_energy()

        # If all the neighbour nodes have their energy depleted so the eval for all neighbour nodes is 0 then return
        # as the evaluation of every node 0.0
        if denominator == 0:
            return 0.0

        return float(node.get_energy()) / float(denominator)

    def __eval_node_return(self, node, node_edge_pairs):
        ext_lesk = CustomExtendedLesk()
        denominator = 0
        for nd, _ in node_edge_pairs:
            denominator += ext_lesk.calculate_value(self.odour, nd.get_odour())

        # If nothing in common with any neighbour node then simply return 0 as the value evaluated in the node,
        if denominator == 0:
            return 0.0

        return float(ext_lesk.calculate_value(self.odour, node.get_odour())) / float(denominator)

    def __eval_edge(self, edge):
        if self.ant_state == AntState.EXPLORATION:
            return 1 - edge.get_pheromone()

        if self.ant_state == AntState.RETURN:
            return edge.get_pheromone()

    def on_friend_nest(self):
        if not self.current_node.is_nest():
            return False

        current_node_parent, _ = self.current_node.get_neighbours_previous()[0]
        parent_node_parent, _ = self.parent_node.get_neighbours_previous()[0]

        # returns true (meaning on a friend nest) if the current nest where the ant is has a different word than
        # the parent node word node
        return not (current_node_parent == parent_node_parent)

    def __deposit_pheromone(self, edge):
        edge.increase_pheromone(THETA)

    def __deposit_odour_components(self, node):
        if node.is_nest():
            return

        sample_length = int(len(self.odour) * DELTA_V)
        # take a sample of odour components from ant odour array
        ant_odour_sample = random.sample(self.odour, sample_length)

        node_odour = node.get_odour()
        # Randomly pick some indexes from node odour array (we know it has length L_V)
        all_indexes = list(range(len(node_odour)))
        node_odour_index_samples = random.sample(all_indexes, sample_length)
        for i in range(sample_length):
            node_odour[node_odour_index_samples[i]] = ant_odour_sample[i]

        node.set_odour(node_odour)

    # when an ant dies, it deposits the energy in the current node
    def death_mechanic(self):
        if not self.is_alive():
            self.current_node.deposit_energy(self.energy)

    # The energy that an ant can have is maximum E_MAX
    # Also, the ant will always take E_A energy from a node
    # The and will also randomly leave pieces from its odour vector to the node odour
    def move_ant(self, node, edge):
        self.previous_node = self.current_node
        self.__deposit_pheromone(edge)  # deposit pheromone
        self.current_node = node  # set current node as the node we move to
        # take E_A energy from the current node IF not in return mode
        if self.ant_state == AntState.EXPLORATION:
            to_add_energy = node.take_energy(E_A)
            energy_diff = (self.energy + to_add_energy) - E_MAX
            if energy_diff >= 0:
                self.energy = E_MAX
                node.deposit_energy(energy_diff)  # deposit back the energy that goes over max energy
        # Deposit odour pieces
        self.__deposit_odour_components(node)

    def move_ant_through_bridge(self, bridge):
        self.previous_node = self.current_node
        self.__deposit_pheromone(bridge)
        self.current_node = self.parent_node
