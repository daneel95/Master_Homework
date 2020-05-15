from base.game_2048 import game_2048
import numpy as np
import math


class game_2048_power_16(game_2048):
    def get_state(self):
        return self.create_state()

    def create_state(self):
        powers = np.zeros(shape=(4, 4, 16), dtype=np.float32)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    powers[i][j][0] = 1.0
                else:
                    power = int(math.log(self.board[i][j], 2))
                    powers[i][j][power] = 1.0

        return powers
