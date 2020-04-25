import random
import os
import numpy as np
import keras
import copy


class DeepQLearningModelBase:
    def __init__(self,
                 epsilon=0.05,
                 gamma=0.9,
                 learning_rate=0.01,
                 batch_size=512,
                 max_replay_memory=25000,
                 min_replay_memory=5000,
                 epsilon_steps=5000,
                 model_file_name='models/DeepQModel.chkpt',
                 replay_memory_file_name='models/replay_memory',
                 epsilon_file_name='models/epsilon.npy'):
        self.model = None
        self.model_file_name = model_file_name
        self.replay_memory_file_name = replay_memory_file_name
        self.epsilon_file_name = epsilon_file_name

        # Initialize replay memory
        self.replay_memory = []
        self.max_replay_memory = max_replay_memory
        self.min_replay_memory = min_replay_memory
        self.batch_size = batch_size

        # Epsilon initialization
        self.initial_epsilon = 1.0
        self.epsilon = self.initial_epsilon
        self.final_epsilon = epsilon
        self.epsilon_steps = epsilon_steps

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
        raise NotImplemented

    def get_action(self, game):
        legal_actions = game.get_available_moves()
        # state = game.get_state()
        r = random.random()
        # with a random chance that is decreasing over time, pick a random action
        if r < self.epsilon:
            print("Random Action!!")
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
            reward = self.get_reward(game)
            print("Reward = ", reward)
            self.update(self.last_state, self.last_action, game, reward)

        # save every 500 iterations
        if self.save != 0 and self.save % 100 == 0:
            self.save_model()
            self.save_replay_memory()
            self.save_epsilon()
            self.save = 0

    def get_reward(self, game):
        return game.get_score() - self.last_state.get_score()

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
            max_q_value = max(actions_next_q_values)  # max_q_value = max q value of the next state
            old_q_value = actions_q_values[a_action]  # old q value
            if is_final_state:
                # If final state => just set the reward
                updated_q_value = a_reward
            else:
                # If not final then update the q values
                # q_new = q_old + learning_rate * (reward + discount_factor * max_future_value - q_old)
                # old_q_value + self.learning_rate * (a_reward + self.discount * max_q_value - old_q_value)
                updated_q_value = self.update_q_value(old_q_value, a_reward, max_q_value)

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

    def update_q_value(self, old_q_value, a_reward, max_q_value):
        return old_q_value + self.learning_rate * (a_reward + self.discount * max_q_value - old_q_value)

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