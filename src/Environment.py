import numpy as np
import random 



class Environment:
    def __init__(self, grid_size ):
        self.grid_size=grid_size
        self.grid=np.zeros(grid_size)
        self.pedestrians_positions = []
        self.Traffic_lights_states={}
        self.Traffic_lights_pos = []
        self.fuel_capacity=100
        self.dynamic_pedestrians()
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
                    self.grid[row,col]= state # this represents a Traffic light
                    self.Traffic_lights_pos.append((row, col))
                    self.traffic_lights_states[(row, col)] = {
                        'state' :state,
                        'timer': 10,
                        'red_duration':10,
                        'green_duration':20

                    } #this represents the information of the light at the current position on the grid
                    break   
    



    def update_traffic_lights(self):
       """ In this function, we want to update the states of the traffic lights, reflecting a real world environemnt
       the states of the lights will decrement based on a timer... if the timer goes below or equal to some value
       this will cause a switch of states. 
       """
       for pos in self.Traffic_lights_pos:
           # get the information of each traffic light on the grid and assign it to light_information
           light_information = self.Traffic_lights_states[pos]
           #decrement the timer by 1 for each time step, irrespective to the agents actions we decrement the timer
          
           light_information["timer"] -=1
           #if the timer is equal to 0 and its a Red traffic light, we can then switch the state
           if light_information["timer"]<=0:
              if light_information["state"]=="RED":
                  #if the timer reaches 0 and the state was previously Red, we will change it to green and switch states and re-do the timer
                  light_information["state"]="GREEN"
                  light_information["timer"]= light_information["green_duration"]

              else:
                  #if it was previously Green, change state to Red
                  light_information["state"]= "RED"
                  light_information["timer"] = light_information["red_duration"]

              #update the state/value of that position in the gird where the traffic light is placed
              self.grid[pos] = "GREEN" if light_information["state"]=="GREEN" else "RED"





    def dynamic_pedestrians(self):
        
          

         
    

                  

               
               
               
               

           


        


    

           
                

                


            
            




    

    
    


        



