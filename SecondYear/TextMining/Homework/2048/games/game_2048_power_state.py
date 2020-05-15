from base.game_2048 import game_2048


class game_2048_power_state(game_2048):
    def get_state(self):
        state = self.board.flatten()
        powers_state = []
        for el in state:
            power = 0
            while el > 1:
                power += 1
                el /= 2
            powers_state.append(power)

        # set the state to be used in get_score
        return powers_state
