import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# hard threshold
def hardthreshold(input, threshold):
    E = np.ones_like(input)
    output = input*(np.abs(input) >= threshold * E)
    return output


# save binary data to float32 for mada and matlab
def savebin(arr, filename):
    arr = arr.astype(np.float32)
    arr.tofile(filename)
    

# define the red-black colorsmap
def seis2():
    if 'seismic2' not in plt.colormaps():
        N = 40
        u1 = np.concatenate((np.ones(N),  np.linspace(1., 1, 128-N), np.linspace(1, 0, 128-N), np.zeros(N)))
        u2 = np.concatenate((np.zeros(N), np.linspace(0., 1, 128-N), np.linspace(1, 0, 128-N), np.zeros(N)))
        u3 = np.concatenate((np.zeros(N), np.linspace(0., 1, 128-N), np.linspace(1, 0, 128-N), np.zeros(N)))
        colors = np.column_stack((u1, u2, u3))
        cmap = LinearSegmentedColormap.from_list('seismic2', colors)
        plt.register_cmap(cmap=cmap)
    else:
        cmap = 'seismic2'
seis2()


def SNR(I, In):
    """
    """
    Ps = np.sum(I ** 2)
    Pn = np.sum((In - I) ** 2)
    snr = 10 * np.log10(Ps / Pn)
    return snr

