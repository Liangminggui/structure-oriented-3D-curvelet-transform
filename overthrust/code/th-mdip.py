# This code is used to implement struture-oriented thresholding of sythtic data


import numpy as np
import time
import curvelops.fdct3d_wrapper as ct
from function import *
import matplotlib.pyplot as plt

plt.close('all')
start_time = time.time()
data  = np.memmap('../data.dat',  dtype='float32', mode='r', shape=(67, 67, 130))
noise = np.memmap('../noise.dat', dtype='float32', mode='r', shape=(67, 67, 130))
dip   = np.memmap('../dip0.dat',   dtype='float32', mode='r', shape=(67, 67, 130))


# curvelet parameter
clip = 2
nbscales = 5
nbdstz_coarse = 4
ac = 1
n1, n2, n3 = data.shape



tau1 = np.array([0, 0.43, 0.43, 0.42, 0.54])
tau2 = np.array([0, 0.30, 0.30, 0.30, 0.36])

# # dip area
tau_dip = 1.8 # T_{\mu} oprator
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
 
        
xinv = np.real(ct.fdct3d_inverse_wrap(*data.shape, nbscales, nbdstz_coarse, ac, C))

savebin(xinv, '../th_mdip.dat')

end_time = time.time()
exection_time = end_time - start_time
print("Execution time: ", exection_time, "seconds")

snr1 = SNR(data, noise)
print('noise data snr:', snr1)

snr = SNR(data, xinv)
print('SNR:', snr)








