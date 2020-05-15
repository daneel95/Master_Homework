from games.game_2048_binary_state import game_2048_binary_state
import copy


class game_2048_binary_state_with_custom_score(game_2048_binary_state):
    def get_score(self, with_potential=True):
        if not with_potential:
            return self.score

        potential = 0
        for i in range(0, 4):  # 4 possible moves
            game_clone = copy.copy(self)
            game_clone.do_game_round(i)
            potential += game_clone.get_score(with_potential=False) - self.score

        return self.score + potential // 2
