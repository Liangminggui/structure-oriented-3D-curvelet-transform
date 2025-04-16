#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 10:40:06 2024

@author: lmg
"""

import time
import numpy as np
import pyortho as lo
from function import *
import matplotlib.pyplot as plt
import curvelops.fdct3d_wrapper as ct


start_time = time.time()
data  = np.memmap('../sim.dat',   dtype='float32', mode='r', shape=(20, 130, 500))
dip   = np.memmap('../dip.dat',   dtype='float32', mode='r', shape=(20, 130, 500))
datad = np.memmap('../data-lar-xt.dat', dtype='float32', mode='r', shape=(20, 130, 500))

# curvelet parameter
ac = 1
clip = 2
nbscales = 5
nbdstz_coarse = 4
n1, n2, n3 = data.shape


tau1 = np.array([1e8, 1e8, 1e8, 1e8, 1e8])
tau2 = np.array([0, 0, 0, 0, 0])


# # dip area
tau_dip = 3
dip = dip*(np.abs(dip) >= tau_dip*np.ones_like(dip))
index = np.argwhere(dip != 0)


# forward transform
C = ct.fdct3d_forward_wrap(nbscales, nbdstz_coarse, ac, data)


for s in range(len(C)):
    for w in range(len(C[s])):
        

        temp0_real = np.zeros_like(C[s][w].real)
        temp0_imag = np.zeros_like(C[s][w].imag)
        
        temp0_real[:] = C[s][w].real[:]
        temp0_imag[:] = C[s][w].imag[:]
        temp0 = temp0_real + temp0_imag*1j
        temp1 = temp0_real + temp0_imag*1j

        C[s][w] = np.zeros(np.shape(C[s][w]))

        m3, m2, m1 = np.shape(temp0)
        rate_x = m1 / n1
        rate_y = m2 / n2
        rate_z = m3 / n3
        
        scaled_indices = (index * [rate_x, rate_y, rate_z]).astype(int)
        temp0[scaled_indices[:, 2], scaled_indices[:, 1], scaled_indices[:, 0]] = 0
        
        temp1 = temp1 - temp0
    
        temp0 = hardthreshold(temp0, tau1[s]) 
        temp1 = hardthreshold(temp1, tau2[s]) # the cut of area

        C[s][w]  = temp0 + temp1
        # C[s][w]  = temp1
 
        
new = np.real(ct.fdct3d_inverse_wrap(*data.shape, nbscales, nbdstz_coarse, ac, C))

savebin(new, '../data-lar-ct.dat')


end_time = time.time()
exection_time = end_time - start_time
print("Execution time: ", exection_time, "seconds")

# # show the slice
pos0 = 2; clip1= 0.15
pos1 = slice(None); pos2 = slice(None);
data1 = np.transpose(data[pos0, pos1, pos2])
new1 = np.transpose(new[pos0, pos1, pos2])
datad11 = np.transpose(datad[pos0, pos1, pos2])

fig1 = plt.figure(); plt.imshow(new1,        cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=0.4), plt.title('Data')
# fig3 = plt.figure(); plt.imshow(new1-datad11, cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=0.4), plt.title('Dip')
# fig1 = plt.figure(); plt.imshow(data1,        cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=0.4), plt.title('Data')
# fig5 = plt.figure(); plt.imshow(data1-new1,   cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=0.4), plt.title('noise-dip')





