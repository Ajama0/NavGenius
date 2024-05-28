import numpy as np
import random
import time

class QLearningAgent:
    def __init__(self, env,alpha, gamma, epsilon ):
        self.env=env
        self.alpha=alpha
        self,gamma=gamma
        self.epsilon = epsilon
        self.q_table ={}


    def learning(self, episode, decay=0.99):
        #in each episode we want to reset the environment
        for episode in range(episode):
            #returns the initial local observation (6x6 matrix surrounding agent)
            state = self.env.reset() 
            done = False
            total_reward = 0

            #as long as the episode is executing
            while not done:
                action = self.choose_action(action)
                next_state, reward, done = self.env.movement(action)
                self.update_qv(state, action, reward, next_state)
                state = next_state
                total_reward += reward

            print(f"Episode {episode + 1}: Total Reward: {total_reward}")
            self.epsilon = max(self.epsilon * decay, 0.01)  # Decay epsilon but ensure it doesn't go below 0.01



    def choose_action(self, state):
        if np.random.uniform(0,1) < self.epsilon:
            #choose a random action(Exploration phase)   
            action = np.random.choice(self.env.valid_actions())

        else:
            #turn the state(matrix)into a string so it can be used as a Key in the q table dict
            state_key = self.get_state_key(state)
            if state_key not in self.q_table:
            # if the state is not in the q table, initialize all q-values for actions = 0
                self.q_table[state_key] = {action: 0 for action in self.env.ACTIONS }
            #choose action that maximises q value
            action = max(self.q_table[state_key], key = self.q_table[state_key].get)

        return action 


    def update_qv(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state_key)

            #If the current state is not in the Q-table, initialize its Q-values for all possible actions to 0
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0 for action in self.env.ACTIONS}
        
        # If the next state is not in the Q-table, initialize its Q-values for all possible actions to 0
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0 for action in self.env.ACTONS}

        
        old_value = self.q_table[state_key][action]
        #maximum q value for the next state considering all actions for that state
        next_max = max(self.q_table[next_state_key].values())

        #q learning formula
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state_key][action] = new_value  # Update the Q-value in the Q-table


    @staticmethod
    def get_state_key(state):
        #return the local observation as a string to define it as a key
        return str(state.flatten())
    
























