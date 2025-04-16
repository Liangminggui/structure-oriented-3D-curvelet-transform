import numpy as np
import time
import curvelops.fdct3d_wrapper as ct
from function import *
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


start_time = time.time()

noise = np.memmap('../noise.dat',  dtype='float32', mode='r', shape=(136, 111, 250))


# curvelet transform parameters
ac = 1
nbscales = 5
nbdstz_coarse = 4

# forwarding transform
cof = ct.fdct3d_forward_wrap(nbscales, nbdstz_coarse, ac, noise)


tau = np.array([0, 0, 4, 5, 6])

for s in range(len(cof)):
    for w in range(len(cof[s])):

        cof[s][w] = hardthreshold(cof[s][w], tau[s])

# inverse transform
xinv = np.real(ct.fdct3d_inverse_wrap(*noise.shape, nbscales, nbdstz_coarse, ac, cof))

# save to binary data
savebin(xinv, '../th_multi.dat')


end_time = time.time()
exection_time = end_time - start_time
print("Execution time: ", exection_time, "seconds")



# # show the slice
# pos0 = 52; 
# screentio=0.4;
# pos1 = slice(None); pos2 = slice(None);
# noise1 = np.transpose(noise[pos0, pos1, pos2])
# xinv1  = np.transpose(xinv[pos0, pos1, pos2])


# plt.figure(figsize=(100, 50)); axis_num=3
# plt.subplot(1, axis_num, 1)
# plt.imshow(noise1, cmap='seismic2', vmin=-50, vmax=50, aspect=screentio, interpolation='none'), plt.title('Ground')
# plt.subplot(1, axis_num, 2)
# plt.imshow(xinv1, cmap='seismic2', vmin=-50, vmax=50, aspect=screentio, interpolation='none'), plt.title('Global')
# plt.subplot(1, axis_num, 3)
# plt.imshow(noise1-xinv1, cmap='seismic2', vmin=-50, vmax=50, aspect=screentio, interpolation='none'), plt.title('Ground-Global')
# plt.show()


