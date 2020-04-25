from deep_q_learning_model_300_300_200_200_100 import DeepQLearningModel_300_300_200_200_100
import numpy as np


class DeepQLearningModel_300_300_200_200_100_custom_reward(DeepQLearningModel_300_300_200_200_100):
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
        if 2048 in game.get_board():
            return 1.0

        return (self.get_number_of_tiles_merged(game) - 1) / 8.0  # 8 is maximum number of merges possible

    def get_number_of_tiles_merged(self, game):
        return np.count_nonzero(game.get_board() == 0) \
               - np.count_nonzero(self.last_state.get_board() == 0) + 1
