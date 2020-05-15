from base.game_2048 import game_2048


MAX_POWER = 11


class game_2048_binary_state(game_2048):
    def get_state(self):
        state = list(self.board.flatten())
        self.state = []  # assuming 2048 is the biggest number achievable
        for el in state:
            if el == 0:
                el = 1

            element_binary_value = '{0:011b}'.format(el)[::-1]
            self.state = self.state + [int(e) for e in element_binary_value]

        return self.state
