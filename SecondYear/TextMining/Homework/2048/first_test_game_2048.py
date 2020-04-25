import random
import os
import keras
import copy
from keras.layers import Dense
from keras.models import Sequential

import numpy as np

from game_2048 import game_2048


class first_test_game_2048(game_2048):
    def get_state(self):
        state = self.board.flatten()
        powers_state = []
        for el in state:
            power = 0
            while el > 1:
                power += 1
                el /= 2
            powers_state.append(power)

        # set the state to be used in get_score
        self.state = powers_state
        return powers_state


class DeepQLearningModel:
    def __init__(self, epsilon=0.05, gamma=0.95, learning_rate=0.01, model_file_name='models/DeepQModel.chkpt', replay_memory_file_name='models/replay_memory'):
        self.model = None
        self.model_file_name = model_file_name
        self.replay_memory_file_name = replay_memory_file_name

        # Initialize replay memory
        self.replay_memory = []
        self.max_replay_memory = 50000
        self.min_replay_memory = 10000
        self.batch_size = 512

        # Epsilon initialization
        self.initial_epsilon = 1.0
        self.epsilon = self.initial_epsilon
        self.final_epsilon = epsilon
        self.epsilon_steps = 10000

        self.learning_rate = learning_rate
        self.gamma = gamma

        self.discount = self.gamma
        self.update_count = 0

        # Load replay memory if exists
        self.load_replay_memory()
        # Load epsilon if saved previously
        self.load_epsilon()

        self.last_state = None
        self.last_action = None
        self.save = 0

    # state = game instance !!!
    def init_model(self, state):
        q_state = state

        input_dimenstions = len(q_state)
        output_dimensions = 4  # number of possible actions
        hidden_layer_neurons = int(input_dimenstions / 2)
        self.model = Sequential()
        self.model.add(Dense(output_dim=hidden_layer_neurons, input_dim=input_dimenstions,
                             activation='tanh', init='uniform'))
        self.model.add(Dense(output_dimensions, activation='linear', init='uniform'))
        optimizer = keras.optimizers.SGD()
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['accuracy'])

        # Load previous weights if they exist
        self.load_model()

    def get_action(self, game):
        legal_actions = game.get_available_moves()
        # state = game.get_state()
        r = random.random()
        # with a random chance that is decreasing over time, pick a random action
        if r < self.epsilon:
            action = random.choice(legal_actions)
            self.last_state = copy.copy(game)
            self.last_action = action

            return action

        q_state = game.get_state()
        # here are the 4 q values for the given state (for all 4 actions)
        predictions = self.model.predict(np.array([q_state]))[0]
        q_values = list(enumerate(predictions))
        q_values = sorted(q_values, key=lambda x: x[1], reverse=True)

        # Can be done like this because actions can be 0, 1, 2, 3 which comes from enumerate
        for action, q_value in q_values:
            # get only legal actions
            if action in legal_actions:
                self.last_state = copy.copy(game)
                self.last_action = action

                return action

    def observe(self, game):
        if self.last_state is not None:
            reward = game.get_score() - self.last_state.get_score()
            print("Reward = ", reward)
            self.update(self.last_state, self.last_action, game, reward)

        # save every 500 iterations
        if self.save != 0 and self.save % 500 == 0:
            self.save_model()
            self.save_replay_memory()
            self.save_epsilon()
            self.save = 0

    def update(self, game, action, next_game, reward):
        if self.model is None:
            self.init_model(game.get_state())

        self.remember(game, action, reward, next_game)

        if len(self.replay_memory) < self.min_replay_memory:
            print('Not enough memory to go further: ', len(self.replay_memory), ' < ', self.min_replay_memory)
            return

        # print("Taking batch from replay memory! Replay memory size: ", len(self.replay_memory))
        if len(self.replay_memory) >= self.max_replay_memory:
            print("Got to max replay memory!")
        else:
            print("Taking batch from replay memory! Replay memory size: ", len(self.replay_memory))

        batch = self.get_replay_batch()

        training_batch_q_states = []
        training_batch_target_q_values = []

        # q_state = old q state, a_action = old action, a_reward = old reward
        for q_state, a_action, a_reward, next_q_state, is_final_state in batch:
            actions_q_values = self.model.predict(np.array([q_state]))[0]
            actions_next_q_values = self.model.predict(np.array([next_q_state]))[0]
            max_q_value = max(actions_next_q_values)
            old_q_value = actions_q_values[a_action]  # old q value
            if is_final_state:
                # If final state => just set the reward
                updated_q_value = a_reward
            else:
                # If not final then update the q values
                # q_new = q_old + learning_rate * (reward + discount_factor * max_future_value - q_old)
                updated_q_value = old_q_value + self.learning_rate * (a_reward + self.discount * max_q_value - old_q_value)

            target_q_values = actions_q_values.copy()
            target_q_values[a_action] = updated_q_value

            # Add updated values for training
            training_batch_q_states.append(q_state)
            training_batch_target_q_values.append(target_q_values)

        # print("Training on batch!")
        self.model.train_on_batch(x=np.array(training_batch_q_states),
                                  y=np.array(training_batch_target_q_values))

        self.save += 1
        if self.epsilon > self.final_epsilon:
            self.update_count += 1
            print("Update Count = ", self.update_count)
            self.epsilon = max(self.final_epsilon, 1.0 - float(self.update_count) / float(self.epsilon_steps))
            print("New epsilon = ", self.epsilon)

    def remember(self, game, action, reward, next_game):
        if len(self.replay_memory) > self.max_replay_memory:
            # Too many elements in replay memory. Starting to delete old elements
            self.replay_memory.pop(0)

        q_state = game.get_state()
        next_q_state = next_game.get_state()

        is_final_state = game.is_game_over()

        self.replay_memory.append((q_state, action, reward, next_q_state, is_final_state))

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
        epsilon_path = 'models/epsilon.npy'
        if os.path.isfile(epsilon_path):
            eps = np.load(epsilon_path)
            self.epsilon = eps[0]
            self.update_count = eps[1]
            print("Epsilon and episode count loaded!")

    def save_epsilon(self):
        np.save('models/epsilon.npy', np.array([self.epsilon, self.update_count]))
        print("Epsilon and update count saved!")

    def save_model(self):
        self.model.save(self.model_file_name)
        print("Model saved!")

    def load_model(self):
        if os.path.isfile(self.model_file_name):
            self.model = keras.models.load_model(self.model_file_name)
            print("Model loaded!")


# The agent that uses DeepQLearning Model
class DeepQAgent:
    def __init__(self):
        self.model = DeepQLearningModel()

    def set_params(self, is_training=True, episode=0):
        self.is_training = is_training
        self.model.last_action = None
        self.model.last_state = None
        self.episode = episode

    def get_action(self, game):
        state = game.get_state()
        if self.model.model is None:
            self.model.init_model(state)

        if self.is_training:
            print("On episode: ", self.episode + 1)
            self.model.observe(game)
            return self.model.get_action(game)

        legal_actions = game.get_available_moves()
        q_state = state
        predictions = self.model.model.predict(np.array([q_state]))[0]
        q_values = list(enumerate(predictions))
        q_values = sorted(q_values, key=lambda x: x[1], reverse=True)
        for action, q_value in q_values:
            if action in legal_actions:
                return action

        return None

    def final(self, game):
        if self.is_training:
            print("Final")
            self.model.observe(game.get_state())


class DeepQLearningModel2:
    def __init__(self, epsilon=0.05, gamma=0.95, learning_rate=0.01, model_file_name='models/DeepQModel.chkpt', replay_memory_file_name='models/replay_memory'):
        self.model = None
        self.model_file_name = model_file_name
        self.replay_memory_file_name = replay_memory_file_name

        # Initialize replay memory
        self.replay_memory = []
        self.max_replay_memory = 10000
        self.min_replay_memory = 2000
        self.batch_size = 512

        # Epsilon initialization
        self.initial_epsilon = 1.0
        self.epsilon = self.initial_epsilon
        self.final_epsilon = epsilon
        self.epsilon_steps = 5000

        self.learning_rate = learning_rate
        self.gamma = gamma

        self.discount = self.gamma
        self.update_count = 0

        # Load replay memory if exists
        self.load_replay_memory()
        # Load epsilon if saved previously
        self.load_epsilon()

        self.last_state = None
        self.last_action = None
        self.save = 0

    # state = game instance !!!
    def init_model(self, state):
        q_state = state

        input_dimenstions = len(q_state)
        output_dimensions = 4  # number of possible actions
        hidden_layer_neurons = int(input_dimenstions / 2)
        self.model = Sequential()
        self.model.add(Dense(64, input_dim=input_dimenstions, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(output_dimensions, activation='linear',))
        optimizer = keras.optimizers.Adam(lr=0.001)
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['acc'])

        # Load previous weights if they exist
        self.load_model()

    def get_action(self, game):
        legal_actions = game.get_available_moves()
        # state = game.get_state()
        r = random.random()
        # with a random chance that is decreasing over time, pick a random action
        if r < self.epsilon:
            action = random.choice(legal_actions)
            self.last_state = copy.copy(game)
            self.last_action = action

            return action

        q_state = game.get_state()
        # here are the 4 q values for the given state (for all 4 actions)
        predictions = self.model.predict(np.array([q_state]))[0]
        q_values = list(enumerate(predictions))
        q_values = sorted(q_values, key=lambda x: x[1], reverse=True)

        # Can be done like this because actions can be 0, 1, 2, 3 which comes from enumerate
        for action, q_value in q_values:
            # get only legal actions
            if action in legal_actions:
                self.last_state = copy.copy(game)
                self.last_action = action

                return action

    def observe(self, game):
        if self.last_state is not None:
            reward = game.get_score() - self.last_state.get_score()
            print("Reward = ", reward)
            self.update(self.last_state, self.last_action, game, reward)

        # save every 500 iterations
        if self.save != 0 and self.save % 500 == 0:
            self.save_model()
            self.save_replay_memory()
            self.save_epsilon()
            self.save = 0

    def update(self, game, action, next_game, reward):
        if self.model is None:
            self.init_model(game.get_state())

        self.remember(game, action, reward, next_game)

        if len(self.replay_memory) < self.min_replay_memory:
            print('Not enough memory to go further: ', len(self.replay_memory), ' < ', self.min_replay_memory)
            return

        # print("Taking batch from replay memory! Replay memory size: ", len(self.replay_memory))
        if len(self.replay_memory) >= self.max_replay_memory:
            print("Got to max replay memory!")
        else:
            print("Taking batch from replay memory! Replay memory size: ", len(self.replay_memory))

        batch = self.get_replay_batch()

        training_batch_q_states = []
        training_batch_target_q_values = []

        # q_state = old q state, a_action = old action, a_reward = old reward
        for q_state, a_action, a_reward, next_q_state, is_final_state in batch:
            actions_q_values = self.model.predict(np.array([q_state]))[0]
            actions_next_q_values = self.model.predict(np.array([next_q_state]))[0]
            max_q_value = max(actions_next_q_values)
            old_q_value = actions_q_values[a_action]  # old q value
            if is_final_state:
                # If final state => just set the reward
                updated_q_value = a_reward
            else:
                # If not final then update the q values
                # q_new = q_old + learning_rate * (reward + discount_factor * max_future_value - q_old)
                updated_q_value = a_reward + self.discount * max_q_value

            target_q_values = actions_q_values.copy()
            target_q_values[a_action] = updated_q_value

            # Add updated values for training
            training_batch_q_states.append(q_state)
            training_batch_target_q_values.append(target_q_values)

        # print("Training on batch!")
        self.model.fit(np.array(training_batch_q_states),
                       np.array(training_batch_target_q_values),
                       epochs=1,
                       verbose=0)
        # self.model.train_on_batch(x=np.array(training_batch_q_states),
        #                           y=np.array(training_batch_target_q_values))

        self.save += 1
        if self.epsilon > self.final_epsilon:
            self.update_count += 1
            print("Update Count = ", self.update_count)
            self.epsilon = max(self.final_epsilon, 1.0 - float(self.update_count) / float(self.epsilon_steps))
            print("New epsilon = ", self.epsilon)

    def remember(self, game, action, reward, next_game):
        if len(self.replay_memory) > self.max_replay_memory:
            # Too many elements in replay memory. Starting to delete old elements
            self.replay_memory.pop(0)

        q_state = game.get_state()
        next_q_state = next_game.get_state()

        is_final_state = game.is_game_over()

        self.replay_memory.append((q_state, action, reward, next_q_state, is_final_state))

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
        epsilon_path = 'models/epsilon.npy'
        if os.path.isfile(epsilon_path):
            eps = np.load(epsilon_path)
            self.epsilon = eps[0]
            self.update_count = eps[1]
            print("Epsilon and episode count loaded!")

    def save_epsilon(self):
        np.save('models/epsilon.npy', np.array([self.epsilon, self.update_count]))
        print("Epsilon and update count saved!")

    def save_model(self):
        self.model.save(self.model_file_name)
        print("Model saved!")

    def load_model(self):
        if os.path.isfile(self.model_file_name):
            self.model = keras.models.load_model(self.model_file_name)
            print("Model loaded!")


# The agent that uses DeepQLearning Model
class DeepQAgent2:
    def __init__(self):
        self.model = DeepQLearningModel2()

    def set_params(self, is_training=True, episode=0):
        self.is_training = is_training
        self.model.last_action = None
        self.model.last_state = None
        self.episode = episode

    def get_action(self, game):
        state = game.get_state()
        if self.model.model is None:
            self.model.init_model(state)

        if self.is_training:
            print("On episode: ", self.episode + 1)
            self.model.observe(game)
            return self.model.get_action(game)

        legal_actions = game.get_available_moves()
        q_state = state
        predictions = self.model.model.predict(np.array([q_state]))[0]
        q_values = list(enumerate(predictions))
        q_values = sorted(q_values, key=lambda x: x[1], reverse=True)
        for action, q_value in q_values:
            if action in legal_actions:
                return action

        return None

    def final(self, game):
        if self.is_training:
            print("Final")
            self.model.observe(game.get_state())


NUM_GAMES = 10000
NUM_TRAINING = 10000

if __name__ == "__main__":
    # highest_score = 0
    # highest_score_value = 2
    # game_scores = []
    # game_end_boards = []
    # highest_score_best = []
    # highest_score_every_game = []
    #
    # bot = DeepQAgent()
    # for i in range(NUM_GAMES):
    #     print("Game ", i + 1, "/", NUM_GAMES)
    #     bot.set_params(is_training=i < NUM_TRAINING, episode=i)
    #     game = first_test_game_2048()
    #     if i % 5 == 0:
    #         print(game.get_board().__str__())
    #     while not game.is_game_over():
    #         action = bot.get_action(game)
    #         game.do_game_round(action)
    #         if i % 5 == 0:
    #             print("Action = ", action)
    #             print(game.get_board().__str__())
    #
    #     # bot.final(game)
    #     game_scores.append(game.get_score())
    #     game_end_boards.append(game.get_board())
    #     # just some statistics
    #     if game.get_score() > highest_score:
    #         highest_score = game.get_score()
    #     highest = game.get_highest_value()
    #     if highest > highest_score_value:
    #         highest_score_value = highest
    #
    #     print("Final Board!")
    #     print(game.get_board())
    #     print("Highest score until now: ", highest_score)
    #     print("Highest value until now: ", highest_score_value)
    #     # save statistics
    #     highest_score_best.append((highest_score, highest_score_value))
    #     highest_score_every_game.append((game.get_score(), highest))
    #     # Write statistics to file!
    #     # f.write(str(highest_score) + " - " + str(highest_score_value) + "\n")
    #     # g.write(str(game.get_score()) + " - " + str(highest) + "\n")
    #     if i % 10 == 0 and i != 0:
    #         f = open("models/statistics_score_best.txt", "w")
    #         g = open("models/statistics_every_game.txt", "w")
    #         for el in highest_score_best:
    #             f.write(str(el[0]) + " - " + str(el[1]) + "\n")
    #         for el in highest_score_every_game:
    #             g.write(str(el[0]) + " - " + str(el[1]) + "\n")
    #         f.close()
    #         g.close()
    #     print("=======================================")
    #
    # print(game_scores)
    # print(game_end_boards)
    # print("The end!")


    highest_score = 0
    highest_score_value = 2
    game_scores = []
    game_end_boards = []
    highest_score_best = []
    highest_score_every_game = []

    bot = DeepQAgent2()
    for i in range(NUM_GAMES):
        print("Game ", i + 1, "/", NUM_GAMES)
        bot.set_params(is_training=i < NUM_TRAINING, episode=i)
        game = first_test_game_2048()
        if i % 5 == 0:
            print(game.get_board().__str__())
        while not game.is_game_over():
            action = bot.get_action(game)
            game.do_game_round(action)
            if i % 5 == 0:
                print("Action = ", action)
                print(game.get_board().__str__())

        # bot.final(game)
        game_scores.append(game.get_score())
        game_end_boards.append(game.get_board())
        # just some statistics
        if game.get_score() > highest_score:
            highest_score = game.get_score()
        highest = game.get_highest_value()
        if highest > highest_score_value:
            highest_score_value = highest

        print("Final Board!")
        print(game.get_board())
        print("Highest score until now: ", highest_score)
        print("Highest value until now: ", highest_score_value)
        # save statistics
        highest_score_best.append((highest_score, highest_score_value))
        highest_score_every_game.append((game.get_score(), highest))
        # Write statistics to file!
        # f.write(str(highest_score) + " - " + str(highest_score_value) + "\n")
        # g.write(str(game.get_score()) + " - " + str(highest) + "\n")
        if i % 10 == 0 and i != 0:
            f = open("models/statistics_score_best.txt", "w")
            g = open("models/statistics_every_game.txt", "w")
            for el in highest_score_best:
                f.write(str(el[0]) + " - " + str(el[1]) + "\n")
            for el in highest_score_every_game:
                g.write(str(el[0]) + " - " + str(el[1]) + "\n")
            f.close()
            g.close()
        print("=======================================")

    print(game_scores)
    print(game_end_boards)
    print("The end!")


    # play normally
    # print("Playing normally!")
    # bot = DeepQAgent()
    # for i in range(NUM_GAMES):
    #     print("Game ", i + 1, "/", NUM_GAMES)
    #     bot.set_params(is_training=False, episode=i)
    #     game = first_test_game_2048()
    #     print(game.get_board().__str__())
    #     while not game.is_game_over():
    #         action = bot.get_action(game)
    #         game.do_game_round(action)
    #         print(game.get_board().__str__())
    #     print(game.get_score())
    #     print(game.get_highest_value())
    #     print("========================")
    #     import time
    #     time.sleep(2)
    #
    # print(game_scores)
    # print(game_end_boards)
    # print("The end!")
