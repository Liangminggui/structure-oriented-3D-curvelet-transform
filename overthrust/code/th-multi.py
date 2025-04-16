# This code is used to implement multi-scale thresholding of sythtic data


import io
import time
import base64
import numpy as np
from PIL import Image
from function import *
import matplotlib.pyplot as plt
import curvelops.fdct3d_wrapper as ct



plt.close('all')
start_time = time.time()
data  = np.memmap('../data.dat',  dtype='float32', mode='r', shape=(67, 67, 130))
noise = np.memmap('../noise.dat', dtype='float32', mode='r', shape=(67, 67, 130))



# curvelet transform parameters
ac = 1
nbscales = 5
nbdstz_coarse = 4

# forwarding transform
cof = ct.fdct3d_forward_wrap(nbscales, nbdstz_coarse, ac, noise)

tau = np.array([0, 0.38, 0.38, 0.38, 0.52])



for s in range(len(cof)):
    for w in range(len(cof[s])):

        cof[s][w] = hardthreshold(cof[s][w], tau[s])

# inverse transform
xinv = np.real(ct.fdct3d_inverse_wrap(*data.shape, nbscales, nbdstz_coarse, ac, cof))

# save to binary data
savebin(xinv, '../th_multi.dat')



end_time = time.time()
exection_time = end_time - start_time
print("Execution time: ", exection_time, "seconds")

snr1 = SNR(data, noise)
print('noise data snr:', snr1)

snr = SNR(data, xinv)
print('SNR:', snr)



