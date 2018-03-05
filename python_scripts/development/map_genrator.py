import numpy as np
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex

def biome(e, m):
    a = np.zeros(np.shape(e))
    a[m < 0.66] = 15;
    a[m < 0.33] = 14;
    a[m < 0.16] = 13;
    a[e > 0.3] = 12;
    a[np.bitwise_and(e > 0.3, m < 0.83)] = 11;
    a[np.bitwise_and(e > 0.3, m < 0.5)] = 10;
    a[np.bitwise_and(e > 0.3, m < 0.16)] = 9;
    a[e > 0.6] = 8;
    a[np.bitwise_and(e > 0.6, m < 0.66)] = 7;
    a[np.bitwise_and(e > 0.8, m < 0.33)] = 6;
    a[e > 0.8] = 5;
    a[np.bitwise_and(e > 0.8, m < 0.5)] = 4;
    a[np.bitwise_and(e > 0.8, m < 0.2)] = 3;
    a[np.bitwise_and(e > 0.8, m < 0.1)] = 2;
    a[e < 0.12] = 1;
    a[e < 0.1] = 0;
    return a

def simple_biome(e):
    a = 3*np.ones(np.shape(e))
    a[e < 0.8] = 8;
    a[e < 0.6] = 11;
    a[e < 0.2] = 1;
    a[e < 0.1] = 0;
    return a

def normalise(a):
    return (a - np.min(a))/(np.max(a) - np.min(a))

# mountain frequency
scale = 6
m_x = 400
m_y = 400
elevation = np.zeros((m_y, m_x))
moisture = np.zeros((m_y, m_x))
e_n = OpenSimplex(seed=10)
m_n = OpenSimplex(seed=20)
for ii in range(0, m_y):
    for jj in range(0, m_x):
        #a[ii, jj] = (tmp.noise2d(x=ii*scale, y=jj*scale)+1)/2*255
        n_x = ((jj/m_x)-0.5)
        n_y = ((ii/m_y)-0.5)
        e_p1 = 1 * e_n.noise2d(x=n_x*scale*1, y=n_y*scale*1)
        e_p2 = 0.5 * e_n.noise2d(x=n_x*scale*2, y=n_y*scale*2)
        e_p3 = 0.25 * e_n.noise2d(x=n_x*scale*4, y=n_y*scale*4)
        elevation[ii, jj] = e_p1 + e_p2 + e_p3
        m_p1 = 1 * m_n.noise2d(x=n_x*scale*1, y=n_y*scale*1)
        m_p2 = 0.5 * m_n.noise2d(x=n_x*scale*2, y=n_y*scale*2)
        m_p3 = 0.25 * m_n.noise2d(x=n_x*scale*4, y=n_y*scale*4)
        moisture[ii, jj] = m_p1 + m_p2 + m_p3
        

elevation = normalise(elevation)
elevation = np.power(elevation, 1.6)
moisture = normalise(moisture)
#a = simple_biome(elevation)
a = biome(elevation, moisture)

np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map001.out', a, delimiter=',',fmt='%i',newline=',\n')

fig, ax = plt.subplots()
cax = ax.imshow(a)
fig2, ax2 = plt.subplots()
#cax2 = ax2.scatter(elevation, a, c=a)
cax2 = ax2.scatter(elevation, moisture, a, c=a)

plt.show()