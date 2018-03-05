import numpy as np
import matplotlib.pyplot as plt
import sprites

path_in = '/home/pi/Documents/mbed_Graphics/bitmap_maps/test_town_000.bmp'

this_map = sprites.bitmap_fix(path_in)
this_map = np.left_shift(this_map[:, :, 0], 5) + np.left_shift(this_map[:, :, 1], 2) + this_map[:, :, 2]

npc_map = np.zeros(np.shape(this_map), dtype='uint8')
npc_map[7, 2] = 2;
npc_map[15, 23] = 5;
npc_map[23, 40] = 4;
npc_map[27, 31] = 3;

collision_map = np.ones(np.shape(this_map), dtype='uint8')
collision_map[np.logical_and(np.logical_and(this_map != 11, this_map != 3), this_map != 56)] = False;
collision_map[this_map == 56] = 2;


np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map003.out', this_map, delimiter=',',fmt='%i',newline=',\n')
np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map003_npc.out', npc_map, delimiter=',',fmt='%i',newline=',\n')
np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map003_collision.out', collision_map, delimiter=',',fmt='%i',newline=',\n')

fig, ax = plt.subplots()
cax = ax.imshow(this_map)
fig2, ax2 = plt.subplots()
cax2 = ax2.imshow(npc_map)
fig3, ax3 = plt.subplots()
cax3 = ax3.imshow(collision_map)

plt.show()