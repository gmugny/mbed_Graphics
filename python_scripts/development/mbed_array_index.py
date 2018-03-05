import numpy as np

n_x = 240
n_y = 240
n_v = n_x * n_y

world_x = 200

sprite_x = 16
sprite_y = 16
n_sprites = 3

vis_grid_x = n_x // sprite_x
vis_grid_y = n_y // sprite_y

pos_x = 0
pos_y = 0

map_index_x = np.zeros((n_v))
map_index_y = np.zeros((n_v))
map_index = np.zeros((n_v))
sprite_index = np.zeros((n_v))
ind1 = np.zeros((n_v))
ind2 = np.zeros((n_v))
for i_16 in range(0, n_v):
    map_index_x[i_16] = (((i_16//sprite_x)%vis_grid_x)+pos_x)
    map_index_y[i_16] = (((i_16//(n_x*sprite_x))+pos_y)*world_x)
    map_index[i_16] = map_index_x[i_16] + map_index_y[i_16]
    sprite_index[i_16] = ((i_16%sprite_x)+(sprite_x*2)) + ((i_16%(n_x*sprite_x)//n_x)*(sprite_x*n_sprites))
    ind1[i_16] = (i_16%sprite_x)
    ind2[i_16] = ((i_16//n_x)*n_x)
    
aa = np.reshape(ind1, (n_y, n_x))
bb = np.reshape(range(0, n_v), (n_y, n_x))