from graph import Node, NodeType, Edge, EdgeType, get_nests, get_word_nodes
from ant import Ant, AntState
from nltk import tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import random
from numpy.random import choice
from constants import C_AC
from aco_configuration import ACOConfiguration
from custom_extended_lesk import WordsEncoder

# This constant is used as "almost 0". As, according to the given formula, the value of pheromone will
# never hit 0, as the update is being done with a multiplication, we chose a smaller number to act as a 0 value
# for bridges destruction
ALMOST_0 = 0.000001


# !! Mandatory a space after a punctuation otherwise it won't split
class AntColonyAlgorithmWSD:
    def __init__(self, text, verbose=True):
        print("Initialize Ant Colony Algorithm")
        self.__words_encoder = self.__intialize_words_encoder(text, with_local_dictionary=True)
        self.__root = self.__initialize_graph(text, self.__words_encoder)
        self.__word_nodes = get_word_nodes(self.__root)
        self.__nests = get_nests(self.__root)
        self.__ants = []  # no ant at the beginning
        self.__best_configuration = None
        self.__verbose = verbose
        if self.__verbose:
            print(self.__root)

    def get_root(self):
        return self.__root

    def get_nests(self):
        return self.__nests

    def get_ants(self):
        return self.__ants

    def get_best_configuration(self):
        return self.__best_configuration

    def run_algorithm(self):
        if self.__verbose:
            print("Running Ant Colony Algorithm for", C_AC, "iterations")
        for i in range(C_AC):
            if self.__verbose:
                print("Iteration:", i + 1, "/", C_AC)
                print("Number of ants:", len(self.__ants))
            self.__iteration()
            current_configuration = ACOConfiguration(self.__word_nodes)
            if self.__best_configuration is None:
                self.__best_configuration = current_configuration
            else:
                if current_configuration.get_global_score() > self.__best_configuration.get_global_score():
                    self.__best_configuration = current_configuration
            if self.__verbose:
                print("Global Score:", self.__best_configuration.get_global_score())

    def __iteration(self):
        # Before doing anything, check if any ant died and remove the dead ants
        self.__remove_dead_ants()
        # Kill ants that returned to parent node
        self.__kill_and_remove_ants_that_returned_to_parent()
        # Switch ant mode to return according to probability
        for ant in self.__ants:
            self.__ant_switch_mode(ant)
        # Create ants
        for nest in self.__nests:
            self.__create_ant(nest)

        # move ants
        for ant in self.__ants:
            self.__ant_movement(ant)

        # Evaporate pheromone
        self.__evaporate_all_edges_pheromone()
        # Decrease ants life cycles
        self.__decrease_all_ants_life_cycle()

    def __create_ant(self, nest):
        probability = nest.calculate_ant_generation_probability()
        random_number = random.uniform(0, 1)
        if random_number < probability and nest.get_energy() > 0:
            ant = Ant(nest, self.__root)
            self.__ants.append(ant)

    def __remove_dead_ants(self):
        indexes_to_remove = []
        for i, ant in enumerate(self.__ants):
            if not ant.is_alive():
                ant.death_mechanic()
                indexes_to_remove.append(i)
        indexes_to_remove.sort(reverse=True)
        for i in indexes_to_remove:
            del self.__ants[i]

    def __kill_and_remove_ants_that_returned_to_parent(self):
        indexes_to_remove = []
        for i, ant in enumerate(self.__ants):
            # if it is in return mode and got to the parent node then kill it and deposit energy
            if ant.current_node == ant.parent_node and ant.get_ant_state() == AntState.RETURN:
                ant.death_mechanic()
                indexes_to_remove.append(i)

        indexes_to_remove.sort(reverse=True)
        for i in indexes_to_remove:
            del self.__ants[i]

    def __ant_movement(self, ant):
        # if ant is in a friend nest it will 100% create a bridge
        if ant.on_friend_nest():  # and ant.get_ant_state() == AntState.RETURN:
            self.__create_bridge_and_move_ant(ant)
            return
        # If not in a friend nest then just randomly choose where to go according to the probability formulas
        # Also, omit the previous node (where the ant came from) -> according to the paper
        ant_current_node = ant.get_current_node()
        # According to the paper it should omit the previous node
        current_node_neighbours = ant_current_node.get_neighbours(omit=ant.get_previous_node())
        probabilities = ant.transition_probabilities(current_node_neighbours)
        # choose 1 (node, edge) to move to according to the probabilities
        indexes = list(range(len(current_node_neighbours)))
        ch = choice(indexes, 1, p=probabilities)
        node, edge = current_node_neighbours[ch[0]]

        # Move the ant through the given edge to the given node
        self.__move_ant(ant, node, edge)

    # movement will do the following
    # 1. Move the ant to the given node through the given edge
    # 2. Deposit pheromone on the edge
    # 3. Collect energy from the node (if not in return mode)
    # 4. Deposit pieces of odour in the current node (randomly)
    def __move_ant(self, ant, node, edge):
        ant.move_ant(node, edge)

    def __create_bridge_and_move_ant(self, ant):
        # don't create a bridge if one exists already
        current_node_neighbours_beneath = ant.get_current_node().get_neighbours_beneath()
        # if we are in a nest that doesn't have a bridge, then create a bridge and move through it
        if len(current_node_neighbours_beneath) == 0:
            bridge = Edge(edge_type=EdgeType.BRIDGE)
            ant_current_node = ant.get_current_node()
            ant_parent_node = ant.get_parent_node()
            ant_current_node.add_neighbour_beneath((ant_parent_node, bridge))
            ant_parent_node.add_previous_node((ant_current_node, bridge))
        # Else if there is a bridge there already, just pick it and move through it
        else:
            bridge = current_node_neighbours_beneath[0][1]  # take the existing bridge

        ant.move_ant_through_bridge(bridge)

    def __evaporate_all_edges_pheromone(self):
        all_edges = self.__root.get_edges_recursive()
        for edge in all_edges:
            edge.evaporate()

        self.__destroy_bridges_if_possible()

    def __destroy_bridges_if_possible(self):
        for nest in self.__nests:
            nest_neighbours_beneath = nest.get_neighbours_beneath()
            nest_neighbours_beneath = self.__remove_destroyed_bridges(nest_neighbours_beneath)
            nest.set_neighbours_beneath(nest_neighbours_beneath)

            nest_neighbours_previous = nest.get_neighbours_previous()
            nest_neighbours_previous = self.__remove_destroyed_bridges(nest_neighbours_previous)
            nest.set_neighbours_previous(nest_neighbours_previous)

    def __remove_destroyed_bridges(self, neighbours):
        indexes = []
        for i, (_, edge) in enumerate(neighbours):
            if edge.is_bridge() and edge.get_pheromone() <= ALMOST_0:
                indexes.append(i)
        indexes.sort(reverse=True)
        for i in indexes:
            del neighbours[i]

        return neighbours

    def __decrease_all_ants_life_cycle(self):
        for ant in self.__ants:
            ant.decrease_life_cycle()

    # randomly switch to return mode according to the calculated probability
    def __ant_switch_mode(self, ant):
        return_mode_probability = ant.return_mode_probability()
        random_number = random.uniform(0, 1)
        if random_number < return_mode_probability:
            ant.set_ant_state(AntState.RETURN)

    def __initialize_graph(self, text, words_encoder):
        root = Node(text)
        sentences = tokenize.sent_tokenize(text)
        for sent in sentences:
            root_sentence_edge = Edge()
            sentence_node = Node(sent, previous_neighbours=[(root, root_sentence_edge)])

            # Add words
            # remove stop words from sentence when looking at words
            words_in_sentence = word_tokenize(sent)
            for w in words_in_sentence:
                if not w.isalnum():  # if it is not alpha numeric (meaning it's punctuation) then skip
                    continue
                synsets = wn.synsets(w)
                if len(synsets) == 0:
                    # if it has no definitions then skip
                    continue

                sentence_word_edge = Edge()
                word_node = Node(w, previous_neighbours=[(sentence_node, sentence_word_edge)])

                # Add senses
                for synset in synsets:
                    sense = synset.definition()
                    word_sense_edge = Edge()
                    sense_node = Node(sense, previous_neighbours=[(word_node, word_sense_edge)],
                                      node_type=NodeType.NEST, words_encoder=words_encoder)

                    # Add the neighbour to word
                    word_node.add_neighbour_beneath((sense_node, word_sense_edge))

                # Add the neighbour to sentence
                sentence_node.add_neighbour_beneath((word_node, sentence_word_edge))

            # Add the neighbour to root
            root.add_neighbour_beneath((sentence_node, root_sentence_edge))

        # if we have only one sentence in text just make that the root
        if len(sentences) == 1:
            return root.get_neighbours_beneath()[0][0]
        return root

    # Initialize the words encoder using only the needed words
    def __intialize_words_encoder(self, text, with_local_dictionary=True):
        if not with_local_dictionary:
            return WordsEncoder()

        dictionary = []
        sentences = tokenize.sent_tokenize(text)
        for sent in sentences:
            words_in_sentence = word_tokenize(sent)
            for w in words_in_sentence:
                if not w.isalnum():  # if it is not alpha numeric (meaning it's punctuation) then skip
                    continue
                synsets = wn.synsets(w)
                if len(synsets) == 0:
                    # if it has no definitions then skip
                    continue
                # Add senses
                for synset in synsets:
                    definition = synset.definition()
                    words = word_tokenize(definition)
                    for w in words:
                        synsets = wn.synsets(w)
                        dictionary += synsets
        return WordsEncoder(dictionary)

