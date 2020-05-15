import numpy as np
import os
import math
import random
import copy
import keras
from keras.layers import Conv2D, Flatten, Dense
from keras.models import Sequential
from keras.optimizers import RMSprop


class ConvolutionModel:
    def __init__(self,
                 epsilon=0.1,
                 gamma=0.9,
                 batch_size=512,
                 max_replay_memory=5000,
                 epsilon_steps=500000,
                 model_file_name='models/DeepQModel.chkpt',
                 replay_memory_file_name='models/replay_memory',
                 epsilon_file_name='models/epsilon.npy'):
        self.model = None
        self.model_file_name = model_file_name
        self.replay_memory_file_name = replay_memory_file_name
        self.epsilon_file_name = epsilon_file_name

        self.gamma = gamma

        # Replay memory
        self.replay_memory = []
        self.max_replay_memory = max_replay_memory
        self.batch_size = batch_size

        # epsilon
        self.epsilon = 1.0  # current epsilon
        self.final_epsilon = epsilon
        self.epsilon_steps = epsilon_steps
        self.update_count = 0

        # Load replay memory if exists
        # self.load_replay_memory()
        # Load epsilon if saved previously
        self.load_epsilon()

    def init_model(self, state):
        input_dimensions = state.shape
        output_dimensions = 4

        self.model = Sequential()
        self.model.add(Conv2D(128, (3, 3), input_shape=input_dimensions, activation="relu"))
        self.model.add(Conv2D(64, (2, 2), activation="relu"))
        self.model.add(Flatten())
        self.model.add(Dense(256, activation="relu"))
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(64, activation="relu"))
        self.model.add(Dense(output_dimensions))

        learning_rate = 0.001
        optimizer = RMSprop(learning_rate=learning_rate)
        self.model.compile(optimizer=optimizer, loss="mse", metrics=['acc'])

        # Load previous weights if they exist
        self.load_model()

    def get_reward(self, game, next_game):
        reward = 0
        current_game_max = np.max(game.get_board())
        next_game_max = np.max(next_game.get_board())
        if current_game_max != next_game_max:
            reward += math.log(next_game_max, 2) * 0.1

        reward += self.get_number_of_merges(game, next_game)
        print("Reward:", reward)
        return reward

    def get_number_of_merges(self, current_game, next_game):
        return np.count_nonzero(next_game.get_board() == 0) \
               - np.count_nonzero(current_game.get_board() == 0)

    def get_action(self, game):
        random_number = random.uniform(0, 1)
        legal_actions = game.get_available_moves()
        labels = self.model.predict(np.array([game.get_state()]))[0]
        sorted_actions_by_q_value = np.flip(np.argsort(labels))
        final_action = None

        if random_number < self.epsilon:
            # pick a random legal action
            action = random.sample(legal_actions, 1)[0]
            next_game = copy.copy(game)
            next_game.do_game_round(action)
            reward = self.get_reward(game=game, next_game=next_game)
            labels[action] = reward
            next_state = next_game.get_state()
            predictions = self.model.predict(np.array([next_state]))[0]
            max_q_value = np.max(predictions)
            labels[action] = labels[action] + self.gamma * max_q_value

            final_action = action
        else:
            for action in sorted_actions_by_q_value:
                if action not in legal_actions:
                    labels[action] = 0.0
                    continue

                next_game = copy.copy(game)
                next_game.do_game_round(action)
                reward = self.get_reward(game=game, next_game=next_game)
                labels[action] = reward
                next_state = next_game.get_state()
                predictions = self.model.predict(np.array([next_state]))[0]
                max_q_value = np.max(predictions)
                labels[action] = labels[action] + self.gamma * max_q_value

                final_action = action
                break

        # update epsilon
        if self.epsilon > self.final_epsilon:
            self.update_count += 1
            print("Update Count = ", self.update_count)
            self.epsilon = max(self.final_epsilon, 1.0 - float(self.update_count) / float(self.epsilon_steps))
            print("New epsilon = ", self.epsilon)

        self.replay_memory.append((game.get_state(), labels))
        if len(self.replay_memory) >= self.max_replay_memory:
            print("Got to max replay memory!")
            # shuffle randomly
            np.random.shuffle(self.replay_memory)
            replay_memory_batch = self.get_replay_batch()
            data = [el[0] for el in replay_memory_batch]
            labels = [el[1] for el in replay_memory_batch]
            self.model.train_on_batch(x=np.array(data),
                                      y=np.array(labels))
            self.save_model()
            self.save_epsilon()
            self.replay_memory = []

        return final_action

    def get_replay_batch(self):
        return random.sample(self.replay_memory, self.batch_size)

    def load_replay_memory(self):
        if os.path.isfile(self.replay_memory_file_name + ".npy"):
            self.replay_memory = list(np.load(self.replay_memory_file_name + ".npy", allow_pickle=True))
            print("Replay memory loaded!")

    def save_replay_memory(self):
        np.save(self.replay_memory_file_name + ".npy", self.replay_memory)
        print("Replay memory saved!")

    def load_epsilon(self):
        epsilon_path = self.epsilon_file_name
        if os.path.isfile(epsilon_path):
            eps = np.load(epsilon_path)
            self.epsilon = eps[0]
            self.update_count = eps[1]
            print("Epsilon and episode count loaded!")

    def save_epsilon(self):
        np.save(self.epsilon_file_name, np.array([self.epsilon, self.update_count]))
        print("Epsilon and update count saved!")

    def save_model(self):
        self.model.save(self.model_file_name)
        print("Model saved!")

    def load_model(self):
        if os.path.isfile(self.model_file_name):
            self.model = keras.models.load_model(self.model_file_name)
            print("Model loaded!")
