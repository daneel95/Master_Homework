from deep_q_learning_model_300_300_200_200_100_100_60_60_package.deep_q_learning_model_300_300_200_200_100_100_60_60 import DeepQLearningModel_300_300_200_200_100_100_60_60
import numpy as np
import math


class DeepQLearningModel_300_300_200_200_100_100_60_60_custom_reward(DeepQLearningModel_300_300_200_200_100_100_60_60):
    def __init__(self,
                 model_file_name='models/DeepQModel.chkpt',
                 replay_memory_file_name='models/replay_memory',
                 epsilon_file_name='models/epsilon.npy',
                 epsilon=0.05,
                 gamma=0.9,
                 max_replay_memory=25000,
                 min_replay_memory=5000,
                 batch_size=512,
                 epsilon_steps=5000,
                 learning_rate=0.01):
        super().__init__(model_file_name=model_file_name,
                         replay_memory_file_name=replay_memory_file_name,
                         epsilon=epsilon,
                         max_replay_memory=max_replay_memory,
                         epsilon_file_name=epsilon_file_name,
                         min_replay_memory=min_replay_memory,
                         batch_size=batch_size,
                         epsilon_steps=epsilon_steps,
                         gamma=gamma,
                         learning_rate=learning_rate)

    def get_reward(self, game):
        reward = 0
        if 2048 in game.get_board():
            reward = 1.0

        return reward + (self.get_number_of_tiles_merged(game) - 1) / 8.0 + \
               self.get_difference_power_normalized(game) + \
               self.get_score_normalized(game) + \
               self.add_score_for_corner_max(game)

    def get_number_of_tiles_merged(self, game):
        return np.count_nonzero(game.get_board() == 0) \
               - np.count_nonzero(self.last_state.get_board() == 0) + 1

    def get_difference_power_normalized(self, game):
        max_current = np.amax(game.get_board())
        max_old = np.amax(self.last_state.get_board())
        if max_current - max_old == 0:
            return 0.0

        return math.log(max_current - max_old) / 10.0

    def get_score_normalized(self, game):
        score_diff = game.get_score() - self.last_state.get_score()

        return score_diff / 2048.0

    def add_score_for_corner_max(self, game):
        max_current = np.amax(game.get_board())
        position = np.where(game.get_board() == max_current)
        xs = list(position[0])
        ys = list(position[1])

        for x, y in zip(xs, ys):
            if x == 0 and y == 0:
                return math.log(max_current, 2) / 11.0

            if x == 3 and y == 0:
                return math.log(max_current, 2) / 11.0

            if x == 0 and y == 3:
                return math.log(max_current, 2) / 11.0

            if x == 3 and y == 3:
                return math.log(max_current, 2) / 11.0

        return -math.log(max_current, 2) / 11.0
