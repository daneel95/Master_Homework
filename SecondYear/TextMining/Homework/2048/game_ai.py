# Abstract class of game_ai that needs to be implemented
class game_ai():
    def get_move(self, game):
        raise NotImplemented()

    def train(self):
        raise NotImplemented()

    def play_game(self, game):
        raise NotImplemented()

    # More to be added, can't think of something that is missing right now
    # The class may change, this is only used for testing the random game at the moment
