import copy
import random

MINUS_INFINITY = -9999
INFINITY = 9999


class TicTacToeGame:
    def __init__(self, n):
        self.board_size = n
        self.initialize_game()

    def initialize_game(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.moves_available = self.initialize_available_moves()
        self.game_over = False
        self.player_turn = -1  # -1 = X and 1 = O
        self.winner = None

    def initialize_available_moves(self):
        available_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                available_moves.append((x, y))

        return available_moves

    def get_available_moves(self):
        return self.moves_available

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner

    def get_player(self):
        return "X" if self.player_turn == -1 else "O"

    def is_move_available(self, action):
        return action in self.moves_available

    def reset(self):
        self.initialize_game()

    def move(self, action):
        if self.moves_available.__contains__(action):
            self.board[action[0]][action[1]] = self.get_player()
        else:
            return False

        self.moves_available.remove(action)
        if len(self.moves_available) == 0:
            self.winner = "Draw"
            self.game_over = True

        # check if there is any winner
        self.check_row_for_winner(action[0])
        self.check_collumn_for_winner(action[1])
        self.check_principal_diagonal_for_winner(action[0], action[1])
        self.check_secondary_diagonal_for_winner(action[0], action[1])

        self.player_turn *= -1

        return True

    def check_row_for_winner(self, row):
        for i in range(1, self.board_size):
            if self.board[row][i] != self.board[row][i - 1]:
                break

            if i == self.board_size - 1:
                self.winner = self.get_player()
                self.game_over = True

    def check_collumn_for_winner(self, collumn):
        for i in range(1, self.board_size):
            if self.board[i][collumn] != self.board[i - 1][collumn]:
                break

            if i == self.board_size - 1:
                self.winner = self.get_player()
                self.game_over = True

    def check_principal_diagonal_for_winner(self, row, col):
        if row != col:
            return

        for i in range(1, self.board_size):
            if self.board[i][i] != self.board[i - 1][i - 1]:
                break
            if i == self.board_size - 1:
                self.winner = self.get_player()
                self.game_over = True

    def check_secondary_diagonal_for_winner(self, row, col):
        if self.board_size - 1 - row != col:
            return

        for i in range(1, self.board_size):
            if self.board[self.board_size - 1 - i][i] != self.board[self.board_size - i][i - 1]:
                break
            if i == self.board_size - 1:
                self.winner = self.get_player()
                self.game_over = True

    def __str__(self):
        str_value = ""
        for el in self.board:
            str_value = str_value + str(el) + "\n"
        return str_value[:-1]


def alpha_beta_search(tic_tac_toe_game, player):
    _, action = max_value(tic_tac_toe_game, player, MINUS_INFINITY, INFINITY)
    return action


def max_value(tic_tac_toe_game, player, alpha, beta):
    if tic_tac_toe_game.is_game_over():
        if tic_tac_toe_game.get_winner() == player:
            return 1, None
        if tic_tac_toe_game.get_winner() == "Draw":
            return 0, None
        return -1, None

    best_action = None
    best_value = MINUS_INFINITY
    for action in tic_tac_toe_game.get_available_moves():
        next_board = copy.deepcopy(tic_tac_toe_game)
        next_board.move(action)
        min_value_result, _ = min_value(next_board, player, alpha, beta)

        if min_value_result > best_value:
            best_value = min_value_result
            best_action = action

        if best_value >= beta:
            return best_value, best_action

        alpha = max(alpha, best_value)

    return best_value, best_action


def min_value(tic_tac_toe_game, player, alpha, beta):
    if tic_tac_toe_game.is_game_over():
        if tic_tac_toe_game.get_winner() == player:
            return 1, None
        if tic_tac_toe_game.get_winner() == "Draw":
            return 0, None
        return -1, None

    best_value = INFINITY
    best_action = None

    for action in tic_tac_toe_game.get_available_moves():
        next_board = copy.deepcopy(tic_tac_toe_game)
        next_board.move(action)
        max_value_result, _ = max_value(next_board, player, alpha, beta)
        if max_value_result < best_value:
            best_value = max_value_result
            best_action = action

        if best_value <= alpha:
            return best_value, best_action

        beta = min(beta, best_value)

    return best_value, best_action


if __name__ == "__main__":
    print("Start")
    file = open("input.txt", "r")
    board_size = int(file.readline())
    experiment_runs = int(file.readline())
    file.close()

    winnings = {"X": 0,
                "O": 0,
                "Draw": 0
                }

    file = open("output.txt", "w")
    for i in range(experiment_runs):
        tic_tac_toe = TicTacToeGame(board_size)
        while not tic_tac_toe.is_game_over():
            if i == experiment_runs - 1:
                file.write(str(tic_tac_toe) + "\n\n")
            if tic_tac_toe.get_player() == "X":
                # x = int(input("Insert the row: "))
                # y = int(input("Insert the collumn: "))
                # if tic_tac_toe.is_move_available((x, y)):
                #     tic_tac_toe.move((x, y))
                # else:
                #     print("Invalid move, insert a valid move please!")

                tic_tac_toe.move(random.choice(tic_tac_toe.get_available_moves()))
            else:
                action = alpha_beta_search(tic_tac_toe, "O")
                tic_tac_toe.move(action)
        if i == experiment_runs - 1:
            file.write(str(tic_tac_toe) + "\n\n")

        print("Round " + str(i) + " won by: " + tic_tac_toe.get_winner())
        winnings[tic_tac_toe.get_winner()] = winnings[tic_tac_toe.get_winner()] + 1

    file.write("Bot won: " + str(winnings["O"]))
    file.write("\nRandom won: " + str(winnings["X"]))
    file.write("\nDraws: " + str(winnings["Draw"]))
    file.close()
