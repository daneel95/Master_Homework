from game_2048 import game_2048


class game_2048_flatten_state(game_2048):
    def get_state(self):
        self.state = self.board.flatten()
        return list(self.state)