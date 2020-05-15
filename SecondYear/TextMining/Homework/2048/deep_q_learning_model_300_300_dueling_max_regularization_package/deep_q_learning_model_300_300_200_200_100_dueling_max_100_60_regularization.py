from base.deep_q_learning_model_base import DeepQLearningModelBase
import keras
from keras.layers import Dense, Lambda
from keras.models import Sequential
from keras.regularizers import l1
import keras.backend as K
from keras.models import Model


class DeepQLearningModel_300_300_200_200_100_dueling_max_100_60_regularization(DeepQLearningModelBase):
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
        self.regularization = 0.000001

    def init_model(self, state):
        q_state = state

        input_dimensions = len(q_state)
        output_dimensions = 4  # number of possible actions

        self.model = Sequential()
        self.model.add(Dense(300, input_dim=input_dimensions, activation='relu', kernel_regularizer=l1(self.regularization)))
        self.model.add(Dense(300, activation='relu', kernel_regularizer=l1(self.regularization)))
        self.model.add(Dense(200, activation='relu', kernel_regularizer=l1(self.regularization)))
        self.model.add(Dense(200, activation='relu', kernel_regularizer=l1(self.regularization)))
        self.model.add(Dense(100, activation='relu', kernel_regularizer=l1(self.regularization)))
        self.model.add(Dense(100, activation='relu', kernel_regularizer=l1(self.regularization)))
        self.model.add(Dense(output_dimensions))

        dqn = self.model.layers[-2]
        dqn = Dense(60, activation='relu', kernel_regularizer=l1(self.regularization))(dqn.output)
        y = Dense(output_dimensions + 1, activation="linear")(dqn)
        outputlayer = Lambda(lambda a: K.expand_dims(a[:, 0], -1) + a[:, 1:] - K.max(a[:, 1:], axis=1, keepdims=True),
                             output_shape=(output_dimensions,))(y)

        self.model = Model(inputs=self.model.input, outputs=outputlayer)

        optimizer = keras.optimizers.Adam()
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['acc'])

        # Load previous weights if they exist
        self.load_model()

    def update_q_value(self, old_q_value, a_reward, max_q_value):
        return old_q_value + self.learning_rate * (a_reward + self.discount * max_q_value - old_q_value)


