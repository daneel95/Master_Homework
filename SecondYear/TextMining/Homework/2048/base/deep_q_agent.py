import numpy as np


# The agent that uses DeepQLearning Model
class DeepQAgent:
    def __init__(self, model):
        self.model = model

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

    def final_state(self, game):
        self.model.observe(game)
