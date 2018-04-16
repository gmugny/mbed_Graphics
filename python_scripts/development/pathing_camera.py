import numpy as np
import matplotlib.pyplot as plt

vis_grid_x = 15
vis_grid_y = 15
vis_grid_n = vis_grid_x * vis_grid_y

start_pos = 112
#start_pos = 526
#end_pos = 112
#end_pos = 525

#collision_map[np.unravel_index(start_pos, collision_map.shape, 'F')] = 2
#collision_map[np.unravel_index(end_pos, collision_map.shape, 'F')] = 3
fill_map = np.ones((vis_grid_y, vis_grid_x), dtype='uint8')*30
collision_map = np.ones((vis_grid_y, vis_grid_x), dtype='uint8')
collision_map[0, 0] = 0
collision_map[1, 0] = 0
collision_map[2, 0] = 0
collision_map[0, 2] = 0
collision_map[1, 2] = 0
collision_map[2, 2] = 0
collision_map[3, 2] = 0
collision_map[3, 3] = 0
collision_map[3, 4] = 0
collision_map[3, 5] = 0
collision_map[3, 6] = 0
collision_map[2, 6] = 0
collision_map[1, 6] = 0
this_point = start_pos
fill_map[np.unravel_index(this_point, collision_map.shape, 'F')] = 0
queue = [this_point]
this_value = fill_map[np.unravel_index(this_point, collision_map.shape, 'F')]
#map_n-1
for ii in range(0, vis_grid_n):
    ixn = np.size(queue)
    if ixn == 0:
        break
    this_point = queue[0]
    this_value = fill_map[np.unravel_index(this_point, collision_map.shape, 'F')]
    if ((this_point%vis_grid_x)+1 < vis_grid_x) and (fill_map[np.unravel_index(this_point+1, collision_map.shape, 'F')] == 30) and (collision_map[np.unravel_index(this_point+1, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point+1, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point+1)
    if ((this_point%vis_grid_x)-1 >= 0) and (fill_map[np.unravel_index(this_point-1, collision_map.shape, 'F')] == 30) and (collision_map[np.unravel_index(this_point-1, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point-1, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point-1)
    if ((this_point+vis_grid_x) < vis_grid_n) and (fill_map[np.unravel_index(this_point+vis_grid_x, collision_map.shape, 'F')] == 30) and (collision_map[np.unravel_index(this_point+vis_grid_x, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point+vis_grid_x, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point+vis_grid_x)
    if ((this_point-vis_grid_x) >= 0) and (fill_map[np.unravel_index(this_point-vis_grid_x, collision_map.shape, 'F')] == 30) and (collision_map[np.unravel_index(this_point-vis_grid_x, collision_map.shape, 'F')] == 1):
        fill_map[np.unravel_index(this_point-vis_grid_x, collision_map.shape, 'F')] = this_value+1
        queue.append(this_point-vis_grid_x)
    queue.pop(0)

fig, ax = plt.subplots()
cax = ax.imshow(fill_map)
cax.set_clim(0, 30)

plt.show()