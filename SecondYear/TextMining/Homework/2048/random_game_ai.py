from game_ai import game_ai
import random


# A random moves game ai for testing purposes
class random_game_ai(game_ai):
    def get_move(self, game):
        return random.choice(game.get_available_moves())

    def train(self):
        # Random ai does not require training
        pass

    def play_game(self, game):
        # Plays a game as a random AI
        print(game.get_board())
        while not game.is_game_over():
            _ = game.do_game_round(self.get_move(game))
            print(game.get_board())  # show the game at every step
