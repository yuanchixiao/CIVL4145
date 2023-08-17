# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 10:34:35 2023

@author: s4680073
"""


import numpy as np
import matplotlib.pyplot as plt
import flopy
from flopy.utils.binaryfile import HeadFile
# Constants
h_1 = 11.2
h_2 = 9.6
L = 1500
W = 0.762 / 365
K = 110  # Replace this if you have a specific value for K.

# Define the equation for h in terms of x
def h(x):
    return np.sqrt(h_1**2 - ((h_1**2 - h_2**2) * x) / L + (W / K) * (L - x) * x)


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def nse(y_true, y_pred):
    return 1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2))

def pbias(y_true, y_pred):
    return (np.sum(y_true - y_pred) / np.sum(y_true)) * 100

def pcc(y_true, y_pred):
    return np.corrcoef(y_true, y_pred)[0, 1]


# Generate x values and corresponding h values
x = np.linspace(0, L, 32) # Adjust 400 for more or less points
h_analytical= h(x)


headobj = HeadFile('C:/Users/s4680073/OneDrive - The University of Queensland/tutor/CIVL4145/Run001/gwf-Base.hds')
times = headobj.get_times()
head_data = headobj.get_data(totim=times[-1])
h_modflow=head_data[0,10,:]
# Plot
plt.plot(h_analytical,label='analytical')
plt.plot(h_modflow,label='modflow')
plt.xlabel('x')
plt.ylabel('h')
plt.title('Visualization of h in terms of x')
plt.legend()
plt.grid(True)
plt.show()
rmse_value = rmse(h_modflow, h_analytical)
nse_value = nse(h_modflow, h_analytical)
pbias_value = pbias(h_modflow, h_analytical)
pcc_value = pcc(h_modflow, h_analytical)
print('rmse =',rmse_value,'nse =',nse_value,'pbias =',pbias_value,'pcc =',pcc_value)
