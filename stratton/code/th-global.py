# This code is used to implement global thresholding of sythtic data


import time
import numpy as np
from function import *
import curvelops.fdct3d_wrapper as ct
import matplotlib.pyplot as plt

start_time = time.time()

noise = np.memmap('../cube.dat',  dtype='float32', mode='r', shape=(100, 77, 350))


# curvelet transform parameters
ac = 1
nbscales = 5
nbdstz_coarse = 4

# forwarding transform
cof = ct.fdct3d_forward_wrap(nbscales, nbdstz_coarse, ac, noise)


tau = 450
for s in range(len(cof)):
    for w in range(len(cof[s])):

        cof[s][w] = hardthreshold(cof[s][w], tau)

# inverse transform
xinv = np.real(ct.fdct3d_inverse_wrap(*noise.shape, nbscales, nbdstz_coarse, ac, cof))

savebin(xinv, '../th_global.dat')

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


