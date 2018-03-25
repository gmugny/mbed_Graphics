# bug: sometimes you get an error about not being able to find image
# comment out canvas.createimage in SpritePanel, run the script, close all windows, uncomment canvas.createimage in SpritePanel, run, it should now work

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import scipy as sp
import glob
import sprites
import pandas as pd
import re
from npc_definitions import npc_list

class SpritePanel(tk.Frame):
    def __init__(self, root, path_in, n_rows, sprite_scaling, show_x_sprites, show_y_sprites):
        tk.Frame.__init__(self, root)
        
        self.n_rows = n_rows
        self.sprite_scaling = sprite_scaling
        self.selected_sprite = 0
        
        # load an image
        file_list = sorted(glob.glob("%s%s" % (path_in, "/*.bmp")))
        total_spritesheet = np.zeros((sprites.sprite_y*(((np.size(file_list))//n_rows)+1), sprites.sprite_x*n_rows), dtype='uint8')
        jj = 0
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            if ii%n_rows == 0:
                jj = jj + 1
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[(jj-1)*sprites.sprite_y:jj*sprites.sprite_y, (ii%n_rows)*sprites.sprite_x:((ii%n_rows)*sprites.sprite_x)+sprites.sprite_x] = export_sprite
        
        disp_sprite = np.zeros((np.size(total_spritesheet, 0), np.size(total_spritesheet, 1), 3), dtype='uint8')
        disp_sprite[:, :, 0] = ((np.right_shift(total_spritesheet, 5) & 7) / 7) * 255
        disp_sprite[:, :, 1] = ((np.right_shift(total_spritesheet, 2) & 7) / 7) * 255
        disp_sprite[:, :, 2] = ((total_spritesheet & 3) / 3) * 255
        
        disp_sprite_r = sp.misc.imresize(disp_sprite, [np.size(disp_sprite, 0)*sprite_scaling, np.size(disp_sprite, 1)*sprite_scaling, np.size(disp_sprite, 2)], interp='nearest', mode=None)
        
        sprite_pane_width = sprite_scaling*sprites.sprite_x*show_x_sprites
        sprite_pane_height = sprite_scaling*sprites.sprite_y*show_y_sprites

        # position the frame within the window
        self.pack(expand="no", fill="none", side="right")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=sprite_pane_width, height=sprite_pane_height, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")
        
        # bind the mouse button 1
        self.canvas.bind("<Button 1>", self.select_sprite)
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
        # convert the array into a Image object
        im=Image.fromarray(disp_sprite_r, 'RGB')
        
        # set the starting point of the scroll
        width,height=im.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def select_sprite(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//(sprites.sprite_x*self.sprite_scaling)
        y_pos = y_pix//(sprites.sprite_y*self.sprite_scaling)
        self.selected_sprite = x_pos + (y_pos * self.n_rows)

class MapPanel(tk.Frame):
    def __init__(self, root, sprite_select):
        tk.Frame.__init__(self, root)
        
        self.handle_SpritePanel = sprite_select
        
        self.map_x = 1
        self.map_y = 1
        self.generate_map()
        
        self.pack(expand="no", fill="none", side="left")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=400, height=300, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")

        self.canvas.bind("<Button 1>", self.change_map_element)
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
    def load_sprite_sheet(self):
        file_list = sorted(glob.glob("%s%s" % (self.sprite_path, "/*.bmp")))
        
        total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
            
        self.sprite_sheet = total_spritesheet
        
    def change_map_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        self.current_map[y_pos, x_pos] = self.handle_SpritePanel.selected_sprite
        self.update_map_image()
        
    def set_sprite_path(self, path_in):
        self.sprite_path = path_in
        
    def generate_map(self):
        self.current_map = np.ones((self.map_y, self.map_x), dtype='uint8')
        
    def load_map_bitmap(self, path_in):
        this_map = sprites.bitmap_fix(path_in)
        this_map = np.left_shift(this_map[:, :, 0], 5) + np.left_shift(this_map[:, :, 1], 2) + this_map[:, :, 2]

        self.current_map = this_map
        self.map_x = np.size(self.current_map, 1)
        self.map_y = np.size(self.current_map, 0)
        
    def load_map_text(self, path_in):
        #self.current_map = np.loadtxt(path_in, dtype='uint8', delimiter=',')
        self.current_map = np.genfromtxt(path_in, dtype='float64', delimiter=',')
        if np.isnan(self.current_map[0, np.size(self.current_map, 1)-1]):
            self.current_map = self.current_map[0:np.size(self.current_map, 0), 0:np.size(self.current_map, 1)-1]
        self.current_map = np.uint8(self.current_map)
        self.map_x = np.size(self.current_map, 1)
        self.map_y = np.size(self.current_map, 0)
        
    def update_map_display(self):        
        total_map = np.zeros((self.map_y*sprites.sprite_y, self.map_x*sprites.sprite_x), dtype='uint8')
        for ii in range(0, self.map_x):
            for jj in range(0, self.map_y):
                this_sprite_index = self.current_map[jj, ii]
                #thing = total_spritesheet[(0*sprites.sprite_y):(0*sprites.sprite_y)+sprites.sprite_y-1, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x-1]
                total_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
        
        disp_map = np.zeros((np.size(total_map, 0), np.size(total_map, 1), 3), dtype='uint8')
        disp_map[:, :, 0] = ((np.right_shift(total_map, 5) & 7) / 7) * 255
        disp_map[:, :, 1] = ((np.right_shift(total_map, 2) & 7) / 7) * 255
        disp_map[:, :, 2] = ((total_map & 3) / 3) * 255
        
        # convert the array into a Image object
        im=Image.fromarray(disp_map, 'RGB')
        
        # set the starting point of the scroll
        width,height=im.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def update_map_image(self):
        total_map = np.zeros((self.map_y*sprites.sprite_y, self.map_x*sprites.sprite_x), dtype='uint8')
        for ii in range(0, self.map_x):
            for jj in range(0, self.map_y):
                this_sprite_index = self.current_map[jj, ii]
                #thing = total_spritesheet[(0*sprites.sprite_y):(0*sprites.sprite_y)+sprites.sprite_y-1, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x-1]
                total_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
        
        disp_map = np.zeros((np.size(total_map, 0), np.size(total_map, 1), 3), dtype='uint8')
        disp_map[:, :, 0] = ((np.right_shift(total_map, 5) & 7) / 7) * 255
        disp_map[:, :, 1] = ((np.right_shift(total_map, 2) & 7) / 7) * 255
        disp_map[:, :, 2] = ((total_map & 3) / 3) * 255
        
        # convert the array into a Image object
        im=Image.fromarray(disp_map, 'RGB')
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        self.canvas.itemconfig(self.imgtag, image=self.im2)

class MapDropDown(tk.Frame):
    def __init__(self, root, bitmap_path, textmap_path):
        tk.Frame.__init__(self, root)
        
        #map_out_list = sorted(glob.glob("%s%s" % ("/home/pi/Documents/mbed_Graphics/output_maps", "/*.out")))

        self.bitmap_path = bitmap_path
        self.textmap_path = textmap_path

        self.choice = tk.StringVar()

        self.option = tk.OptionMenu(root, self.choice, [])
        self.option.pack()
        self.option.config(width=20)
        
        self.clear_list()
        
    def load_bitmap_maps(self):
        map_bmp_list = sorted(glob.glob("%s%s" % (self.bitmap_path, "/*.bmp")))
        # prepare a Series
        s = pd.Series()
        # For each .bmp found add it's filename and path+filename to the Series
        for this_map in map_bmp_list:
            n = re.split(r"/", this_map)
            filename = n[-1]
            s2 = pd.Series(this_map, index=[filename])
            s = s.append(s2)
        # store the current Series
        self.map_series = self.map_series.append(s)
        # force the list of maps to update
        self.update_list(self.map_series.index)
        
    def load_text_maps(self):
        map_out_list = sorted(glob.glob("%s%s" % (self.textmap_path, "/*.out")))
        s = pd.Series()
        for this_map in map_out_list:
            n = re.split(r"/", this_map)
            filename = n[-1]
            s2 = pd.Series(this_map, index=[filename])
            s = s.append(s2)
            #m = re.search(r"[0-9].out", this_map)
            #if m is not None:
                #n = re.split(r"/", this_map)
                #filename = n[-1]
                #s2 = pd.Series(this_map, index=[filename])
                #s = s.append(s2)
        self.map_series = self.map_series.append(s)
        self.update_list(self.map_series.index)
        
    def clear_list(self):
        # clears the drop down list
        self.option['menu'].delete(0, 'end')
        s = pd.Series()
        self.map_series = s
        
    def update_list(self, new_entries):
        self.option['menu'].delete(0, 'end')
        choices = self.map_series.index
        self.choice.set(choices[0])
        for choice in choices:
            self.option['menu'].add_command(label=choice, command=tk._setit(self.choice, choice))
            
    def get_selection(self):
        return self.map_series.get(self.choice.get())
  
def load_map(inp):
    this_sel = inp.get_selection()
    n = re.split(r"\.", this_sel)
    fileexten = n[-1]
    if "bmp" in fileexten:
        map_panel.load_map_bitmap(this_sel)
    if "out" in fileexten:
        map_panel.load_map_text(this_sel)
    map_panel.update_map_display()
    
def save_map(inp):
    # remove the dot at the end
    n = re.split(r"\.", e.get())
    this_sel = n[0]
    inp.textmap_path
    np.savetxt(inp.textmap_path + "/" + this_sel + ".out", map_panel.current_map, delimiter=',',fmt='%i',newline=',\n')
    
def refresh_map(inp):
    inp.clear_list()
    inp.load_bitmap_maps()
    inp.load_text_maps()
    
def create_map(inp):
    x = np.uint8(e1.get())
    y = np.uint8(e2.get())
    map_panel.map_x = x
    map_panel.map_y = y
    map_panel.generate_map()
    map_panel.current_map = map_panel.current_map * map_panel.handle_SpritePanel.selected_sprite
    map_panel.update_map_display()

# create window instance
root = tk.Tk()
root.geometry("800x600") #You want the size of the app to be 500x500
root.resizable(0, 0) #Don't allow resizing in the x or y direction
#root.columnconfigure(0, weight=1)
#root.rowconfigure(0, weight=1)

# frame layout on grids
map_frame = tk.Frame(master=root, bd=1, bg="red")
map_frame.grid(row=0, column=0, sticky="nw")
map_frame_buttons = tk.Frame(master=root, bd=1, bg="green")
map_frame_buttons.grid(row=0, column=1, sticky="nw")
map_frame01 = tk.Frame(master=map_frame_buttons)
map_frame01.grid(row=0, column=0, columnspan=2, sticky="nw")
map_frame02 = tk.Frame(master=map_frame_buttons)
map_frame02.grid(row=1, column=0, columnspan=2, sticky="nw")
map_frame03 = tk.Frame(master=map_frame_buttons)
map_frame03.grid(row=2, column=0, columnspan=2, sticky="nw")
map_frame04 = tk.Frame(master=map_frame_buttons)
map_frame04.grid(row=3, column=0, columnspan=2, sticky="nw")
map_frame05 = tk.Frame(master=map_frame_buttons)
map_frame05.grid(row=4, column=0, columnspan=2, sticky="nw")
map_frame06 = tk.Frame(master=map_frame_buttons)
map_frame06.grid(row=5, column=0, columnspan=1, sticky="nw")
map_frame07 = tk.Frame(master=map_frame_buttons)
map_frame07.grid(row=5, column=1, columnspan=1,  sticky="nw")
map_frame08 = tk.Frame(master=map_frame_buttons)
map_frame08.grid(row=6, column=0, columnspan=2,  sticky="nw")
sprite_frame = tk.Frame(master=root)
sprite_frame.grid(row=1, column=0)

# handle, n_rows, sprite_scaling, show_x_sprites, show_y_sprites
sprite_panel = SpritePanel(sprite_frame, "/home/pi/Documents/mbed_Graphics/bitmap_sprites", 7, 4, 3, 3)
map_panel = MapPanel(map_frame, sprite_panel)
map_panel.set_sprite_path("/home/pi/Documents/mbed_Graphics/bitmap_sprites")
map_panel.load_sprite_sheet()
#map_panel.load_map_bitmap("/home/pi/Documents/mbed_Graphics/bitmap_maps/room_005.bmp")
#map_panel.load_map_text("/home/pi/Documents/mbed_Graphics/output_maps/map004.out")
#map_panel.update_map_display()

map_panel_dropdown = MapDropDown(map_frame01, "/home/pi/Documents/mbed_Graphics/bitmap_maps", "/home/pi/Documents/mbed_Graphics/output_maps")
map_panel_dropdown.load_bitmap_maps()
map_panel_dropdown.load_text_maps()

b_load = tk.Button(map_frame02, text="Load", command=lambda: load_map(map_panel_dropdown))
b_load.pack()
b_save = tk.Button(map_frame03, text="Save", command=lambda: save_map(map_panel_dropdown))
b_save.pack()
b_refresh = tk.Button(map_frame04, text="Refresh", command=lambda: refresh_map(map_panel_dropdown))
b_refresh.pack()
b_empty = tk.Button(map_frame08, text="Create", command=lambda: create_map(map_panel_dropdown))
b_empty.pack()

e = tk.Entry(map_frame05, textvariable=map_panel_dropdown.choice, width=25)
e.pack()
e1 = tk.Entry(map_frame06, width=12)
e1.insert(0, "0")
e1.pack()
e2 = tk.Entry(map_frame07, width=12)
e2.insert(0, "0")
e2.pack()

#e.delete(0)
#e.insert(0, map_panel_dropdown.choice.get())

#map_out_list = sorted(glob.glob("%s%s" % ("/home/pi/Documents/mbed_Graphics/output_maps", "/*.out")))
#for ii in map_out_list:
#    n = re.search(r"[0-9].out", ii)
#    if n is not None:
#        print(n)

# display the window
root.update()
root.mainloop()

