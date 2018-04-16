import numpy as np
import glob
import sprites
import matplotlib.pyplot as plt
from map_output_C import read_map_CPP
from map_output_C import read_map_H

file_list = sorted(glob.glob("%s%s" % ("/home/pi/Documents/mbed_Graphics/bitmap_sprites", "/*.bmp")))

total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
for ii in range(0, np.size(file_list)):
    this_sprite = sprites.bitmap_fix(file_list[ii])
    export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
    total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
    
sprite_sheet = np.reshape(total_spritesheet, (np.size(total_spritesheet)))

dicta_cpp = read_map_CPP("/home/pi/Documents/mbed_Graphics/output_maps/map005.cpp")
dicta_h = read_map_H("/home/pi/Documents/mbed_Graphics/output_maps/map005.h")
this_map = dicta_cpp["map_array"]

sprite_x = 16
sprite_y = 16
sprite_n = sprite_x * sprite_y
post_pos_x = 2
post_pos_y = 1
buffer_size = sprite_n * 2 
n_x = sprite_x
n_sprites = 175

mm = np.zeros(buffer_size, dtype='uint32')
map_index = np.zeros(buffer_size, dtype='uint32')
total_map = np.zeros(buffer_size, dtype='uint8')
for i_16 in range(0, buffer_size):
#    mm[i_16]= (((i_16//sprite_x)%2)+post_pos_x) + (post_pos_y*dicta_h["map_x"][0])
#    map_index[i_16] = this_map[(((i_16//sprite_x)%2)+post_pos_x) + (post_pos_y*dicta_h["map_x"][0])];
#    sprite_pixel = ((i_16%sprite_x)+(sprite_x*map_index[i_16]))+(((i_16%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
#    total_map[i_16] = sprite_sheet[sprite_pixel]
#map_index = map[(((i_16/sprite_x)%vis_grid_x)+pos_x)+(((i_16/(n_x*sprite_x))+pos_y)*world_x)];
    mm[i_16] = (post_pos_x) + (((i_16//sprite_n)+post_pos_y)*dicta_h["map_x"][0])
    map_index[i_16] = this_map[mm[i_16]];
    sprite_pixel = ((i_16%sprite_x)+(sprite_x*map_index[i_16]))+(((i_16%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
    total_map[i_16] = sprite_sheet[sprite_pixel]
    
total_map_2 = np.reshape(total_map, (sprite_y*2, sprite_x))
total_map_2 = np.uint8(total_map_2)

disp_map = np.zeros((np.size(total_map_2, 0), np.size(total_map_2, 1), 3), dtype='uint8')
disp_map[:, :, 0] = ((np.right_shift(total_map_2, 5) & 7) / 7) * 255
disp_map[:, :, 1] = ((np.right_shift(total_map_2, 2) & 7) / 7) * 255
disp_map[:, :, 2] = ((total_map_2 & 3) / 3) * 255

fig, ax = plt.subplots()
cax = ax.imshow(disp_map)

plt.show()