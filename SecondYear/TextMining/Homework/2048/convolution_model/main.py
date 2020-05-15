from games.game_2048_power_16 import game_2048_power_16
from convolution_model.agent import ConvolutionQAgent
from convolution_model.model import ConvolutionModel
from os import path

NUM_GAMES = 200001
NUM_TRAINING = 200001
START_FROM = 192000
MODEL_FILE_NAME = 'model_convolution/DeepQModel.chkpt'
REPLAY_MEMORY_FILE_NAME = 'model_convolution/replay_memory'
STATISTICS_BEST_SCORE_FILE = "model_convolution/statistics_score_best.txt"
STATISTICS_EVERY_GAME_FILE = "model_convolution/statistics_every_game.txt"
EPSILON_FILE_NAME = "model_convolution/epsilon.npy"
STATISTICS_FILE = "model_convolution/statistics_final.txt"
DO_STATISTICS = True

IS_TRAINING = True


if __name__ == "__main__":
    if DO_STATISTICS:
        highest_score_every_game = []
        if path.exists(STATISTICS_BEST_SCORE_FILE):
            g = open(STATISTICS_EVERY_GAME_FILE, "r")

            for el in g.readlines():
                values = el.split(" - ")
                if "(" in values[0]:
                    values[0] = values[0][1:-2]
                score = int(values[0])
                value = int(values[1])
                highest_score_every_game.append((score, value))

            g.close()
        with open(STATISTICS_FILE, "w") as file:
            best_tiles_number = dict()
            games_number = 0
            best_score = 0
            for score, value in highest_score_every_game:
                games_number += 1
                if score > best_score:
                    best_score = score
                if value not in best_tiles_number:
                    best_tiles_number[value] = 1
                else:
                    best_tiles_number[value] += 1
            percentages = dict()
            for key in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
                if key not in best_tiles_number:
                    percentages[key] = "0%"
                else:
                    percentages[key] = str((float(best_tiles_number[key]) / games_number) * 100) + "%"

            file.write("Best score: " + str(best_score) + "\n\n")
            for key in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
                file.write("Tile: " + str(key) + " appeared in: " + percentages[key] + " of games\n")
    else:
        if IS_TRAINING:
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
                    if "(" in values[0]:
                        values[0] = values[0][1:-2]
                    score = int(values[0])
                    value = int(values[1])
                    highest_score_every_game.append((score, value))

                f.close()
                g.close()

            # Define bot
            bot = ConvolutionQAgent(ConvolutionModel(model_file_name=MODEL_FILE_NAME,
                                                     replay_memory_file_name=REPLAY_MEMORY_FILE_NAME,
                                                     epsilon_file_name=EPSILON_FILE_NAME))
            for i in range(START_FROM, NUM_GAMES):
                print("Game ", i + 1, "/", NUM_GAMES)
                bot.set_params(is_training=i < NUM_TRAINING, episode=i)
                game = game_2048_power_16()
                while not game.is_game_over():
                    action = bot.get_action(game)
                    game.do_game_round(action)

                game_scores.append(game.get_score())
                game_end_boards.append(game.get_board())
                # just some statistics
                if game.get_score() > highest_score:
                    highest_score = game.get_score()
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
                highest_score_every_game.append((game.get_score(), highest))
                # Write statistics to file!
                if (i + 1) % 500 == 0 and i != 0:
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
        else:
            # Define bot
            bot = ConvolutionQAgent(ConvolutionModel(model_file_name=MODEL_FILE_NAME,
                                                     replay_memory_file_name=REPLAY_MEMORY_FILE_NAME,
                                                     epsilon_file_name=EPSILON_FILE_NAME))

            games_scores = []
            games_max_values = []
            for i in range(100):
                print("Game ", i + 1, "/", 100)
                bot.set_params(is_training=False, episode=i)
                game = game_2048_power_16(show_ui=True)
                print(game.get_board().__str__())
                while not game.is_game_over():
                    action = bot.get_action(game)
                    game.do_game_round(action)
                    print("Action = ", action)
                    print(game.get_board().__str__())

                games_scores.append(game.get_score())
                games_max_values.append(game.get_highest_value())

            print(games_scores)
            print(games_max_values)
