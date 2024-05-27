import numpy as np

class QLearningAgent:
    def __init__(self, env,alpha, gamma, epsilon ):
        self.env=env
        self.alpha=alpha
        self,gamma=gamma
        self.epsilon = epsilon
        self.q_table ={}