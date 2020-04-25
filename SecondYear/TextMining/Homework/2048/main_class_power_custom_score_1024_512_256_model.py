from deep_q_agent import DeepQAgent
from game_2048_power_state_custom_score import game_2048_power_state_custom_score
from deep_q_learning_model_1024_512_256 import DeepQLearningModel_1024_512_256
from os import path

NUM_GAMES = 5021 - 100 - 345
NUM_TRAINING = 5000 - 100 - 345
MODEL_FILE_NAME = 'models_power_custom_score_1024_model/DeepQModel.chkpt'
REPLAY_MEMORY_FILE_NAME = 'models_power_custom_score_1024_model/replay_memory'
STATISTICS_BEST_SCORE_FILE = "models_power_custom_score_1024_model/statistics_score_best.txt"
STATISTICS_EVERY_GAME_FILE = "models_power_custom_score_1024_model/statistics_every_game.txt"
EPSILON_FILE_NAME = "models_power_custom_score_1024_model/epsilon.npy"


if __name__ == "__main__":
    highest_score = 0
    highest_score_value = 2
    game_scores = []
    game_end_boards = []
    highest_score_best = []
    highest_score_every_game = []

    if path.exists(STATISTICS_BEST_SCORE_FILE):
        f = open(STATISTICS_BEST_SCORE_FILE, "r")
        g = open(STATISTICS_EVERY_GAME_FILE, "r")
        for el in f.readlines():
            values = el.split(" - ")
            score = int(values[0])
            value = int(values[1])
            highest_score_best.append((score, value))
            highest_score = score
            highest_score_value = value

        for el in g.readlines():
            values = el.split(" - ")
            score = int(values[0]),
            value = int(values[1])
            highest_score_every_game.append((score, value))

        f.close()
        g.close()

    # Define bot
    bot = DeepQAgent(DeepQLearningModel_1024_512_256(model_file_name=MODEL_FILE_NAME,
                                                     replay_memory_file_name=REPLAY_MEMORY_FILE_NAME,
                                                     epsilon_file_name=EPSILON_FILE_NAME,
                                                     epsilon=0.05,
                                                     max_replay_memory=25000,
                                                     min_replay_memory=5000,
                                                     batch_size=256))
    for i in range(NUM_GAMES):
        print("Game ", i + 1, "/", NUM_GAMES)
        bot.set_params(is_training=i < NUM_TRAINING, episode=i)
        game = game_2048_power_state_custom_score()
        if i % 5 == 0:
            print(game.get_board().__str__())
        while not game.is_game_over():
            action = bot.get_action(game)
            game.do_game_round(action)
            if i % 5 == 0:
                print("Action = ", action)
                print(game.get_board().__str__())

        # bot.final(game)
        game_scores.append(game.get_score(with_potential=False))
        game_end_boards.append(game.get_board())
        # just some statistics
        if game.get_score(with_potential=False) > highest_score:
            highest_score = game.get_score(with_potential=False)
        highest = game.get_highest_value()
        if highest > highest_score_value:
            highest_score_value = highest

        print("Final Board!")
        print(game.get_board())
        print("Available moves remaining: ", len(game.get_available_moves()))
        print("Highest score until now: ", highest_score)
        print("Highest value until now: ", highest_score_value)
        # save statistics
        highest_score_best.append((highest_score, highest_score_value))
        highest_score_every_game.append((game.get_score(with_potential=False), highest))
        # Write statistics to file!
        # f.write(str(highest_score) + " - " + str(highest_score_value) + "\n")
        # g.write(str(game.get_score()) + " - " + str(highest) + "\n")
        if i % 10 == 0 and i != 0:
            f = open(STATISTICS_BEST_SCORE_FILE, "w")
            g = open(STATISTICS_EVERY_GAME_FILE, "w")
            for el in highest_score_best:
                f.write(str(el[0]) + " - " + str(el[1]) + "\n")
            for el in highest_score_every_game:
                g.write(str(el[0]) + " - " + str(el[1]) + "\n")
            f.close()
            g.close()
        print("=======================================")

    print(game_scores)
    print(game_end_boards)
    print("The end!")
