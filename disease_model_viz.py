from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from disease_model import *
# from disease_model import DiseaseModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "false",
                 "r": 0.9}

    if agent.state == 0:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    elif agent.state == 1:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0
        
    elif agent.state == 2:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        
    elif agent.state == 3:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 1000, 1000)

number_of_people = 1000
width_of_grid = 30
height_of_grid = 30

mu_2 = 0.1
mu_3 = 0

#Initiating with at t_0 : S and E (no Infected at t = 0 days)
# Case 1: Infection 0 in the region at t = 0
# Case 2: Infection not 0 in the region at t = 0
# Exposed turns Infected or Susceptible after a number of days

mu_1 = 1 - mu_2 - mu_3

delta_1 = 0.01
delta_2 = 0
delta_3 = 0
delta_4 = 0
beta_12 = 0.006
beta_13 = 0.007
beta_21 = 0.008
beta_23 = 0.006
beta_34 = 0.009
epsilon_12 = 5
epsilon_13 = 6
epsilon_21 = 7
epsilon_23 = 8
epsilon_34 = 9
theta_12 = 0.1
theta_13 = 0.2
theta_21 = 0.3
theta_23 = 0.4
theta_34 = 0.5
sigma_12 = 0.06
sigma_13 = 0.07
sigma_21 = 0.08
sigma_23 = 0.09
sigma_34 = 0.1


line_charts = ChartModule([
    {'Label': 'S', 'Color': 'blue'},
    {'Label': 'E', 'Color': 'orange'},
     {'Label': 'I', 'Color': 'green'},
    {'Label': 'R', 'Color': 'red'}])


server = ModularServer(DiseaseModel,
                       [grid, line_charts],
                       "SEIR Disease Model",
                       {"n": number_of_people, "the_width": width_of_grid, "the_height": height_of_grid, "x": width_of_grid-1, "y": height_of_grid-1, "mu_1": mu_1, "mu_2":mu_2, "mu_3": mu_3, "delta_1": delta_1, "delta_2": delta_2, "delta_3":delta_3, "delta_4":delta_4, "beta_12": beta_12, "beta_13": beta_13, "beta_21": beta_21, "beta_23": beta_23, "beta_34": beta_34, "epsilon_12": epsilon_12, "epsilon_13": epsilon_13, "epsilon_21": epsilon_21, "epsilon_23":epsilon_23, "epsilon_34": epsilon_34, "theta_12": theta_12, "theta_13": theta_13, "theta_21": theta_21, "theta_23": theta_23, "theta_34": theta_34, "sigma_12": sigma_12, "sigma_13": sigma_13, "sigma_21": sigma_21, "sigma_23": sigma_23, "sigma_34": sigma_34})


server.port = 8521 # The default
server.launch()