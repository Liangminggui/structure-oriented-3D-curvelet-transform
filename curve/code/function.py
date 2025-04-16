import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def hardthreshold(input, threshold):
    
    # hard threshold
    E = np.ones_like(input)
    output = input*(np.abs(input) >= threshold * E)
    return output

def snr3d(g, f):
    
    # singal noise ration
    # g: ground data
    # f: reconstruct data
    
    ps = np.linalg.norm(f)
    pn = np.linalg.norm(f - g)
    snr = 10*np.log10(ps/pn)
    return snr

def savebin(arr, filename):
    
    # save binary data to float32 for mada and matlab
    arr = arr.astype(np.float32)

    # 写入二进制文件
    arr.tofile(filename)
    


def seis2():
    
    # create colormap like mada color=g, red-black
    if 'seismic2' not in plt.colormaps():
        N = 40
        u1 = np.concatenate((np.ones(N), np.linspace(1., 1, 128-N), np.linspace(1, 0, 128-N), np.zeros(N)))
        u2 = np.concatenate((np.zeros(N), np.linspace(0., 1, 128-N), np.linspace(1, 0, 128-N), np.zeros(N)))
        u3 = np.concatenate((np.zeros(N), np.linspace(0., 1, 128-N), np.linspace(1, 0, 128-N), np.zeros(N)))

        colors = np.column_stack((u1, u2, u3))
        cmap = LinearSegmentedColormap.from_list('seismic2', colors)
        
        # 使用自定义的seismic2或者已经存在的seismic2
        plt.register_cmap(cmap=cmap)
        
    else:
        
        cmap = 'seismic2'

seis2()









