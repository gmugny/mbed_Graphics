import numpy as np
#import matplotlib as mpl
#mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
#from scipy import ndimage
#from mpldatacursor import datacursor
#from skimage import color

rr = np.arange(0, 2**3)
gg = np.arange(0, 2**3)
bb = np.arange(0, 2**2)

bi = 0
this_color = np.zeros((256, 3))
for ii in range(0, np.size(rr)):
    for jj in range(0, np.size(gg)):
        for kk in range(0, np.size(bb)):
            this_color[bi, 0] = rr[ii]
            this_color[bi, 1] = gg[jj]
            this_color[bi, 2] = bb[kk]
            bi = bi + 1

this_color = np.reshape(this_color, (16, 16, 3))
this_color_norm = np.zeros((16, 16, 3), dtype='double')
this_color_norm[:, :, 0] = this_color[:, :, 0]/np.max(rr)
this_color_norm[:, :, 1] = this_color[:, :, 1]/np.max(gg)
this_color_norm[:, :, 2] = this_color[:, :, 2]/np.max(bb)

rgb = np.floor(this_color_norm * 255)
#lab = color.rgb2lab(rgb)
#lab = np.reshape(lab, (256, 3))
#lab = np.sort(lab, axis=0)
#lab = np.reshape(lab, (16, 16, 3))
#rgb = color.lab2rgb(lab)
rgb = np.reshape(rgb, (256, 3))
aa = rgb

np.savetxt('/home/pi/Documents/PythonScripts/8bit_color.out', aa, delimiter=' ',fmt='%i')

fig, ax = plt.subplots()
cax = ax.imshow(this_color_norm)

#datacursor(cax)

plt.show()

