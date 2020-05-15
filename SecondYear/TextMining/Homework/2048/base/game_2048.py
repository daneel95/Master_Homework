import numpy as np
from numpy import array, zeros, rot90
import random
from random import randint
from ui.ui import DrawUI, NoUI


# Game class
class game_2048:
    def __init__(self, board_size=4, show_ui=False):
        self.board_size = board_size
        self.__initialize(show_ui=show_ui)

    # Initializes the game with 1 random values already on board
    def __initialize(self, show_ui):
        # Initialize the game
        self.board = zeros((self.board_size, self.board_size), dtype=np.int)
        self.fill_cell()
        self.fill_cell()

        # self.__calculate_available_moves()
        self.__calculate_available_moves()
        self.score = 0
        if show_ui:
            self.ui = DrawUI()
        else:
            self.ui = NoUI()
        self.ui.init_board(self.board)

    def __calculate_available_moves(self):
        available_moves = []
        for i in range(0, 4):  # 4 possible moves
            new_board = self.__move(i)
            if not (new_board == self.board).all():
                available_moves.append(i)

        self.available_moves = available_moves

    # Reset the game no an initial state (so no new game instance is being created)
    def reset_game(self):
        self.__initialize()

    def get_score(self):
        return self.score

    def get_highest_value(self):
        return sorted(list(self.board.flatten()), reverse=True)[0]

    # Make a move and return the new board
    def __move(self, direction, add_score=False):
        # 0: Left, 1: Up, 2: Right, 3: Down
        rotated_board = rot90(self.board, direction)
        cols = [rotated_board[i, :] for i in range(self.board_size)]
        new_board = array([self.move_left(col, add_score) for col in cols])

        return rot90(new_board, -direction)

    # Completes 1 whole game round
    # 1 round means making the move (if possible)
    # and adding 1 new random value of 2 on the board
    def do_game_round(self, direction):
        if direction not in self.available_moves:
            return False
        self.board = self.__move(direction, True)
        self.fill_cell()
        self.__calculate_available_moves()
        self.__draw()

        return True

    # Tells if the game can continue or it's done (no more available moves)
    def is_game_over(self):
        if len(self.available_moves) == 0 or np.isin(2048, self.board):
            self.ui.destroy()
            return True
        return False

    def get_board(self):
        return self.board

    def get_available_moves(self):
        return self.available_moves

    def get_state(self):
        # This should be the game state implementation for AI. It may be moved to game_ai class. TBD
        raise NotImplemented("Implement this method. Inherit from main class game_2048")

    # Adds a random value of 2 on the current board
    def fill_cell(self):
        i, j = (self.board == 0).nonzero()
        if i.size != 0:
            rnd = randint(0, i.size - 1)
            self.board[i[rnd], j[rnd]] = 2 * ((random.random() > .9) + 1)

    # Makes a move to the left.
    # It is the only needed move as making other moves will rotate the whole board
    # so that a move left is needed then it is rotated back
    def move_left(self, col, add_score=False):
        new_col = zeros(4, dtype=col.dtype)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:
                if previous is None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_col[j] = 2 * col[i]
                        if add_score:
                            self.score += new_col[j]
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[i]

        if previous is not None:
            new_col[j] = previous

        return new_col

    def __draw(self):
        self.ui.draw_board(self.board, self.score)
