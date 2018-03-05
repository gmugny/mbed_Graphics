import numpy as np
import matplotlib.pyplot as plt
import sprites

path_in = '/home/pi/Documents/mbed_Graphics/bitmap_maps/forest_map_test.bmp'

this_map = sprites.bitmap_fix(path_in)
this_map = np.left_shift(this_map[:, :, 0], 5) + np.left_shift(this_map[:, :, 1], 2) + this_map[:, :, 2]

mm = np.shape(this_map);
map_y = mm[1];
map_x = mm[0];
map_n = map_x * map_y;

collide_tile_list = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 56, 57, 58, 59, 60, 68, 80, 84, 93, 94]
collision_map = np.ones(np.shape(this_map), dtype='uint8')
logi = np.ones(np.shape(this_map), dtype='bool')
for ii in range(0, np.size(collide_tile_list)):
    logi = np.logical_and(logi, this_map != collide_tile_list[ii])
    
collision_map[logi] = 0

start_pos = 101
#start_pos = 526
end_pos = 134
#end_pos = 525

#collision_map[np.unravel_index(start_pos, collision_map.shape, 'F')] = 2
#collision_map[np.unravel_index(end_pos, collision_map.shape, 'F')] = 3
fill_map = np.ones(np.shape(this_map), dtype='uint8')*255
this_point = start_pos
fill_map[np.unravel_index(this_point, collision_map.shape, 'F')] = 0
queue = [this_point]
this_value = fill_map[np.unravel_index(this_point, collision_map.shape, 'F')]
#map_n-1
for ii in range(0, map_n):
    ixn = np.size(queue)
    if ixn == 0:
        break
    this_point = queue[0]
    this_value = fill_map[np.unravel_index(this_point, collision_map.shape, 'F')]
    if ((this_point%map_x)+1 < map_x) and (fill_map[np.unravel_index(this_point+1, collision_map.shape, 'F')] == 255) and (collision_map[np.unravel_index(this_point+1, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point+1, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point+1)
    if ((this_point%map_x)-1 >= 0) and (fill_map[np.unravel_index(this_point-1, collision_map.shape, 'F')] == 255) and (collision_map[np.unravel_index(this_point-1, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point-1, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point-1)
    if ((this_point+map_x) < map_n) and (fill_map[np.unravel_index(this_point+map_x, collision_map.shape, 'F')] == 255) and (collision_map[np.unravel_index(this_point+map_x, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point+map_x, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point+map_x)
    if ((this_point-map_x) >= 0) and (fill_map[np.unravel_index(this_point-map_x, collision_map.shape, 'F')] == 255) and (collision_map[np.unravel_index(this_point-map_x, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point-map_x, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point-map_x)
    queue.pop(0)

nav_map = np.zeros(np.shape(this_map), dtype='uint8')
this_point = end_pos
nav_map[np.unravel_index(this_point, collision_map.shape, 'F')] = 1
for ii in range(0, map_n):
    chk = [255,255,255,255]
    points = [0,0,0,0]
    if this_point+1 < map_n:
        chk[0] = fill_map[np.unravel_index(this_point+1, collision_map.shape, 'F')]
        points[0] = this_point+1
    if this_point-1 >= 0:
        chk[1] = fill_map[np.unravel_index(this_point-1, collision_map.shape, 'F')]
        points[1] = this_point-1
    if (this_point+map_x < map_n):
        chk[2] = fill_map[np.unravel_index(this_point+map_x, collision_map.shape, 'F')]
        points[2] = this_point+map_x
    if (this_point-map_x >= 0):
        chk[3] = fill_map[np.unravel_index(this_point-map_x, collision_map.shape, 'F')]
        points[3] = this_point-map_x
    this_point = points[np.argmin(chk)]
    nav_map[np.unravel_index(this_point, collision_map.shape, 'F')] = 1
    if (this_point == start_pos):
        break

fig, ax = plt.subplots()
cax = ax.imshow(fill_map)
fig2, ax2 = plt.subplots()
cax2 = ax2.imshow(nav_map)

plt.show()