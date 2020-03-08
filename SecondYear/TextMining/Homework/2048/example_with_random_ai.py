from game_2048 import game_2048
from random_game_ai import random_game_ai

if __name__ == "__main__":
    game = game_2048()
    random_ai = random_game_ai()
    random_ai.play_game(game)
