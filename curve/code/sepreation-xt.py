#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 17:30:29 2024

@author: lmg
"""

import time
import numpy as np
from function import *
import matplotlib.pyplot as plt
import curvelops.fdct3d_wrapper as ct

plt.close('all')
start_time = time.time()
data  = np.memmap('../sim.dat', dtype='float32', mode='r', shape=(20, 130, 500))
dip   = np.memmap('../dip.dat', dtype='float32', mode='r', shape=(20, 130, 500))


# curvelet parameter
ac = 1
clip = 2
nbscales = 5
nbdstz_coarse = 4
n1, n2, n3 = data.shape


# # dip area
tau_dip = 3
dip = dip*(np.abs(dip) >= tau_dip*np.ones_like(dip))
index = np.argwhere(dip != 0)

datas = np.copy(data)
datas[index[:, 0], index[:, 1], index[:, 2]] = 0
datad = data - datas
savebin(datad, '../data-lar-xt.dat')


C = ct.fdct3d_forward_wrap(nbscales, nbdstz_coarse, ac, data)

s=4; w=1161 # Manual selection

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

max_index = np.array([m1-1, m2-1, m3-1])
scaled_indices = (index * [rate_x, rate_y, rate_z])
scaled_indices = np.round(scaled_indices).astype(int)
scaled_indices = np.clip(scaled_indices, 0, max_index)


# scaled_indices = (index * [rate_x, rate_y, rate_z]).astype(int)
temp0[scaled_indices[:, 2], scaled_indices[:, 1], scaled_indices[:, 0]] = 0
temp1 = temp1 - temp0
cof1 = np.real(C[s][w])

temp0 = np.real(temp0)
temp1 = np.real(temp1)

a = temp0+temp1

pos0c = slice(None); clip1c=1e-1; screentio=1
pos1c = slice(None); pos2c = 0;
temp11 = np.transpose(a[pos0c, pos1c, pos2c])
fig3 = plt.figure(); plt.imshow(temp11, cmap='seismic2', vmin=-clip1c, vmax=clip1c, aspect=screentio), plt.title('Global')


savebin(temp1, '../cof-lar.dat')
savebin(a,     '../cof-all.dat')


# # show the slice(70 ,40)
pos0 = 2; clip1=0.15; screentio=0.3
pos1 = slice(None); pos2 = slice(None);
datad1 = np.transpose(datad[pos0, pos1, pos2])
datas1 = np.transpose(datas[pos0, pos1, pos2])


cof1 = np.real(C[4][1161])
pos0c = slice(None); clip1c=5e-2; screentio=1
pos1c = slice(None); pos2c = 0;
cof11 = np.transpose(cof1[pos0c, pos1c, pos2c])
fig3 = plt.figure(); plt.imshow(cof11, cmap='seismic2', vmin=-clip1c, vmax=clip1c, aspect=screentio), plt.title('Global')











   
