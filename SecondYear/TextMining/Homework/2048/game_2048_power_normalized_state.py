from game_2048 import game_2048
import math


class game_2048_power_normalized_state(game_2048):
    def get_state(self):
        state = self.board.flatten()
        powers_state = []
        for el in state:
            if el == 0:
                powers_state.append(0.0)
            else:
                powers_state.append(math.log(el, 2) / 11.0)  # divide by power of 2 of 2048

        return powers_state
