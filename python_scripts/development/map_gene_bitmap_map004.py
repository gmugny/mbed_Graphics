import numpy as np
import matplotlib.pyplot as plt
import sprites

path_in = '/home/pi/Documents/mbed_Graphics/bitmap_maps/forest_map_test.bmp'

this_map = sprites.bitmap_fix(path_in)
this_map = np.left_shift(this_map[:, :, 0], 5) + np.left_shift(this_map[:, :, 1], 2) + this_map[:, :, 2]

npc_map = np.zeros(np.shape(this_map), dtype='uint8')

collide_tile_list = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 56, 57, 58, 59, 60, 68, 80, 84, 93, 94]
collision_map = np.ones(np.shape(this_map), dtype='uint8')
logi = np.ones(np.shape(this_map), dtype='bool')
for ii in range(0, np.size(collide_tile_list)):
    logi = np.logical_and(logi, this_map != collide_tile_list[ii])
    
collision_map[logi] = False;
collision_map[this_map == 56] = 3;


np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map004.out', this_map, delimiter=',',fmt='%i',newline=',\n')
np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map004_npc.out', npc_map, delimiter=',',fmt='%i',newline=',\n')
np.savetxt('/home/pi/Documents/mbed_Graphics/output_maps/map004_collision.out', collision_map, delimiter=',',fmt='%i',newline=',\n')

fig, ax = plt.subplots()
cax = ax.imshow(this_map)
fig2, ax2 = plt.subplots()
cax2 = ax2.imshow(npc_map)
fig3, ax3 = plt.subplots()
cax3 = ax3.imshow(collision_map)

plt.show()