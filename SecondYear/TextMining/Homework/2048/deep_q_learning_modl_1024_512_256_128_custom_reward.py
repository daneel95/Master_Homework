from deep_q_learning_model_1024_512_256_128 import DeepQLearningModel_1024_512_256_128
import math
import numpy as np


class DeepQLearningModel_1024_512_256_128_custom_reward(DeepQLearningModel_1024_512_256_128):
    def __init__(self,
                 model_file_name='models/DeepQModel.chkpt',
                 replay_memory_file_name='models/replay_memory',
                 epsilon_file_name='models/epsilon.npy',
                 epsilon=0.05,
                 max_replay_memory=25000,
                 min_replay_memory=5000,
                 batch_size=512,
                 epsilon_steps=5000):
        super().__init__(model_file_name=model_file_name,
                         replay_memory_file_name=replay_memory_file_name,
                         epsilon=epsilon,
                         max_replay_memory=max_replay_memory,
                         epsilon_file_name=epsilon_file_name,
                         min_replay_memory=min_replay_memory,
                         batch_size=batch_size,
                         epsilon_steps=epsilon_steps)

    def get_reward(self, game):
        return math.log(np.max(game.get_board()), 2) + self.get_number_of_merges(game)

    def get_number_of_merges(self, game):
        return np.count_nonzero(game.get_board() == 0) \
               - np.count_nonzero(self.last_state.get_board() == 0)
