#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:27:44 2022

@author: andreaskoundouros
"""

# This script compares the standard medium-scale NK model to the same model 
# extended with price indexation

# Import packages
import econpizza as ep 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "svg" # For plotting in the Spyder window

# Load and solve standard medium-scale NK model
med_nk = '/medium_scale_nk_models/med_scale_nk.yaml' # If needed, adjust for individual file path here
med_nk_mod = ep.load(med_nk)
_ = med_nk_mod.solve_stst() 

# Load and solve medium-scale NK model with price indexation 
med_nk_price_indexation = '/medium_scale_nk_models/med_scale_nk_price_indexation.yaml' # If needed, adjust for individual file path here
med_nk_price_indexation_mod = ep.load(med_nk_price_indexation)
_ = med_nk_price_indexation_mod.solve_stst() 

# Specify shock 
shocks = ('e_beta', 0.01)

# Find IRFs
nk_x, nk_flag = med_nk_mod.find_path(shock = shocks)
nk_price_indexation_x, nk_price_indexation_flag = med_nk_price_indexation_mod.find_path(shock = shocks)

# Create data frame for plotting
time = list(range(0,50,1))
infl = np.column_stack([time, nk_x[:50, 15], nk_price_indexation_x[:50, 15]]) # Concatenate data 
infl = pd.DataFrame(infl, columns = ['Quarters', 'Inflation w/o Indexation', 'Inflation w Indexation']) # Turn data into data frame

# Plotting
fig = px.line(infl, x = "Quarters", y = ['Inflation w/o Indexation', 'Inflation w Indexation'])
fig.update_layout(title='', # Empty title
                   xaxis_title='Quarters', # x-axis labeling
                   yaxis_title='Gross Inflation', # y-axis labeling
                   legend=dict( # For horizontal legend
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
), plot_bgcolor = 'whitesmoke')
fig.show() # Display plot
