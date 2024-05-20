import numpy as np
import random 



class Environment:
    def __init__(self, grid_size ):
        self.grid_size=grid_size
        self.grid=np.zeros(grid_size)
        self.pedestrians = []
        self.Traffic_lights_states={}
        self.Traffic_lights_pos = []
        self.fuel_capacity=100
        self.place_pedestrians()
        self.place_lights()
        


    def initialize_grid(self):
       # initialize the grid with empty cells using np
        grid = np.zeros(self.grid_size, self.grid_size)
        return grid
    

    def place_lights(self):
        # Allow for the random placing of traffic lights
        #define the number of traffic lights
        num_traffic_lights = 50
        for _ in range(num_traffic_lights): # iterating based on number of traffic lights
            while True:
                row = np.random.randint(self.grid_size)
                col = np.random.randint(self.grid_size)
                #lets check if its an empty cell
                # if the cell is empty we can assign a Traffic light... 0 = empty cell
                if self.grid[row, col]==0:
                    #randomly choose which state the traffic light will be in
                    state = random.choice(['RED', 'GREEN'])
                    self.grid[row,col]== state # this represents a Traffic light
                    self.Traffic_lights_pos.append(row, col)
                    self.traffic_lights_states[(row, col)] = {
                        'state' :state,
                        'timer': 10,
                        'red_duration':10,
                        'green_duration':10

                    } #this represents the information of the light at the current position on the grid
                    break
    

                    

    

           
                

                


            
            




    

    
    


        



