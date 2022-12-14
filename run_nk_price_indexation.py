#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:27:44 2022

@author: andreaskoundouros
"""

# This script compares the standard small-scale NK model to the same model 
# extended with price indexation

# Import packages
import econpizza as ep 
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "svg" # For plotting in the Spyder window


# Load and solve standard NK model
nk = "/small_scale_nk/nk.yaml" # Adjust for individual file path here
nk_mod = ep.load(nk)
_ = nk_mod.solve_stst() 

# Load and solve NK model with price indexation 
nk_price_indexation = "/small_scale_nk/nk_price_indexation.yaml" # Adjust for individual file path here
nk_price_indexation_mod = ep.load(nk_price_indexation)
_ = nk_price_indexation_mod.solve_stst() 

# Specify shock 
shocks = ('e_beta', 0.01)

# Find IRFs
nk_x, nk_flag = nk_mod.find_path(shock = shocks)
nk_price_indexation_x, nk_price_indexation_flag = nk_price_indexation_mod.find_path(shock = shocks)

# Create data frame for plotting
time = list(range(0,50,1))
infl = np.column_stack([time, nk_x[:50, 2], nk_price_indexation_x[:50, 2]]) # Concatenate data 
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
