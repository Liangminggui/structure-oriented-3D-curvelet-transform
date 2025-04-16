
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:23:32 2023

@author: lmg(this code havd three verion,this one is python)
"""

import numpy as np
import time
import curvelops.fdct3d_wrapper as ct
from function import *
import matplotlib.pyplot as plt


start_time = time.time()
noise = np.memmap('../noise.dat',   dtype='float32', mode='r', shape=(136, 111, 250))
dip   = np.memmap('../ndip.dat',     dtype='float32', mode='r', shape=(136, 111, 250))

# curvelet parameter
clip = 2
nbscales = 5
nbdstz_coarse = 4
ac = 1
n1, n2, n3 = noise.shape


tau1 = np.array([0, 0, 4, 5, 6])
tau2 = np.array([0, 0, 4, 3, 4])


# # dip area
tau_dip = 0.9
dip = dip*(np.abs(dip) >= tau_dip*np.ones_like(dip))
index = np.argwhere(dip != 0)


# forward transform
C = ct.fdct3d_forward_wrap(nbscales, nbdstz_coarse, ac, noise)


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
 
        
xinv = np.real(ct.fdct3d_inverse_wrap(*noise.shape, nbscales, nbdstz_coarse, ac, C))

savebin(xinv, '../th_mdip.dat')

end_time = time.time()
exection_time = end_time - start_time
print("Execution time: ", exection_time, "seconds")


# show the slice
pos0 = 52; 
screentio=0.4;
pos1 = slice(None); pos2 = slice(None);
noise1 = np.transpose(noise[pos0, pos1, pos2])
xinv1  = np.transpose(xinv[pos0, pos1, pos2])


plt.figure(figsize=(100, 50)); axis_num=3
plt.subplot(1, axis_num, 1)
plt.imshow(noise1, cmap='seismic2', vmin=-50, vmax=50, aspect=screentio, interpolation='none'), plt.title('Ground')
plt.subplot(1, axis_num, 2)
plt.imshow(xinv1, cmap='seismic2', vmin=-50, vmax=50, aspect=screentio, interpolation='none'), plt.title('Global')
plt.subplot(1, axis_num, 3)
plt.imshow(noise1-xinv1, cmap='seismic2', vmin=-50, vmax=50, aspect=screentio, interpolation='none'), plt.title('Ground-Global')
plt.show()






















