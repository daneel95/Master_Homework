from deep_q_agent import DeepQAgent
from game_2048_power_normalized_state import game_2048_power_normalized_state
from deep_q_learning_model_300_300_200_200_100_100_60_60_custom_reward import DeepQLearningModel_300_300_200_200_100_100_60_60_custom_reward
from os import path

NUM_GAMES = 10000 - 7075
NUM_TRAINING = 10000 - 7075
MODEL_FILE_NAME = 'models_power_normalized_custom_reward_300_300_200_200_100_100_60_60/DeepQModel.chkpt'
REPLAY_MEMORY_FILE_NAME = 'models_power_normalized_custom_reward_300_300_200_200_100_100_60_60/replay_memory'
STATISTICS_BEST_SCORE_FILE = "models_power_normalized_custom_reward_300_300_200_200_100_100_60_60/statistics_score_best.txt"
STATISTICS_EVERY_GAME_FILE = "models_power_normalized_custom_reward_300_300_200_200_100_100_60_60/statistics_every_game.txt"
EPSILON_FILE_NAME = "models_power_normalized_custom_reward_300_300_200_200_100_100_60_60/epsilon.npy"

IS_TRAINING = False

if __name__ == "__main__":
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
                score = int(values[0])
                value = int(values[1])
                highest_score_every_game.append((score, value))

            f.close()
            g.close()

        # Define bot
        bot = DeepQAgent(DeepQLearningModel_300_300_200_200_100_100_60_60_custom_reward(
            model_file_name=MODEL_FILE_NAME,
            replay_memory_file_name=REPLAY_MEMORY_FILE_NAME,
            epsilon_file_name=EPSILON_FILE_NAME,
            epsilon=0.02,
            epsilon_steps=10000,
            gamma=0.95,
            learning_rate=0.1,
            max_replay_memory=15000,
            min_replay_memory=3000,
            batch_size=64))
        for i in range(NUM_GAMES):
            print("Game ", i + 1, "/", NUM_GAMES)
            bot.set_params(is_training=i < NUM_TRAINING, episode=i)
            game = game_2048_power_normalized_state()
            if i % 5 == 0:
                print(game.get_board().__str__())
            while not game.is_game_over():
                action = bot.get_action(game)
                game.do_game_round(action)
                if i % 5 == 0:
                    print("Action = ", action)
                    print(game.get_board().__str__())

            bot.final_state(game)

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
            if i % 5 == 0 and i != 0:
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
        bot = DeepQAgent(DeepQLearningModel_300_300_200_200_100_100_60_60_custom_reward(
            model_file_name=MODEL_FILE_NAME,
            replay_memory_file_name=REPLAY_MEMORY_FILE_NAME,
            epsilon_file_name=EPSILON_FILE_NAME,
            epsilon=0.02,
            epsilon_steps=10000,
            gamma=0.95,
            learning_rate=0.1,
            max_replay_memory=15000,
            min_replay_memory=3000,
            batch_size=64))

        games_scores = []
        games_max_values = []
        for i in range(100):
            print("Game ", i + 1, "/", 100)
            bot.set_params(is_training=False, episode=i)
            game = game_2048_power_normalized_state()
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

