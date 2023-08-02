from disease_model import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
import plotly.express as px
import csv

from itertools import cycle
import random
import math
import scipy.stats as ss

import numpy as np
from scipy.integrate import odeint
#import matplotlib.pyplot as plt

import itertools

def looping(number_of_people, width_of_grid, height_of_grid,number_of_iterations, mu_2, mu_3, mu_1, delta_1, delta_2, delta_3, delta_4, beta_12, beta_13, beta_21, beta_23, beta_34, epsilon_12, epsilon_13, epsilon_21, epsilon_23, epsilon_34, theta_12, theta_13, theta_21, theta_23,theta_34, sigma_12, sigma_13, sigma_21, sigma_23, sigma_34 ):

#Initiating with at t_0 : S and E (no Infected at t = 0 days)
# Case 1: Infection 0 in the region at t = 0
# Case 2: Infection not 0 in the region at t = 0
# Exposed turns Infected or Susceptible after a number of days
    
   
    model = DiseaseModel(number_of_people, width_of_grid, height_of_grid, width_of_grid - 1, height_of_grid - 1,  mu_1, mu_2, mu_3, delta_1, delta_2, delta_3, delta_4, beta_12, beta_13, beta_21, beta_23, beta_34, epsilon_12, epsilon_13, epsilon_21, epsilon_23, epsilon_34, theta_12, theta_13, theta_21, theta_23, theta_34, sigma_12, sigma_13, sigma_21, sigma_23, sigma_34)
    for i in range(number_of_iterations):
        model.step()


    agent_reporters = model.datacollector.get_model_vars_dataframe()
#    print(agent_reporters)

    state_I = agent_reporters["I"]


# state_S = agent_reporters["S"]
# state_S.plot(legend='S')

# state_E = agent_reporters["E"]
# state_E.plot(legend='E')

# state_R = agent_reporters["R"]
# state_R.plot(legend='R')


# l = agent_reporters.values.tolist()
# plt.figure()
#merged = pd.DataFrame(list(itertools.chain.from_iterable(l)))
#merged.plot()


# model_reporters = model.datacollector.get_agent_vars_dataframe()
# print(model_reporters)

# # save the agent data to CSV
# agent_reporters.to_csv("agent_data.csv")

# # save the model data to CSV.
# model_reporters.to_csv("model_data.csv")
    return state_I
