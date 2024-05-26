import numpy as np
import random 
import time

class Environment:
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
    
        self.place_lights()
    
        self.static_pedestrians()
        
        self.initial_vehicle_position()
        

       

    def initialize_grid(self):
         # initialize the grid 
       # Initialize the grid with roads ('-,|'), intersections ('+'), and side-walks ('0')
   
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i % 2 == 0 and j % 2 == 0:
                    self.grid[i, j] = '+'  # Intersection
                elif i % 2 == 0:
                    self.grid[i, j] = '-'  # Horizontal road
                elif j % 2 == 0:
                    self.grid[i, j] = '|'  # Vertical road
                else:
                    self.grid[i, j] = '0'  # Side-walk
       



    def place_lights(self):
        
        # Allow for the random placing of traffic lights
        #traffic lights can only be placed on intersections
        #define the number of traffic lights
        num_traffic_lights = 8
        for _ in range(num_traffic_lights):  # iterating based on number of traffic lights
            while True:
                row = np.random.randint(0, self.grid_size)
                col = np.random.randint(0, self.grid_size)
                #lets check if its an empty cell
                # if the cell is empty we can assign a Traffic light... on an intersection
                if self.grid[row, col] == '+':
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
                self.grid[pos] = "G" if light_information["state"] == "G" else "R"
        print("Traffic lights updated.")


    def static_pedestrians(self):
        #define the number of pedestrians
        num_of_pedestrians = 8
        for _ in range(num_of_pedestrians):
            while True:
                row = random.randint(0, self.grid_size)
                col = random.randint(0, self.grid_size)
                if self.grid[row, col] == '0':
                    self.grid[row, col] = 'P'
                    self.pedestrians_positions.append((row, col))
                    break
        

    def dynamic_pedestrians(self):
       # yet to do this implementation
       # some pedestrians will be walking around the grid
        return None    


    def initial_vehicle_position(self):
        # The vehicle is placed randomly on the grid
        # placed on a a horizontal or vertical road
        
        while True:
            row = random.randint(0, self.grid_size)
            col = random.randint(0, self.grid_size)
            if self.grid[row, col] in ['|', '-']:
                self.grid[row, col] = 'V'
                self.vehicle_position = (row, col)
                break
        print(f"Vehicle placed at position: {self.vehicle_position}")
        return self.local_observation()
    


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
         #initially fill local observation matrix with empty spaces '-'
        local_obs_matrix = np.full((observation_size, observation_size), '-', dtype=object)

        for i in range(observation_size):
            for j in range(observation_size):
                 # we want to get to the upper and lower limit of of the matrix surrounding the agent
                obs_row = row - half_obs + i
                obs_col = col - half_obs + j
                
                 #lets check if the matrix surrounding the vehicle is within our boundary
                if self.within_boundary(obs_row, obs_col):
                    #copy the values of the main grid at the positons into our local observation matrix
                    local_obs_matrix[i, j] = self.grid[obs_row, obs_col]

      
        return local_obs_matrix
    


    def valid_actions(self, state):
        #These are the valid actions the agent can take
        row, col = self.vehicle_position
        valid_actions = []
        
        

        #at any point if the cells the surrounding cells the agent are a road or a Green light, we can append to the valid actions
        if self.grid[row - 1, col] in ['-', '|', 'G']:
            valid_actions.append("up")

        if self.grid[row + 1, col]  in ['-', '|', 'G']:
            valid_actions.append("down") 

        if self.grid[row, col + 1]  in ['-', '|', 'G']:
            valid_actions.append("right") 

        if self.grid[row, col - 1]  in ['-', '|', 'G']:
            valid_actions.append("left")

        # we include a stop action, if any of the surrounding cells are a red light
        #then this way the agent can take the stop action, remaining in its current cell
        if self.grid[row - 1, col] == 'R' or self.grid[row + 1, col] == 'R' or \
           self.grid[row, col - 1] == 'R' or self.grid[row, col + 1] == 'R':    
            valid_actions.append("stop")



        return self.valid_actions



    def movement(self, action):
        row, col = self.vehicle_position
        new_row, new_col = row, col

        #updating the agents positions based on the action taken
        if action == 'up':
            new_row -=1

        elif action == 'down':
            new_row +=1

        elif action == 'left':
            new_col -=1

        elif action == 'right' :
            new_col += 1


        elif action == 'stop':
            






        
       
            




    


    




env = Environment(grid_size=10)

# Get the local observation matrix
local_obs = env.local_observation()

# Print the local observation matrix
print("Local Observation Matrix:")
for row in local_obs:
    print(' '.join(row))

# Print the grid for visualization
print("Global Grid:")
for row in env.grid:
    print(' '.join(row))