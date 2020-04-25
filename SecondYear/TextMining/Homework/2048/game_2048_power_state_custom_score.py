from game_2048 import game_2048
import copy


class game_2048_power_state_custom_score(game_2048):
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

    def get_score(self, with_potential=True):
        if not with_potential:
            return self.score

        # Worked really really really bad with this :)
        # if self.is_game_over():
        #     return self.board.max() - 2048

        potential = 0
        for i in range(0, 4):  # 4 possible moves
            game_clone = copy.copy(self)
            game_clone.do_game_round(i)
            # potential += game_clone.get_score(with_potential=False) - self.score
            potential = max(potential, game_clone.get_score(with_potential=False) - self.score)

        # Divide by for because
        # 1. Divide 2 because the potential is calculated twice (for both opposite directions)
        # for example: up and down (cam do both moves if one is possible)

        return potential // 2  # A bit bad too so
        # return self.score + potential // 2
