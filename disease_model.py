from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import batch_run


from itertools import cycle
import random
import math
import scipy.stats as ss

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


stages = ['S','E','I','R']
# stages_with_death = ['S','E','I','R', 'S_delta_1', 'S_delta_2', 'S_delta_3', 'S_delta_4']


def infection_rates(model):

    agent_state = [agent.state for agent in model.schedule.agents]

    N = model.num_agents
    stages_dict = dict.fromkeys(stages, 0)


    for agents in agent_state:
        stages_dict[str(stages[agents])] += 1

    return stages_dict


def susceptible(self):
    agents = self.schedule.agents
    stages_dict = infection_rates(self)
    the_S = stages_dict['S']
    return the_S

def exposed(self):
    agents = self.schedule.agents
    stages_dict = infection_rates(self)
    the_E = stages_dict['E']
    return the_E

def infected(self):
    agents = self.schedule.agents
    stages_dict = infection_rates(self)
    the_I = stages_dict['I']
    return the_I

def recovered(self):
    agents = self.schedule.agents
    stages_dict = infection_rates(self)
    the_R = stages_dict['R']
    return the_R


class DiseaseAgent(Agent):
    def __init__(self, unique_id, model):

        super().__init__(unique_id, model)
        self.unique_id = unique_id
        
        global iterations
        iterations = 1
        self.model = model
        #self.iterations = iterations
        global the_time
        the_time = 1
        self.time = the_time
        
        self.interact_with_S = []
        self.interact_with_E = []
        self.interact_with_I = []
        self.interact_with_R = []


        s_initial = mu_s
        #s_initial = 5

        e_initial = mu_e
        #e_initial = 2

        #i_initial = 3
        i_initial = mu_i

        r_initial = int(N - e_initial - i_initial - s_initial)

        self.state = random.randint(0,2)

        stages_dict = infection_rates(model)

        if stages_dict['S'] > s_initial - 1 and self.state == 0:
            self.state = 2

            if stages_dict['I'] > i_initial - 1 and self.state == 2:
                self.state = 1

        elif stages_dict['E'] > e_initial - 1 and self.state == 1:
            self.state = 0
            if stages_dict['S'] > s_initial - 1 and self.state == 0:
                self.state = 2
        elif stages_dict['I'] > i_initial - 1 and self.state == 2:
            self.state = 0


            if stages_dict['S'] > s_initial - 1:
                self.state = 1


        else:
            self.state = self.state



    def step(self):

        #print('def step(self) of class DiseaseAgent(Agent) ')

        self.move()

        if self.state < 4:
            self.spread_disease()

        global iterations
        if (iterations % N) == 0:
            global the_time
            the_time += 1

        iterations += 1

    def spread_disease(self):

        
        for interaction in range(len(self.interact_with_S)):
            self.interact_with_S[interaction] += 1
        
        for interaction in range(len(self.interact_with_E)):
            self.interact_with_E[interaction] += 1

        for interaction in range(len(self.interact_with_I)):
            self.interact_with_I[interaction] += 1

        for interaction in range(len(self.interact_with_R)):
            self.interact_with_R[interaction] += 1

            
        #days: I : days 
        #E's: days: (5 - 10) : to S
        # no probability
        # just probability : S becomes E
        # probability: E becomes I (after days, no need interaction)
        
        
        for agent in self.model.schedule.agents:
            the_distance = math.sqrt((self.pos[0]-agent.pos[0])**2+(self.pos[1]-agent.pos[1])**2)
            
            if float(the_distance) <= 5:
                if self.state == 0 and agent.state == 1:
                    self.interact_with_E.append(1)
                    
                    for interaction in range(len(self.interact_with_E)):

                        if self.interact_with_E[interaction] == epsilon_se and self.unique_id < beta_se:
                            self.state = 1
                            self.interact_with_E = []
                            break
                
                elif self.state == 0 and agent.state == 2:
                    self.interact_with_I.append(1)
                    
                    for interaction in range(len(self.interact_with_I)):
                        if self.interact_with_I[interaction] == epsilon_se and self.unique_id < beta_se:
                            self.state = 1
                            self.interact_with_I = []
                            break
                        if self.interact_with_I[interaction] == epsilon_si and self.unique_id < beta_si:
                            self.state = 2
                            self.interact_with_I = []
                            break
                            
                elif self.state == 1:
#                   
                    self.interact_with_S.append(1)
                    
                    for interaction in range(len(self.interact_with_S)):
                        if self.interact_with_S[interaction] == epsilon_es and self.unique_id < beta_es: 
                            self.state = 0
                            self.interact_with_S = []
                            break
                    
                           
                        if self.interact_with_S[interaction] == epsilon_ei:
                            if self.unique_id < beta_ei:
                                self.state = 2
                                self.interact_with_s = []
                          
                            break
                    
                elif self.state == 2:
                    
                    self.interact_with_R.append(1)
                    
                    for interaction in range(len(self.interact_with_R)):
                        
                        if self.interact_with_R[interaction] == epsilon_ir and self.unique_id < beta_ir:
                            self.state = 3
                            self.interact_with_R = []
                            break
                else:
                    self.state = self.state

        return





    def move(self):
   #     print('def move(self) of class DiseaseAgent(Agent) ')
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
    #    print(possible_steps[0])
        # new_position = possible_steps[0]

        new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)


class DiseaseModel(Model):
    def __init__(self, n, the_width, the_height, x, y, mu_1, mu_2, mu_3, delta_1, delta_2, delta_3, delta_4, beta_12, beta_13, beta_21, beta_23, beta_34, epsilon_12, epsilon_13, epsilon_21, epsilon_23, epsilon_34, theta_12, theta_13, theta_21, theta_23, theta_34, sigma_12, sigma_13, sigma_21, sigma_23, sigma_34):
        # print('class DiseaseModel(Model) ')
        self.num_agents = n
        global N
        N = n
        
        global mu_e
        mu_e = mu_2
        # mu_e = math.floor(N * mu_2)
        
        
        global mu_i
        mu_i = mu_3
        # mu_i = math.floor(N * mu_3)
        
        
        global mu_s
        mu_s = mu_1
        # mu_s = N - mu_e - mu_i
        
        
        global delta_s
        delta_s = delta_1

        global delta_e
        delta_e = delta_2

        global delta_i
        delta_i = delta_3

        global delta_r
        delta_r = delta_4
        
        global beta_se
        beta_se = beta_12
        # beta_se = math.ceil(N * beta_12)
        
        
        global beta_si
        beta_si = beta_13
        #beta_si = math.ceil(N * beta_13)
        
        
        global beta_es
        beta_es = beta_21
        #beta_es = math.ceil(N * beta_21)
        
        
        global beta_ei
        beta_ei = beta_23
        #beta_ei = math.ceil(N * beta_23)
        
        
        global beta_ir
        beta_ir = beta_34
        #beta_ir = math.ceil(N * beta_34)
        
        
        global epsilon_se
        epsilon_se = epsilon_12

        global epsilon_si
        epsilon_si = epsilon_13

        global epsilon_es
        epsilon_es = epsilon_21

        global epsilon_ei
        epsilon_ei = epsilon_23

        global epsilon_ir
        epsilon_ir = epsilon_34

        global theta_se
        theta_se = theta_12

        global theta_si
        theta_si = theta_13

        global theta_es
        theta_es = theta_21

        global theta_ei
        theta_ei = theta_23

        global theta_ir
        theta_ir = theta_34

        global sigma_se
        sigma_se = sigma_12

        global sigma_si
        sigma_si = sigma_13

        global sigma_es
        sigma_es = sigma_21

        global sigma_ei
        sigma_ei = sigma_23

        global sigma_ir
        sigma_ir = sigma_34



        self.grid = MultiGrid(the_width, the_height, True)
        global width
        width = the_width
        global height
        height = the_height
        self.schedule = RandomActivation(self)
        self.running = True
        self.x = x
        self.y = y

        for i in range(self.num_agents):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            a = DiseaseAgent(i, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (x, y))
 
            # self.datacollector = DataCollector(model_reporters={"Current State": infection_rates},
            #    agent_reporters={"S": susceptible, "E": exposed, "I": infected, "R": recovered} )

            self.datacollector = DataCollector({"S": susceptible, "E": exposed, "I": infected, "R": recovered})
            
    
         


     
            
    def step(self):
    #    print('def step(self) of class DiseaseModel(Model) ')
        self.datacollector.collect(self)
        self.schedule.step()
  