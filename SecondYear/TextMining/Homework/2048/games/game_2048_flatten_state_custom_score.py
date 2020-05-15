from games.game_2048_flatten_state import  game_2048_flatten_state
import copy

class game_2048_flatten_state_custom_score(game_2048_flatten_state):
    def get_score(self, with_potential=True):
        if not with_potential:
            return self.score

        potential = 0
        for i in range(0, 4):  # 4 possible moves
            game_clone = copy.copy(self)
            game_clone.do_game_round(i)
            potential += game_clone.get_score(with_potential=False) - self.score

        # Divide by for because
        # 1. Divide by 2 because I want the potential to be half of the score that is added
        # 2. Divide by another 2 because the potential is calculated twice (for both opposite directions)
        # for example: up and down (cam do both moves if one is possible)
        return self.score + potential // 4
