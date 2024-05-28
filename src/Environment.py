import numpy as np
import random 


class Environment:


    ACTIONS = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
     

    def __init__(self, grid_size):
     
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=object)
        self.pedestrians_positions = []
        self.traffic_lights_states = {}
        self.traffic_lights_pos = []
        self.fuel_capacity = 100
        self.vehicle_position = None
        self.destination = None

        # Exececuted when an instance of the env class is created
        self.initialize_grid()
        self.place_destination()
        self.initial_vehicle_position()
        self.place_lights()
        self.static_pedestrians()
        
    
    def initialize_grid(self):
       # Initialize the grid with roads
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=object)


    def place_lights(self):
        
        # Allow for the random placing of traffic lights
        #traffic lights can only be placed on intersections
        #define the number of traffic lights
        num_traffic_lights = 5
        for _ in range(num_traffic_lights):  # iterating based on number of traffic lights
            while True:
                row = np.random.randint(0, self.grid_size-1)
                col = np.random.randint(0, self.grid_size-1)
                #lets check if its an empty cell
                # if the cell is empty we can assign a Traffic light... on an empty cell
                if self.grid[row, col] == 0:
                     #randomly choose which state the traffic light will be in R=red, G=green
                    state = random.choice(['R', 'G'])
                    self.grid[row, col] = state  # this represents a Traffic light
                    self.traffic_lights_pos.append((row, col))
                    self.traffic_lights_states[(row, col)] = {
                        'state': state,
                        'timer': 10,
                        'red_duration': 10,
                        'green_duration': 20
                    }
                    break
       


    def update_traffic_lights(self):
        print("Updating traffic lights...")
        """In this function, we want to update the states of the traffic lights, reflecting a real world environemnt
         the states of the lights will decrement based on a timer... if the timer goes below or equal to some value
        this will cause a switch of states. 
         """
        for pos in self.traffic_lights_pos: 
            # get the information of each traffic light on the grid and assign it to light_information
            light_information = self.traffic_lights_states[pos]
            #decrement the timer by 1 for each time step, irrespective to the agents actions we decrement the timer

            light_information["timer"] -= 1
            #if the timer is equal to 0 and its a Red traffic light, we can then switch the state
            if light_information["timer"] <= 0:
                if light_information["state"] == "R":
                    light_information["state"] = "G"
                    light_information["timer"] = light_information["green_duration"]
                else:
                    light_information["state"] = "R"
                    #if the timer reaches 0 and the state was previously Red, we will change it to green and switch states and reset the timer
                    light_information["timer"] = light_information["red_duration"]
                 #update the state/value of that position in the grid where the traffic light is placed
                self.grid[pos] = light_information["state"]
        print("Traffic lights updated.")


    def static_pedestrians(self):
        #define the number of pedestrians
        num_of_pedestrians = 4
        for _ in range(num_of_pedestrians):
            while True:
                row = random.randint(0, self.grid_size-1)
                col = random.randint(0, self.grid_size-1)
                if self.grid[row, col] == 0:
                    self.grid[row, col] = 'P'   #assign a pedestrian at this position
                    self.pedestrians_positions.append((row, col))
                    break
        

    def dynamic_pedestrians(self):
       # yet to do this implementation
       # some pedestrians will be walking around the grid
        return None    


    def initial_vehicle_position(self):
        # The vehicle is placed randomly on the grid
        # placed on a a horizontal or vertical road
        row = 0
        col = 0
        self.grid[row,col]= 'V'
        self.vehicle_position = (row,col)
        print(f"Vehicle placed at position: {self.vehicle_position}")
        return self.local_observation()
    

    def place_destination(self):
        dest_row, dest_col = self.grid_size - 1, self.grid_size - 1
        self.grid[dest_row, dest_col] = 'D'
        self.destination = (dest_row, dest_col)
        print(f"Destination placed at position: {self.destination}")


    def within_boundary(self, x, y):
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size


    def local_observation(self):
        """"within this function instead of having the agent compute q values for the entirety of the 
        200x200 grid after every state change. We will use a 6x6 matrix positioned around the point
        of the vehicle. This way we can reduce the learning time and allow the vehicle to know about
        its immediate environment instead of processing 40,000 cells as our state
        """
         # if the vehicle's position is yet to be defined
        if self.vehicle_position is None:
            return None
        
        #extract the position of the vehicle
        row, col = self.vehicle_position
        observation_size = 6  #size of our local observation Matrix 6x6
        half_obs = observation_size // 2
         #initially fill local observation matrix with empty spaces and ! for out of bounds
        local_obs_matrix = np.full((observation_size, observation_size), '!', dtype=object)

        for i in range(observation_size):
            for j in range(observation_size):
                 # we want to get to the upper and lower limit of of the matrix surrounding the agent
                obs_row = row - half_obs + i
                obs_col = col - half_obs + j
                
                 #lets check if the matrix surrounding the vehicle is within our boundary
                if self.within_boundary(obs_row, obs_col):
                    #copy the values of the main grid at the positons into our local observation matrix
                    local_obs_matrix[i, j] = str(self.grid[obs_row, obs_col])

      
        return local_obs_matrix
    


    def valid_actions(self):
        #These are the valid actions the agent can take, gives the option to the agent to make correct choice
        row, col = self.vehicle_position
        valid_actions = []

        #at any point if actions taken are within boundary, we can append to the valid actions
        for action, movement in self.ACTIONS.items():
            new_row, new_col = row + movement[0], col + movement[1]
            if self.within_boundary(new_row, new_col):
             valid_actions.append(action)

        return valid_actions
    

    
    
    
     


    def movement(self, action):
        if action not in self.ACTIONS:
            print("invalid action taken")
            return self.local_observation(), -10, False   #-10 for an invalid action
       

        row, col = self.vehicle_position
        move = self.ACTIONS[action]
        new_row, new_col = row + move[0], col + move[1]

        
        if self.within_boundary(new_row,new_col):
            if self.grid[new_row,new_col] =='P':
                print("collided with a pedestrian")
                #assign a large penalty for hitting a pedestrian
                reward = -100
                #end the episode when the agent collides with pedestrian
                done = True
            
            elif self.grid[new_row, new_col]  == 'R':
                print("Encountered a red light")
                reward = -10 #moderate penalty for running a red light
                done = False

            elif self.grid[new_row, new_col]=='D':
                print("episode compelte")
                reward = 100
                done = True

            #else if the new action is a valid move
            elif self.grid[new_row, new_col] in [0, 'G']:
                self.grid[row,col] = 0
                self.vehicle_position = (new_row, new_col)
                self.grid[new_row, new_col] = 'V'
                print(f"Vehicle moved to position: {self.vehicle_position}")
                reward = -1 #small negative penalty to reduce unneccessary exploring
                done = False

        else:
            #anything else such as out of boundary
            reward = -10
            done = False        

           

        next_state = self.local_observation
        return next_state, reward, done
       

    def is_done(self):
        return self.vehicle_position == self.destination  
     


    def reset(self):
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=object)
        self.pedestrians_positions = []
        self.traffic_lights_states = {}
        self.traffic_lights_pos = []
        self.fuel_capacity = 100
        self.vehicle_position = None
        self.destination = None

        self.initialize_grid()
        self.place_destination()
        self.initial_vehicle_position()
        self.place_lights()
        self.static_pedestrians()

        return self.local_observation() 
            


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