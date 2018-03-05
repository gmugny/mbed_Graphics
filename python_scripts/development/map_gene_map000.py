import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import ndimage

rr = np.arange(0, 2**3)
gg = np.arange(0, 2**3)
bb = np.arange(0, 2**2)

bi = 0
this_color = np.zeros((256, 1, 3))
for ii in range(0, np.size(rr)):
    for jj in range(0, np.size(gg)):
        for kk in range(0, np.size(bb)):
            this_color[bi, 0, 0] = rr[ii]
            this_color[bi, 0, 1] = gg[jj]
            this_color[bi, 0, 2] = bb[kk]
            bi = bi + 1

this_color = np.reshape(this_color, (16, 16, 3))
this_color_norm = np.zeros((16, 16, 3), dtype='double')
this_color_norm[:, :, 0] = this_color[:, :, 0]/np.max(rr)
this_color_norm[:, :, 1] = this_color[:, :, 1]/np.max(gg)
this_color_norm[:, :, 2] = this_color[:, :, 2]/np.max(bb)

grid = np.random.randint(256, size=(200, 200), dtype='uint8')
grid2 = np.zeros((200, 200), dtype='uint8')

grid2[np.nonzero(grid>253)]= 1

struct2 = [[False, True, True, False],
           [True, False, True, True],
           [True, True, False, True],
           [False, True, True, False]]
grid2 = ndimage.binary_dilation(grid2, structure=struct2, iterations=6).astype(grid2.dtype)
grid2[np.nonzero(grid2==1)]= 8

fig, ax = plt.subplots()
cax = ax.imshow(grid2, cmap='binary')
#cax = ax.imshow(this_color_norm)
fig.colorbar(cax)

np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map000.out', grid2, delimiter=',',fmt='%i')

plt.show()