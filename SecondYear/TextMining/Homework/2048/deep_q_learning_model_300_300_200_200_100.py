from deep_q_learning_model_base import DeepQLearningModelBase
import keras
from keras.layers import Dense
from keras.models import Sequential


class DeepQLearningModel_300_300_200_200_100(DeepQLearningModelBase):
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
                         epsilon_file_name=epsilon_file_name,
                         epsilon=epsilon,
                         max_replay_memory=max_replay_memory,
                         batch_size=batch_size,
                         min_replay_memory=min_replay_memory,
                         epsilon_steps=epsilon_steps,
                         gamma=gamma,
                         learning_rate=learning_rate)

    def init_model(self, state):
        q_state = state

        input_dimensions = len(q_state)
        output_dimensions = 4  # number of possible actions
        self.model = Sequential()
        self.model.add(Dense(300, input_dim=input_dimensions, activation='relu'))
        self.model.add(Dense(300, activation='relu'))
        self.model.add(Dense(200, activation='relu'))
        self.model.add(Dense(200, activation='relu'))
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dense(output_dimensions))
        optimizer = keras.optimizers.Adam()
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['acc'])

        # Load previous weights if they exist
        self.load_model()

    def update_q_value(self, old_q_value, a_reward, max_q_value):
        return old_q_value + self.learning_rate * (a_reward + self.discount * max_q_value - old_q_value)


