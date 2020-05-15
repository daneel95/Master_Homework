from base.deep_q_agent import DeepQAgent
from deep_q_learning_model_64_32_package.deep_q_learning_model_64_32 import DeepQLearningModel6432
from games.game_2048_flatten_state import game_2048_flatten_state

NUM_GAMES = 10500
NUM_TRAINING = 10000

if __name__ == "__main__":
    highest_score = 0
    highest_score_value = 2
    game_scores = []
    game_end_boards = []
    highest_score_best = []
    highest_score_every_game = []
    # Define bot
    bot = DeepQAgent(DeepQLearningModel6432())
    for i in range(NUM_GAMES):
        print("Game ", i + 1, "/", NUM_GAMES)
        bot.set_params(is_training=i < NUM_TRAINING, episode=i)
        game = game_2048_flatten_state()
        if i % 5 == 0:
            print(game.get_board().__str__())
        while not game.is_game_over():
            action = bot.get_action(game)
            game.do_game_round(action)
            if i % 5 == 0:
                print("Action = ", action)
                print(game.get_board().__str__())

        # bot.final(game)
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
        print("Highest score until now: ", highest_score)
        print("Highest value until now: ", highest_score_value)
        # save statistics
        highest_score_best.append((highest_score, highest_score_value))
        highest_score_every_game.append((game.get_score(), highest))
        # Write statistics to file!
        # f.write(str(highest_score) + " - " + str(highest_score_value) + "\n")
        # g.write(str(game.get_score()) + " - " + str(highest) + "\n")
        if i % 10 == 0 and i != 0:
            f = open("models/statistics_score_best.txt", "w")
            g = open("models/statistics_every_game.txt", "w")
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
