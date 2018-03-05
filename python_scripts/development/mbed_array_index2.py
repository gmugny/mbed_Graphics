import numpy as np

vis_grid_x = 15
vis_grid_y = 15
vis_grid_n = vis_grid_x * vis_grid_y
pos_x = 1
pos_y = 11
world_x = 50
world_y = 30
world_n = world_x * world_y

map003_collision = np.genfromtxt('/home/pi/Documents/mbed_Graphics/output_maps/map003_collision.out', delimiter=',')
map003_collision = map003_collision[0:world_y][:,0:world_x]
map003_collision = np.reshape(map003_collision, (world_y*world_x))

out = np.zeros((vis_grid_n))
for i_8 in range(0, vis_grid_n):
    out[i_8] = map003_collision[((i_8%vis_grid_x)+pos_x) + (((i_8//vis_grid_x)+pos_y)*world_x)]
    #if (map003_collision[((i_8%vis_grid_x)+pos_x) + (((i_8//vis_grid_x)+pos_y)*world_x)]):
    #    out[i_8] = 2

out2 = np.reshape(out, (vis_grid_y, vis_grid_x))

map003_npcm = np.genfromtxt('/home/pi/Documents/mbed_Graphics/output_maps/map003_npc.out', delimiter=',')
map003_npcm = map003_npcm[0:world_y][:,0:world_x]
map003_npc = np.reshape(map003_npcm, (world_y*world_x))

npc_n = 0
for i_16 in range(0, world_n):
    if (map003_npc[i_16] == 1):
        npc_n = npc_n + 1
        
npc_loc = np.zeros((npc_n, 1))
i_8 = 0
for i_16 in range(0, world_n):
    if (map003_npc[i_16] == 1):
        npc_loc[i_8] = i_16;
        i_8 = i_8 + 1
        
b = npc_loc[0]%world_x
c = npc_loc[0]//world_x
d = np.zeros((world_n, 1))
for i_16 in range(0, world_n):
    pos_x = i_16%world_x
    pos_y = i_16//world_x
    d[i_16] = ((b >= pos_x) & (b <= (pos_x + vis_grid_x)) & (c >= pos_y) & (c <= (pos_y + vis_grid_y)))

e = np.reshape(d, (world_y, world_x))



