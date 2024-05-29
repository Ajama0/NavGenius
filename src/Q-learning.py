class QLearningAgent:
    def __init__(self, env, alpha, gamma, epsilon):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def learning(self, episodes, epsilon_decay_rate):
        performance_metrics = {
            'episode': [],
            'total_reward': [],
            'steps': [],
            'collisions': [],
            'infractions': [],
            'success': []
        }
         #in each episode we want to reset the environment
        for episode in range(episodes):
            state = self.env.reset()
            done = False
            total_reward = 0
            step_count = 0
            collisions = 0
            infractions = 0
            success = 0

             #as long as the episode is executing
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.movement(action)
                
                if reward == -50:
                    collisions += 1
                if reward == -5:
                    infractions += 1
                if reward == 2000:
                    success = 1

                self.update_qv(state, action, reward, next_state)
                state = next_state
                total_reward += reward
                step_count += 1

                if step_count >= 1000:
                    print("Episode step count exceeded")
                    break

            print(f"Episode {episode + 1}: Total Reward: {total_reward}, Steps: {step_count}, Collisions: {collisions}, Infractions: {infractions}, Success: {success}")
            print("-------------------------------------------------------------------------------------------------------------------------")

            performance_metrics['episode'].append(episode + 1)
            performance_metrics['total_reward'].append(total_reward)
            performance_metrics['steps'].append(step_count)
            performance_metrics['collisions'].append(collisions)
            performance_metrics['infractions'].append(infractions)
            performance_metrics['success'].append(success)

            self.epsilon = max(self.epsilon * epsilon_decay_rate, 0.1)

        return performance_metrics

    def choose_action(self, state):
      #choose a random action(Exploration phase)
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.env.valid_actions())
        else:
           #turn the state(matrix)into a string so it can be used as a Key in the q table dict
            state_key = self.get_state_key(state)
            if state_key not in self.q_table:
              # if the state is not in the q table, initialize all q-values for actions = 0
                self.q_table[state_key] = {action: 0 for action in self.env.ACTIONS}
            #choose action that maximises q value
            action = max(self.q_table[state_key], key=self.q_table[state_key].get)
        return action


    def update_qv(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0 for action in self.env.ACTIONS}
             # If the next state is not in the Q-table, initialize its Q-values for all possible actions to 0
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0 for action in self.env.ACTIONS}

        old_value = self.q_table[state_key][action]
        #maximum q value for the next state considering all actions for that state
        next_max = max(self.q_table[next_state_key].values())

         #q learning formula
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state_key][action] = new_value

    @staticmethod
    def get_state_key(state):
       #return the local observation as a string to define it as a key
        return str(state.flatten())
    
    

env = Environment(grid_size=10)
# Get the local observation matrix
local_obs = env.local_observation()

# Print the local observation matrix
print("Local Observation Matrix:")
for row in local_obs:
    print(' '.join(row))

# Print the global grid
print("Global Grid:")
for row in env.grid:
    print(' '.join(map(str, row)))

agent = QLearningAgent(env, alpha=0.1, gamma=0.9, epsilon=1.0)

# Train the agent and collect performance metrics
performance_metrics = agent.learning(episodes=1000, epsilon_decay_rate=0.99)


print(performance_metrics)