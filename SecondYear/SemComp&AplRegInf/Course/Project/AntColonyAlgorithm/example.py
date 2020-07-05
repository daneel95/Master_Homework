from ant_colony_algorithm_wsd import AntColonyAlgorithmWSD

NUMBER_OF_ALGORITHM_RUNS = 1
VERBOSE = True

# Code using a simple example
if __name__ == "__main__":
    # text = "Computer have mouse and keyboard. Computers will not work without them."
    text = "mouse pilot computers."
    # text = "hear bass sound"
    # text = "I exist"
    # text = "The wolf caught a sheep. Then it ran in the forest."
    best_configuration = None
    best_score = -1
    for i in range(NUMBER_OF_ALGORITHM_RUNS):
        print("Iteration: ", i + 1, "/", NUMBER_OF_ALGORITHM_RUNS)
        aco = AntColonyAlgorithmWSD(text, verbose=VERBOSE)
        aco.run_algorithm()

        final_configuration = aco.get_best_configuration()
        final_configuration_score = final_configuration.get_global_score()
        print("Current score:", final_configuration_score)
        if final_configuration_score >= best_score:
            best_configuration = final_configuration
            best_score = final_configuration_score

    best_senses = best_configuration.get_best_word_senses()
    print("======================================")
    print("Best score found:", best_configuration.get_global_score())
    for word, sense in best_senses:
        print(word.get_text())
        print(sense.get_text())
        print("=================================")
