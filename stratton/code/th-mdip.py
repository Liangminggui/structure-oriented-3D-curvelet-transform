# This code is used to implement struture-oriented thresholding of sythtic data


import time
import numpy as np
from function import *
import curvelops.fdct3d_wrapper as ct
import matplotlib.pyplot as plt


start_time = time.time()
noise = np.memmap('../cube.dat',  dtype='float32', mode='r', shape=(100, 77, 350))
dip   = np.memmap('../ndip.dat',    dtype='float32', mode='r', shape=(100, 77, 350))

# curvelet parameter
ac = 1
clip = 2
nbscales = 5
nbdstz_coarse = 4
n1, n2, n3 = noise.shape


tau1 = np.array([0, 0, 400, 400, 500])
tau2 = np.array([0, 0, 250, 250, 300])


# # dip area
tau_dip = 1.4
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



pos0 = 10;
clip1=3e3; screentio=0.3;
pos1 = slice(None); pos2 = slice(None);
noise1 = np.transpose(noise[pos0, pos1, pos2])
xinv1 = np.transpose(xinv[pos0, pos1, pos2])

fig2 = plt.figure(); plt.imshow(noise1, cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=screentio, interpolation='none'), plt.title('Noise')
fig3 = plt.figure(); plt.imshow(xinv1, cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=screentio, interpolation='none'), plt.title('Global')
fig3 = plt.figure(); plt.imshow(noise1-xinv1, cmap='seismic2', vmin=-clip1, vmax=clip1, aspect=screentio, interpolation='none'), plt.title('Global')





















