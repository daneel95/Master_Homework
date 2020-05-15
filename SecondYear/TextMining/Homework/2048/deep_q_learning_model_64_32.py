from deep_q_learning_model_base import DeepQLearningModelBase
import keras
from keras.layers import Dense
from keras.models import Sequential


class DeepQLearningModel6432(DeepQLearningModelBase):
    def __init__(self,
                 model_file_name='models/DeepQModel.chkpt',
                 replay_memory_file_name='models/replay_memory',
                 epsilon_file_name='models/epsilon.npy',
                 epsilon=0.05,
                 max_replay_memory=25000,
                 min_replay_memory=5000,
                 batch_size=512):
        super().__init__(model_file_name=model_file_name,
                         replay_memory_file_name=replay_memory_file_name,
                         epsilon_file_name=epsilon_file_name,
                         epsilon=epsilon,
                         max_replay_memory=max_replay_memory,
                         batch_size=batch_size,
                         min_replay_memory=min_replay_memory)

    def init_model(self, state):
        q_state = state

        input_dimensions = len(q_state)
        output_dimensions = 4  # number of possible actions
        self.model = Sequential()
        self.model.add(Dense(64, input_dim=input_dimensions, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(output_dimensions))
        optimizer = keras.optimizers.Adam()
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['acc'])

        # Load previous weights if they exist
        self.load_model()

    def update_q_value(self, old_q_value, a_reward, max_q_value):
        return a_reward + self.discount * max_q_value
