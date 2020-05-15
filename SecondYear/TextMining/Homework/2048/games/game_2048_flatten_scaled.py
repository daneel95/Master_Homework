from base.game_2048 import game_2048
import numpy as np


class game_2048_flatten_scaled(game_2048):
    def get_state(self):
        return np.log(self.board.flatten() + 1)
