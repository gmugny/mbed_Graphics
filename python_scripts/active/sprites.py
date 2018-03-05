import numpy as np
from scipy import misc

sprite_x = 16
sprite_y = 16

rr = np.arange(0, 2**3)
gg = np.arange(0, 2**3)
bb = np.arange(0, 2**2)

def sprite000():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s000_water.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite001():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s001_beachsand.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite


def sprite002():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s002_snowpeak.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite003():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s003_stonepeak.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite004():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s004_wetpeak.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite005():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s005_drydirt.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite006():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s006_dirt.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite007():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s007_wetdirt.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite008():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s008_rock.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite009():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s009_deadforest.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite010():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s010_plains.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite011():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s011_forest.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite012():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s012_jungle.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite013():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s013_dirtysand.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite014():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s014_bog.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite015():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s015_swamp.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite016():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s016_player_wb1.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite017():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s017_player_wb2.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite018():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s018_player_wd1.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite019():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s019_player_wd2.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite020():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s020_player_wr1.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def sprite021():
    im_path = '/home/pi/Documents/PythonScripts/Sprites/s021_player_wr2.bmp'
    this_sprite = bitmap_fix(im_path)
    return this_sprite

def bitmap_fix(path_in):
    this_sprite = misc.imread(path_in, mode='RGB')
    this_sprite[:, :, 0] = np.round((this_sprite[:, :, 0]/255)*np.max(rr))
    this_sprite[:, :, 1] = np.round((this_sprite[:, :, 1]/255)*np.max(gg))
    this_sprite[:, :, 2] = np.round((this_sprite[:, :, 2]/255)*np.max(bb))
    return this_sprite
