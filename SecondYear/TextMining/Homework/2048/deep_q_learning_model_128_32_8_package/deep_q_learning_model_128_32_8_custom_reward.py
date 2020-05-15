from deep_q_learning_model_128_32_8_package.deep_q_learning_model_128_32_8 import DeepQLearningModel_128_32_8
import numpy as np


class DeepQLearningModel_128_32_8_custom_reward(DeepQLearningModel_128_32_8):
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
        current_board = game.get_board().copy()
        reward_between_states = game.get_score() - self.last_state.get_score()
        corner_max = self.get_corner_max_value(current_board)
        global_max = current_board.max()
        sorted_flatten_board = np.sort(current_board.reshape(-1))
        second_global_max = sorted_flatten_board[sorted_flatten_board.size - 2]
        distance = self.calculate_distance(current_board, global_max, second_global_max)

        return self.corner_vs_global_max_reward(corner_max, global_max) + \
               self.first_and_second_max_with_distance(global_max, second_global_max, distance) + \
               self.number_of_zeros_with_maxes(current_board, corner_max, global_max) + \
               self.reward_using_reward_between_states(reward_between_states, corner_max, global_max)

    def reward_using_reward_between_states(self, reward_between_states, corner_max, global_max):
        return reward_between_states * (corner_max - global_max / 4) / (global_max * global_max) * 4 / 3

    def number_of_zeros_with_maxes(self, current_board, corner_max, global_max):
        return np.count_nonzero(current_board == 0) * (corner_max - global_max / 3) / 4096

    def first_and_second_max_with_distance(self, global_max, second_global_max, distance):
        return np.log(1.5 * second_global_max + 1) * second_global_max / global_max * (-1 * (distance - 1))

    def corner_vs_global_max_reward(self, corner_max, global_max):
        return (corner_max - global_max / 2) / (global_max + 1)

    def calculate_distance(self, current_board, global_max, second_global_max):
        global_max_coordinates = np.where(current_board == global_max)
        if global_max == second_global_max:
            first_value = (global_max_coordinates[0][0] - global_max_coordinates[0][-1])**2
            second_value = (global_max_coordinates[1][0] - global_max_coordinates[1][-1])**2
            return np.sqrt(first_value + second_value)

        second_global_max_coordinates = np.where(current_board == second_global_max)
        distance = 8  # max distance
        for i in range(len(second_global_max_coordinates[0])):
            first_value = (global_max_coordinates[0][0] - second_global_max_coordinates[0][i])**2
            second_value = (global_max_coordinates[1][0] - second_global_max_coordinates[1][i])**2
            dist = np.sqrt(first_value + second_value)
            if dist < distance:
                distance = dist

        return distance

    def get_corner_max_value(self, current_board):
        corner_max = 0
        for i in [0, 3]:
            for j in [0, 3]:
                if current_board[i][j] > corner_max:
                    corner_max = current_board[i][j]

        return corner_max
