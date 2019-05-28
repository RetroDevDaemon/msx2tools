#########################################################
# MSX2 Bitmapper
#
# (c) 2019 Ben Ferguson
#  (w/contributions from jlbeard83)
# Use Python 3! (Coded in 3.7.1)
# 
# v1.0: Initial release
#           
# Assembles z80 byte data for GRAPHIC4-7 (SCREEN5-8)
#  bitmap graphics for use with compilers.
# Easy point-and-click interface.
# 
##########################################################

import tkinter as tk 
import sys 
import math 
import os 
import zipfile 
# before anything else:


# define TK
app = tk.Tk()

graphics_mode_width = 256
graphics_mode_192 = 192
graphics_mode_212 = 212
graphics_mode_height = graphics_mode_192
app_scale = 1
zoom_scale = 1
screen_data = []
screen_pixels = []
y_ratio = (3/4)
graphic_mode = 'G4'
draw_mode = 'PX'
selector_rect = None
# 'LINE', 'CIRCLE', 'SQUARE', 'SELECT'

###### BIT MAP DATA #######
dotdata = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x00, 0x10, 0x00, 0x28, 0x00, 0x5c, 0x00, 0x2e, 0x00, 0x17, 0x80, 0x0b, 0xc0, 0x05, 0xe0, 0x02, 0x70, 0x01, 0xb8, 0x00, 0x54, 0x00, 0x24, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00
};
"""

scale_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0xff, 0x00, 0xff, 0x01, 0x83, 0x00, 0x81, 0x08, 0x85, 0x00, 0xff, 0x40, 0xf8, 0xff, 0xf8, 0xff, 0xf8, 0xff, 0x08, 0x80, 0x08, 0x80, 0x08, 0x80, 0x08, 0x80, 0x08, 0x80, 0x08, 0x80, 0xf8, 0xff
};
"""

zoom1_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xf0, 0x00, 0xf8, 0x01, 0x0c, 0x03, 0x36, 0x06, 0x16, 0x06, 0x06, 0x06, 0x06, 0x06, 0x0c, 0x03, 0xf8, 0x07, 0xf4, 0x0e, 0x06, 0x1c, 0x04, 0x38, 0xa4, 0x70, 0x44, 0xe0, 0xae, 0xc0
};
"""

zoom2_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xf0, 0x00, 0xf8, 0x01, 0x0c, 0x03, 0x36, 0x06, 0x16, 0x06, 0x06, 0x06, 0x06, 0x06, 0x0c, 0x03, 0xf8, 0x07, 0xfe, 0x0e, 0x09, 0x1c, 0x08, 0x38, 0xa4, 0xc0, 0x42, 0xe0, 0xaf, 0xc0
};
"""

zoom4_icon_data= """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xf0, 0x00, 0xf8, 0x01, 0x0c, 0x03, 0x36, 0x06, 0x16, 0x06, 0x06, 0x06, 0x06, 0x06, 0x0c, 0x03, 0xf8, 0x07, 0xf1, 0x0e, 0x09, 0x1c, 0x0f, 0x38, 0xa8, 0x70, 0x48, 0xe0, 0xa8, 0xc0
};
"""

zoom8_icon_data= """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xf0, 0x00, 0xf8, 0x01, 0x0c, 0x03, 0x36, 0x06, 0x16, 0x06, 0x06, 0x06, 0x06, 0x06, 0x0c, 0x03, 0xf8, 0x07, 0xf6, 0x0e, 0x09, 0x1c, 0x06, 0x38, 0xa9, 0x70, 0x49, 0xe0, 0xa6, 0xc0
};
"""

line_icon_data= """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x14, 0x00, 0x08, 0x00, 0x14, 0x00, 0x20, 0x00, 0x40, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x04, 0x00, 0x08, 0x00, 0x50, 0x00, 0x20, 0x00, 0x50, 0x00, 0x00, 0x00, 0x00,
};
"""

circle_icon_data= """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xe0, 0x07, 0x10, 0x08, 0x08, 0x10, 0x04, 0x28, 0x02, 0x44, 0x02, 0x42, 0x82, 0x41, 0x82, 0x41, 0x02, 0x40, 0x04, 0x20, 0x08, 0x10, 0x10, 0x08, 0xe0, 0x07, 0x00, 0x00, 0x00, 0x00
};
"""
rect_icon_data= """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xfe, 0x3f, 0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x02, 0x20, 0x82, 0x7f, 0x82, 0x40, 0x82, 0x40, 0xfe, 0x40, 0x80, 0x40, 0xfc, 0x43, 0x04, 0x42, 0x04, 0x7e, 0xfc, 0x03, 0x00, 0x00
};
"""

select_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00,0x00, 0x00, 0x54, 0x15,0x00, 0x20,
0x04, 0x00,0x00, 0x20, 0x04, 0x00,0x00, 0x20,
0x04, 0x00,0x00, 0x20, 0x04, 0x00,0x00, 0x20,
0x04, 0x00,0xa8, 0x2a, 0x00, 0x00,0x00, 0x00
};
"""
cut_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x80, 0x00, 0x80, 0x01, 0x80, 0x02, 0x80, 0x02, 0x80, 0x02, 0x80, 0x02, 0x80, 0x32, 0x80, 0x7a, 0xff, 0xcf, 0x82, 0xce, 0xfc, 0xcb, 0x80, 0x31, 0xc0, 0x03, 0x60, 0x06, 0x60, 0x06, 0xc0, 0x03
};
"""
copy_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0xf8, 0x00, 0xac, 0x01, 0x56, 0x03, 0xab, 0x06, 0x55, 0x05, 0xab, 0x1f, 0xd5, 0x20, 0x6b, 0x40, 0x36, 0x80, 0x2c, 0x80, 0x38, 0x80, 0x20, 0x80, 0x20, 0x80, 0x40, 0x40, 0x80, 0x20, 0x00, 0x1f
};
"""
paste_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x01, 0x80, 0x01, 0x80, 0x01, 0xc0, 0x02, 0xe0, 0x05, 0x20, 0x05, 0xe0, 0x0c, 0x10, 0x09, 0x08, 0x16, 0xe8, 0x17, 0x28, 0x14, 0x28, 0x14, 0xe8, 0x17, 0x08, 0x10, 0x08, 0x10, 0xf0, 0x0f
};
"""
undo_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x40, 0x00, 0x60, 0x00, 0xf0, 0x0f, 0xf8, 0x1f, 0xf0, 0x3f, 0x60, 0x38, 0x40, 0x30, 0x00, 0x30, 0x00, 0x30, 0x00, 0x18, 0x00, 0x0c, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};
"""
redo_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x00, 0x02, 0x00, 0x06, 0xf0, 0x0b, 0x08, 0x10, 0xf4, 0x0b, 0x14, 0x06, 0x0c, 0x02, 0x0c, 0x00, 0x0c, 0x00, 0x18, 0x00, 0x30, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};
"""
save_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xfc, 0x3f, 0x1e, 0x78, 0x5e, 0x78, 0x5e, 0x78, 0x1e, 0x78, 0xfe, 0x7f, 0xfe, 0x7f, 0x7e, 0x7e, 0xbe, 0x7d, 0xbe, 0x7c, 0x7e, 0x7e, 0xfe, 0x7f, 0xfe, 0x6f, 0xfc, 0x3f, 0x00, 0x00
};
"""

dotbmp = tk.BitmapImage(data=dotdata)
scale_icon = tk.BitmapImage(data=scale_icon_data)
zoom1_icon = tk.BitmapImage(data=zoom1_icon_data)
zoom2_icon = tk.BitmapImage(data=zoom2_icon_data)
zoom4_icon = tk.BitmapImage(data=zoom4_icon_data)
zoom8_icon = tk.BitmapImage(data=zoom8_icon_data)
line_icon = tk.BitmapImage(data=line_icon_data)
circle_icon = tk.BitmapImage(data=circle_icon_data)
rect_icon = tk.BitmapImage(data=rect_icon_data)
select_icon = tk.BitmapImage(data=select_icon_data)
cut_icon = tk.BitmapImage(data=cut_icon_data)
copy_icon = tk.BitmapImage(data=copy_icon_data)
paste_icon = tk.BitmapImage(data=paste_icon_data)
undo_icon = tk.BitmapImage(data=undo_icon_data)
redo_icon = tk.BitmapImage(data=redo_icon_data)
save_icon = tk.BitmapImage(data=save_icon_data)

# init screen data
def init_screen_data(mode='G4', expanded=False):
    global screen_data
    global graphics_mode_width
    global graphics_mode_height 
    global graphics_mode_192 
    global graphics_mode_212 
    global y_ratio
    global graphic_mode
    graphic_mode = mode 
    if (mode == 'G4') or (mode == 'G7'):
        graphics_mode_width = 256
        y_ratio = 1
    elif (mode == 'G5') or (mode == 'G6'):
        graphics_mode_width = 512
        y_ratio = 2
    if expanded == False:
        graphics_mode_height = graphics_mode_192 
    else:
        graphics_mode_height = graphics_mode_212
    
    screen_data = []
    i = 0
    while i < (graphics_mode_width*graphics_mode_height):
        if mode != 'G7':
            screen_data.append(0)
        else:
            screen_data.append('#000')
        i += 1

grid_lines=[]

def init_canvas_grid():
    global drawCanvas 
    global app_scale 
    global zoom_scale 
    global grid_lines
    grid_lines=[]
    w = (app_scale*zoom_scale)
    h = (app_scale*zoom_scale)*y_ratio 
    y2 = (app_scale*zoom_scale*graphics_mode_height)*y_ratio
    l = graphics_mode_width
    i = 0
    if (app_scale + zoom_scale) <= 4:
        fill = ''
    else:
        fill = '#333'
    while i < l:
        p = drawCanvas.create_line(i*w, 0, i*w, y2, fill=fill)
        grid_lines.append(p)
        i += 1
    l = graphics_mode_height 
    x2 = (app_scale*zoom_scale*graphics_mode_width)
    i = 0
    while i < l:
        p = drawCanvas.create_line(0, i*h, x2, i*h, fill=fill)
        grid_lines.append(p)
        i += 1
    return

def update_canvas_grid():
    global drawCanvas 
    global app_scale 
    global zoom_scale 
    global grid_lines 
    w = (app_scale*zoom_scale)
    h = (app_scale*zoom_scale)*y_ratio
    y2 = (app_scale*zoom_scale*graphics_mode_height)*y_ratio
    l = graphics_mode_width 
    i = 0
    while i < l:
        drawCanvas.coords(grid_lines[i], i*w, 0, i*w, y2)
        if (app_scale + zoom_scale <= 4):
            drawCanvas.itemconfig(grid_lines[i], fill='')
        else:
            drawCanvas.itemconfig(grid_lines[i], fill='#333')
        i += 1
    #i = 0
    l = graphics_mode_height 
    x2 = (app_scale*zoom_scale*graphics_mode_width)
    i = 0
    while i < l:
        drawCanvas.coords(grid_lines[i+graphics_mode_width], 0, i*h, x2, i*h)
        if (app_scale + zoom_scale <= 4):
            drawCanvas.itemconfig(grid_lines[i+graphics_mode_width], fill='')
        else:
            drawCanvas.itemconfig(grid_lines[i+graphics_mode_width], fill='#333')
        i += 1
    return

# define base window dimensions
#app.config(background='black')

win = tk.Frame(master=app)
win.grid(row=0, column=0)

class drawFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

d = drawFrame(win, padx=20, pady=20, width=256*app_scale, height=graphics_mode_height*app_scale*y_ratio)#, background='black')
d.grid(row = 1, column=1, rowspan=20, columnspan=20, sticky='w')
drawCanvas = tk.Canvas(d, width=256*app_scale, height=graphics_mode_height*app_scale*y_ratio, background='black', scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
drawCanvas.grid(row=1, column=1, rowspan=20, columnspan=20, sticky='w')
d.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale)

draw_scroll_y = tk.Scrollbar(d, orient=tk.VERTICAL, command=drawCanvas.yview)
draw_scroll_y.grid(row=1, rowspan=20, column=21, sticky='ns')
draw_scroll_x = tk.Scrollbar(d, orient=tk.HORIZONTAL, command=drawCanvas.xview)
draw_scroll_x.grid(row=21, column=1, columnspan=20, sticky='ew')

drawCanvas.config(xscrollcommand=draw_scroll_x.set, yscrollcommand=draw_scroll_y.set)


def unclick_all():
    b = 0
    while b < len(palette_display):
        palette_display[b].unclicked()
        b += 1

if graphic_mode == 'G4' or graphic_mode == 'G7':
    scale = 15*app_scale
else:
    scale = 30*app_scale

palette_display = []
palwin = None 
if palwin:
    palwin.mainloop()

def find_and_replace(num, oldc, newc):
    print('Replacing palette number ' + str(num) + '. (Old: ' + oldc + ', new: ' + newc + ')')
    global screen_data
    global screen_pixels
    global drawCanvas
    i = 0
    while i < len(screen_data):
        if screen_data[i] == num:
            drawCanvas.itemconfig(screen_pixels[i], fill=newc)
        i += 1


class palwin_popup(tk.Tk):
    def __init__(self, col):
        if col == -1:
            return
        super().__init__()
        global app_scale 
        global graphic_mode
        if graphic_mode == 'G7':
            myw = 128
        else:
            myw = 256
        self.myscale = app_scale * 8
        self.palnum = col 
        global palette_display
        palette_display[self.palnum].clicked(0)
        self.overrideredirect(1)
        self.move_to_mouse()
        self.frame = tk.Frame(master=self,width=myw*self.myscale, height=128*self.myscale, background='black')
        self.frame.grid(row=0,column=0)
        self.canvas = tk.Canvas(self.frame, background='black',width=myw*self.myscale, height=128*self.myscale)
        self.canvas.grid(row=0,column=0)
        self.populate_colors()
        self.bind("<Button-1>", self.clicked_color)
        
    def clicked_color(self,o):
        x = math.floor(o.x/(self.myscale))
        y = math.floor(o.y/self.myscale)
        global palette_display
        global graphic_mode
        global selected_palette_no
        global hex_palette
        if graphic_mode != 'G7':
            find_and_replace(self.palnum, palette_display[self.palnum].myVal, self.colors[(y*32)+x])
            palette_display[self.palnum].setVal(self.colors[(y*32)+x])
            hex_palette[selected_palette_no] = palette_display[self.palnum].myVal
        else:
            palette_display[self.palnum].setVal(self.colors[(y*16)+x])
            hex_palette[selected_palette_no] = palette_display[self.palnum].myVal
        self.withdraw()
        

    def mainloop(self):
        super().mainloop()

    def populate_colors(self):
        self.colors=[]
        self.coloricons=[]
        global graphic_mode
        if graphic_mode == 'G7':
            blues = 4
            prows = 16
        else:
            blues = 8
            prows = 32
        c1 = 0
        while c1 < 8:
            c2 = 0
            while c2 < 8:
                c3 = 0
                while c3 < blues: #0/2/4/7/9/A/C/F
                    a = math.floor((c1/7)*15 )
                    b = math.floor((c2/7)*15)
                    if blues == 4:
                        m = 2
                    else:
                        m = 1
                    if c3 != 3:
                        c = math.floor(((c3*m)/7)*15)
                    else:
                        c = 15
                    self.colors.append('#'+format(a,'1x') + format(b,'1x')+format(c,'1x'))
                    c3 +=1
                c2 += 1
            c1 += 1
        # now put them on the window
        #global app_scale
        self.canvas.delete("all")
        s = self.myscale
        t = 0
        j = 0
        while j < 16:
            i = 0
            while i < prows:
                f = self.colors[t]
                self.coloricons.append(self.canvas.create_rectangle(i*s, j*s, (i*s)+s, (j*s)+s, fill=f))
                t += 1
                i += 1
            j += 1

    def resize(self):
        if self.state() == 'withdrawn':
            self.deiconify()
        global app_scale
        self.myscale = app_scale * 8
        global graphic_mode 
        if graphic_mode == 'G7':
            myw = 16
        else: 
            myw = 32
        s = self.myscale
        j = 0
        while j < 16:
            i = 0
            while i < myw:
                self.canvas.coords(self.coloricons[(j*myw)+i], i*s, j*s, (i*s)+s, (j*s)+s)
                i += 1
            j += 1

    def change_palnum(self, col):
        self.palnum = col 
        global palette_display
        palette_display[self.palnum].clicked(0)
        self.resize()
        self.move_to_mouse()
    
    def move_to_mouse(self):
        global app
        x,y=app.winfo_pointerxy()
        global graphic_mode
        if graphic_mode == 'G7':
            myw = 16
        else:
            myw = 32
        pos=[self.myscale*myw, self.myscale*16, x+5, y+5]
        sx = app.winfo_screenwidth()
        sy = app.winfo_screenheight()
        if ((pos[0] + pos[2]) > sx):
            pos[2] = sx-pos[0]
        if ((pos[1]+pos[3])>sy): # width + x
            pos[3] = sy-pos[1]
        self.geometry('%dx%d+%d+%d' % (pos[0], pos[1], pos[2], pos[3]))


class PaletteButton(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.lbl = 0
        self.lbl2 = 0
        self.swapping = False
        self.selector=[]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.clicked)
        self.bind("<Button-3>", self.open_palette)

    def open_palette(self, event):
        i = 0
        col = -1
        while i < len(palette_display):
            if palette_display[i] == self:
                col = i 
                break 
            i += 1
        global selected_palette_no
        selected_palette_no = col 
        global palwin 
        if palwin == None:
            palwin = palwin_popup(col)
        else:
            palwin.deiconify()
            palwin.change_palnum(col)
            
    def on_enter(self, event):
        self.delete(self.lbl)
        self.delete(self.lbl2)
        self.lbl2 = self.create_text(17, 17, text=self.myVal, fill='white')
        self.lbl = self.create_text(16, 16, text=self.myVal)
            
    def on_leave(self, enter):
        self.delete(self.lbl)
        self.delete(self.lbl2)
    
    def setVal(self, num):
        self.myVal = num
        #global hex_palette
        #hex_palette[selected_palette_no] = self.myVal
        self.config(background=self.myVal)

    def unclicked(self):
        b = 0
        while b < len(self.selector):
            self.delete(self.selector[b])
            b += 1

    def clicked(self, event):
        unclick_all()
        self.selector.append(self.create_line(2, 2, scale, 2, width=3, fill='yellow'))
        self.selector.append(self.create_line(2, 2, 2, scale, width=3, fill='yellow'))
        self.selector.append(self.create_line(5, scale, scale, scale, width=3, fill='yellow'))
        self.selector.append(self.create_line(scale, 5, scale, scale, width=3, fill='yellow'))
        i = 0
        global selected_palette_no
        while i < len(palette_display):
            if palette_display[i] == self:
                selected_palette_no = i
                break
            i += 1
        global palwin
        if palwin:
            if palwin.state() == "normal":
                palwin.withdraw()
         #
 #

selected_palette_no = 15
hex_palette = [ '#000', '#000', '#2C2', '#6F6',
 '#22F', '#46F', '#A22', '#4CF',
 '#F22', '#F66', '#CC2', '#CC8',
 '#282', '#C4A', '#AAA', '#FFF' ]
 #0/2/4/6/8/A/C/F

palette_display = []

i = 0
while i < 16:
    palette_display.append(PaletteButton(win, width=scale, height=scale, background=hex_palette[i]))
    i += 1

def add_palette_display():
    global palette_display
    global scale 
    global hex_palette
    global graphic_mode
    global win 
    if graphic_mode != 'G5':
        palnums = 16
    else:
        palnums = 4
    i = 0
    while i < len(palette_display):
        if palette_display[i]:
            palette_display[i].grid_forget()
        i += 1
    i = 0
    while i < palnums:
        palette_display[i].grid(row=i + 1, column=32, sticky='w')
        palette_display[i].setVal(hex_palette[i])
        i += 1
    
def rescale_palette():
    global palette_display
    global scale
    global win 
    global selected_palette_no
    global graphic_mode
    if graphic_mode == 'G4' or graphic_mode == 'G7':
        scale = 12*app_scale
    else:
        scale = 24*app_scale
    scale = int(scale)
    i = 0
    while i < len(palette_display):
        palette_display[i].config(width=scale, height=scale)
        i += 1
    palette_display[selected_palette_no].clicked(0)

def init_screen_pixels():
    global screen_pixels
    global drawCanvas
    global app_scale 
    global zoom_scale 
    global screen_data
    if palwin:
        palwin.populate_colors()
        palwin.withdraw()
    screen_pixels = []
    drawCanvas.delete("all")
    l = len(screen_data)
    i = 0
    w = (app_scale*zoom_scale)
    h = (app_scale*zoom_scale)*y_ratio
    while i < l:
        # draw every pixel to the canvas, and append its reference to the array.
        xp = i % graphics_mode_width
        xp = xp * app_scale * zoom_scale
        yp = math.floor(i/graphics_mode_width)
        yp = yp * app_scale * zoom_scale * y_ratio
        # x pos is (l % graphics_mode_width)*
        p = drawCanvas.create_rectangle(xp, yp, xp+w, yp+h, outline='')
        screen_pixels.append(p)
        i += 1
    init_canvas_grid()
    add_palette_display()

def reset_screen_pixels():
    global screen_data
    global drawCanvas
    global screen_pixels
    global hex_palette
    l = len(screen_data)
    i = 0
    while i < l:
        drawCanvas.itemconfig(screen_pixels[i], fill=hex_palette[0])
        i += 1

lastpx = (-1,-1)

def clicked_loc(o):
    global drawCanvas 
    global app_scale 
    global zoom_scale
    global lastpx  
    scr_x = draw_scroll_x.get() 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])  # should be 1:1 px left bounding
    scale = app_scale*zoom_scale
    px = math.floor((xofs+o.x) / scale)
    scr_y = draw_scroll_y.get()
    yofs = scr_y[0] * float(fscr[3])
    py = math.floor((yofs + o.y) / (scale*y_ratio))
    if (px,py) != lastpx:
        lastpx = (px, py)
        color_pixel(px, py)

scroll_orig = (0,0)

def set_scroll_orig(o):
    global drawCanvas 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    global scroll_orig
    scroll_orig = (o.x, o.y)
    return scroll_orig

new_scrollbarpos = (0,0)

class xypos(object):
    def __init__(self, x, y):
        self.x = x 
        self.y = y 

def set_drawwindow_pos(o):
    global drawCanvas 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    scr_rt = o.x / float(fscr[2])
    scr_rty = o.y / float(fscr[3])
    drawCanvas.xview(tk.MOVETO, scr_rt)
    drawCanvas.yview(tk.MOVETO, scr_rty)
    
def scroll_drawwindow(o):
    global scroll_orig
    global drawCanvas
    global zoom_scale
    if zoom_scale == 1:
        return
    xo = o.x - scroll_orig[0]
    yo = o.y - scroll_orig[1]
    scr_x = draw_scroll_x.get()
    scr_y = draw_scroll_y.get() 
    if (scr_x[0] == 0) and (xo > 0):
        # cant scroll left any more
        xo = 0
    if (scr_y[0] == 0) and (yo > 0):
        yo = 0 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])
    yofs = scr_y[0] * float(fscr[3])
    xo = (-1*xo)+xofs
    yo = (-1*yo)+yofs
    if xo < 0:
        xo = 0
    if yo < 0:
        yo = 0
    if xo > (float(fscr[2]) - drawCanvas.winfo_width()):
        xo = float(fscr[2])
    if yo > (float(fscr[3]) - drawCanvas.winfo_height()):
        yo = float(fscr[3])
    # ^^^^ THIS IS ALL GOOD!
    # # what we want is to set the left most bounding of the screen
    # # to xo + xofs. 
    scr_rt = xo / float(fscr[2])
    scr_rty = yo / float(fscr[3])
    drawCanvas.xview(tk.MOVETO, scr_rt)
    drawCanvas.yview(tk.MOVETO, scr_rty)
    scroll_orig = set_scroll_orig(o)
    return


max_scale = True

def toggle_scale(scale=1):
    #used in 'd' and 'drawCanvas'
    sx = app.winfo_screenwidth()
    sy = app.winfo_screenheight()
    global max_scale
    global app_scale 
    global graphic_mode 
    tscale = app_scale + 1
    if graphic_mode == 'G4' or graphic_mode == 'G7':
        ys = 30
        tscale = app_scale+1
    else:
        ys = 50
    if max_scale == True:
        app_scale = 1
        tscale = 1
        max_scale = False 
    if (graphics_mode_height*tscale*y_ratio)+(ys*tscale)+60 > sy:
        #print('broke y')
        app_scale = sy/(((graphics_mode_height*y_ratio)+60)+ys)
        max_scale = True
    elif (graphics_mode_width*tscale)+(160*tscale) > sx:
        #print('broke x')
        app_scale = sx/((graphics_mode_width)+160)
        max_scale = True
    else:
        app_scale = tscale
    if app_scale == 1 and (graphic_mode == 'G4' or graphic_mode == 'G7'):
        app_scale = 2
    w = graphics_mode_width*app_scale
    h = graphics_mode_height*app_scale*y_ratio
    drawCanvas.config(width=w, height=h, scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
    zoom_screen_pixels()
    rescale_palette()
    x = int(sx/2)-int((w/2)) - 75
    y = int(sy/2)-int(h/2) - 120

    app.geometry('{}x{}+{}+{}'.format(int((graphics_mode_width*app_scale)+(160)), int((graphics_mode_height*app_scale*y_ratio)+(ys*app_scale)+60), x, y ))

def get_newzoom_offset(plusminus):
    global draw_scroll_x
    global draw_scroll_y
    global drawCanvas 
    global zoom_scale
    scr_x = draw_scroll_x.get()
    scr_y = draw_scroll_y.get() 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])
    yofs = scr_y[0] * float(fscr[3])
    # xofs and yofs give us the x/y offset of the canvas after zoom. on a normal zoom,
    # this is the top left corner (quarter) of the viewable window.
    if plusminus == '+':
        xofs += float(fscr[2])/(zoom_scale*2)
        yofs += float(fscr[3])/(zoom_scale*2)
    else:
        xofs -= drawCanvas.winfo_width()/4 #= 2048/2 * 4
        yofs -= drawCanvas.winfo_height()/4
    return xofs,yofs

def zoom_screen_pixels():
    global screen_pixels
    global drawCanvas
    global app_scale 
    global zoom_scale 
    global screen_data
    l = len(screen_data)
    w = (app_scale*zoom_scale)
    h = (app_scale*zoom_scale)*y_ratio
    i = 0
    while i < l:
        xp = i % graphics_mode_width
        xp = xp * app_scale * zoom_scale
        yp = math.floor(i/graphics_mode_width)
        yp = yp * app_scale * zoom_scale * y_ratio
        drawCanvas.coords(screen_pixels[i], xp, yp, xp+w, yp+h)
        i += 1
    global selector_rect
    if selector_rect != None:
        drawCanvas.delete(selector_rect)
        selector_rect = None
    update_canvas_grid()
   
zoomplusminus = '+'

def depress_zooms(z):
    global zoom1button
    global zoom2button 
    global zoom4button
    global zoom8button
    zoom1button.config(relief=tk.RAISED)
    zoom2button.config(relief=tk.RAISED)
    zoom4button.config(relief=tk.RAISED)
    zoom8button.config(relief=tk.RAISED)
    if z == 1:
        zoom1button.config(relief=tk.SUNKEN)
    elif z==2:
        zoom2button.config(relief=tk.SUNKEN)
    elif z==4:
        zoom4button.config(relief=tk.SUNKEN)
    elif z==8:
        zoom8button.config(relief=tk.SUNKEN)
def zoom_1x():
    global zoom_scale
    depress_zooms(1)
    if zoom_scale != 1:
        global zoomplusminus
        zoomplusminus = '-'
        toggle_zoom(1)
def zoom_2x():
    global zoom_scale
    depress_zooms(2)
    global zoomplusminus
    if zoom_scale > 2:
        zoomplusminus = '-'
    else:
        zoomplusminus = '+'
    if zoom_scale != 2:
        toggle_zoom(2)
def zoom_4x():
    global zoom_scale
    depress_zooms(4)
    global zoomplusminus
    if zoom_scale > 4:
        zoomplusminus = '-'
    else:
        zoomplusminus = '+'
    if zoom_scale != 4:
        toggle_zoom(4)
def zoom_8x():
    global zoom_scale
    depress_zooms(8)
    global zoomplusminus
    if zoom_scale > 8:
        zoomplusminus = '-'
    else:
        zoomplusminus = '+'
    if zoom_scale != 8:
        toggle_zoom(8)
def toggle_zoom(z=0):
    global zoom_scale
    if z==0:
        if zoom_scale == 2:
            zoom_scale = 4
        elif zoom_scale == 1:
            zoom_scale = 2
        elif zoom_scale == 4:
            zoom_scale = 8
        elif zoom_scale == 8:
            zoom_scale = 1
    else:
        zoom_scale = z
    drawCanvas.config(scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
    zoom_screen_pixels()
    global zoomplusminus
    newx, newy = get_newzoom_offset(zoomplusminus)
    set_drawwindow_pos(xypos(newx,newy))

brush_style = 'square'
button_held = False

def color_pixel(x, y, size=1):
    global drawCanvas
    global graphics_mode_width
    global graphics_mode_height
    if (x >= graphics_mode_width) or (y >= graphics_mode_height):
        return
    if (x < 0) or (y < 0):
        return
    global button_held
    if button_held == False:
        button_held = True
        set_undo_point()
    global screen_data
    global screen_pixels 
    global selected_palette_no
    global hex_palette
    tp = (y*graphics_mode_width) + x
    global graphic_mode
    if graphic_mode != 'G7':
        screen_data[tp] = selected_palette_no
    else:
        screen_data[tp] = hex_palette[selected_palette_no]
    drawCanvas.itemconfig(screen_pixels[tp], fill=hex_palette[selected_palette_no])
    global pxsize
    size = int(pxsize.get())
    if size < 1:
        size = 1
    elif size > 9:
        size = 9
    pxsize.delete(0,tk.END)
    pxsize.insert(0,size)
    if size > 1:
        #TODO: possible toggle for double-high brush size
        #TODO: possible toggle for diamond vs square 
        #atm only pixel-perfect square
        #brush_style = 'diamond'
        global brush_style
        if brush_style == 'square':
            size_loop = size - 1
            if size_loop % 2 == 0: #is pixel size odd?   
                tp_origin_y = y - ((size_loop)/2)
                tp_origin_x = x - ((size_loop)/2)
            else: #is pixel size even?
                tp_origin_y = y - ((size_loop-1)/2)
                tp_origin_x = x - ((size_loop-1)/2)
            paint_square_brush(size, tp_origin_y, tp_origin_x)
        elif brush_style == 'diamond':
            paint_diamond_brush(size, y, x)


def client_exit():
    a = tk.messagebox.askyesnocancel('Save?', message='Save current bitmap before\nquitting?')
    if a == True:
        save_normal()
        global m2bfilename
        if m2bfilename == '' or type(m2bfilename)==tuple:
            return
        sys.exit()
    elif a == False:
        sys.exit()
    elif a == None:
        return
    

def new_file(mode, expanded):
    global app_scale
    init_screen_data(mode=mode, expanded=expanded)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
    global m2bfilename
    m2bfilename = ''
    return

m2bfilename = ''

from tkinter import filedialog, messagebox

def save_normal():
    global m2bfilename 
    if m2bfilename == '':
        m2bfilename = tk.filedialog.asksaveasfilename(title='Save MSX2 Bitmapper file', filetypes=( ('MSX2 Bitmapper file', '*.m2b'),('All files', '*.*') ))
    if m2bfilename == '' or type(m2bfilename) == tuple:
        return
    if m2bfilename[-4:].upper() != '.M2B':
        m2bfilename = m2bfilename + '.m2b'
    save_bitmap()

def save_bitmap():
    global m2bfilename
    global graphic_mode
    global screen_pixels
    global graphics_mode_height
    global drawCanvas
    f = None 
    outbuffer = 'm2b'
    try:
        f = open(outbuffer, 'w')
        f.write(graphic_mode+'\n')
        f.write(str(graphics_mode_height)+'\n')
        for c in palette_display:
            f.write(str(c.myVal)+',')
        f.write('\n')
        if graphic_mode == 'G7':
            i = 0
            while i < len(screen_pixels):
                f.write(drawCanvas.itemcget(screen_pixels[i], 'fill') + ',')
                i += 1
        else:
            for c in screen_data:
                f.write(str(c)+',')
        f.close()
        with zipfile.ZipFile(m2bfilename, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(outbuffer)    
        tk.messagebox.showinfo('Save successful!', message='Bitmap file saved successfully.')
    except:
        tk.messagebox.showerror('Error', message='Error while saving file.')
    finally:
        #f.close()
        os.remove('m2b')

'''unlike refresh_entire_screen, this will only change pixels to reflect whats already in screen_data'''
def repaint_screen():
    global screen_data 
    global graphic_mode 
    global drawCanvas 
    global screen_pixels 
    global hex_palette 
    fsize = int(5*app_scale)
    ofs = get_canvas_offset()
    loadingt = drawCanvas.create_text(ofs[0]+40,ofs[1]+10, text='Refreshing...', fill='black', font=('Times New Roman',fsize))
    loadings = drawCanvas.create_text(ofs[0]+42,ofs[1]+12, text="Refreshing...", fill='white', font=('Times New Roman',fsize))
    drawCanvas.update_idletasks()
    i = 0
    while i < len(screen_data):
        if graphic_mode != 'G7':
            screen_data[i] = int(screen_data[i])
            drawCanvas.itemconfig(screen_pixels[i], fill=hex_palette[screen_data[i]])
        else:
            if screen_data[i] == '':
                screen_data[i] = '#000'
            drawCanvas.itemconfig(screen_pixels[i], fill=screen_data[i])
        i += 1
    drawCanvas.delete(loadingt)
    drawCanvas.delete(loadings)

'''this recreates the entire canvas, essentially'''
def refresh_entire_screen(exp, newdata):
    global graphic_mode
    global screen_data
    global graphics_mode_width
    global graphics_mode_height 
    global graphics_mode_192 
    global graphics_mode_212 
    global y_ratio
    global graphic_mode
    if (graphic_mode == 'G4') or (graphic_mode == 'G7'):
        graphics_mode_width = 256
        y_ratio = 1
    elif (graphic_mode == 'G5') or (graphic_mode == 'G6'):
        graphics_mode_width = 512
        y_ratio = 2
    if exp == False:
        graphics_mode_height = graphics_mode_192 
    else:
        graphics_mode_height = graphics_mode_212
    screen_data = list(newdata)
    init_screen_pixels()    # erases canvas and creates rectangles
    # now all we have to do is fill the rectangles!
    i = 0
    while i < len(screen_data):
        if graphic_mode != 'G7':
            screen_data[i] = int(screen_data[i])
            drawCanvas.itemconfig(screen_pixels[i], fill=hex_palette[screen_data[i]])
        else:
            if screen_data[i] == '':
                screen_data[i] = '#000'
            drawCanvas.itemconfig(screen_pixels[i], fill=screen_data[i])
        i += 1
    return

def load_m2b():
    global m2bfilename
    m2bfilename = ''
    global graphic_mode
    global graphics_mode_height
    global screen_data
    global palette_display
    f = None 
    z = None 
    zipped = False
    inbuffer = 'm2b'
    m2bfilename = tk.filedialog.askopenfilename(title='Load MSX2 Bitmapper file', filetypes=( ('MSX2 Bitmapper file', '*.m2b'),('All files', '*.*') ))
    if m2bfilename == '' or type(m2bfilename) == tuple:
        return 
    try: 
        if zipfile.is_zipfile(m2bfilename):
            zipped = True 
            z = zipfile.ZipFile(m2bfilename)
            f = z.open(inbuffer, 'r')
            gm = f.readline().decode("utf-8")
            pw = f.readline().decode("utf-8")
            pl = f.readline().decode("utf-8")
        else:
            f = open(m2bfilename, 'r')
            gm = f.readline()
            pw = f.readline()
            pl = f.readline()
        gm = gm[0:2]
        pw = pw[0:3]
        if (gm == 'G4') or (gm == 'G5') or (gm == 'G6') or (gm == 'G7'):
            graphic_mode = gm
        if (pw == 212):
            expanded = True 
        else:
            expanded = False
        pl = pl.split(',')
        pl.pop()
        global hex_palette
        i = 0
        while i < (len(pl)):
            hex_palette[i] = pl[i]
            i += 1
        add_palette_display()
        if not zipped:
            indata = f.readline()
        else:
            indata = f.readline().decode("utf-8")
        indata = indata.split(',')
        indata.pop()
        refresh_entire_screen(expanded, indata)
    except:
        tk.messagebox.showerror('Error loading', message='File could not be loaded.')
    finally:
        if (f):
            f.close()
        if(z):
            z.close()

drawing_line = None
line_startpos = (-1,-1)

def start_line(o):
    global drawing_line
    global drawCanvas
    global line_startpos
    global draw_scroll_x
    global draw_scroll_y
    global zoom_scale
    scr_x = draw_scroll_x.get()
    scr_y = draw_scroll_y.get() 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])
    yofs = scr_y[0] * float(fscr[3])
    line_startpos = (o.x+xofs, o.y+yofs)
    drawing_line = drawCanvas.create_line(line_startpos[0], line_startpos[1], line_startpos[0], line_startpos[1], fill='white')

def move_line(o):
    global drawing_line
    global drawCanvas
    global line_startpos
    global draw_scroll_x
    global draw_scroll_y
    global zoom_scale
    scr_x = draw_scroll_x.get()
    scr_y = draw_scroll_y.get() 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])
    yofs = scr_y[0] * float(fscr[3])
    drawCanvas.coords(drawing_line, line_startpos[0], line_startpos[1], o.x+xofs, o.y+yofs)

'''To use this generically, pass a new xypos class, and set globally line_startpos)'''

def paint_line(o, undo=True):
    global line_startpos 
    global drawing_line
    global drawCanvas
    global line_startpos
    global draw_scroll_x
    global draw_scroll_y
    global zoom_scale
    global graphics_mode_width
    global hex_palette
    global selected_palette_no
    global y_ratio
    if undo:
        set_undo_point()
    ofs = get_canvas_offset()
    line_endpos = (o.x+ofs[0], o.y+ofs[1])

    xpx_start = math.floor( line_startpos[0] / (zoom_scale*app_scale) )
    ypx_start = math.floor( line_startpos[1] / (zoom_scale*app_scale*y_ratio) )
    xpx_end = math.floor( line_endpos[0] / (zoom_scale*app_scale) )
    ypx_end = math.floor( line_endpos[1] / (zoom_scale*app_scale*y_ratio) )

    x_step = xpx_end - xpx_start
    y_step = ypx_end - ypx_start
    
    step_up = False 
    step_down = False
    step_left = False 
    step_right = False

    if x_step < 0:
        step_left = True
    elif x_step > 0:
        step_right = True

    if y_step < 0:
        step_up = True
    elif y_step > 0:
        step_down = True

    if step_up == False and step_down == False:
        # horizontal line

        if xpx_start > xpx_end:
            temp = xpx_start
            xpx_start = xpx_end
            xpx_end = temp

        cur_x = xpx_start
        cur_y = ypx_start

        # prevent traversal off of left of screen bounds
        if cur_x < 0:
            cur_x = 0

        while cur_x <= xpx_end:
            
            # prevent traversal off right of screen bounds
            if cur_x > (graphics_mode_width-1):
                break
            cur_index = (cur_y*graphics_mode_width)+cur_x
            draw_pixel_atindex(cur_index)

            cur_x += 1
    elif step_left == False and step_right == False:
        # vertical line

        if ypx_start > ypx_end:
            temp = ypx_start
            ypx_start = ypx_end
            ypx_end = temp

        cur_x = xpx_start
        cur_y = ypx_start

        # prevent traversal off top of screen bounds
        if cur_y < 0:
            cur_y = 0

        while cur_y <= ypx_end:
            
            current_index = (cur_y * graphics_mode_width) + cur_x

            # Prevent traversal off bottom of screen bounds
            if current_index > len(screen_pixels):
                break
            draw_pixel_atindex(current_index)
            
            cur_y += 1
    else:
        # angle of some sort

        if y_step != 0:
            step = x_step/y_step
        else:
            step = x_step

        if step < 0:
            step = step * -1 

        step_counter = 0

        cur_x = xpx_start
        cur_y = ypx_start

        while cur_x != xpx_end or cur_y != ypx_end:
            if step_counter < step:
                if cur_x != xpx_end:
                    if step_left:
                        cur_x -= 1
                    elif step_right:
                        cur_x += 1

                step_counter += 1
            if step_counter >= step:
                if cur_y != ypx_end:
                    if step_up:
                        cur_y -= 1
                    elif step_down:
                        cur_y += 1

                step_counter -= step

            # Check if off screen bounds
            current_index = (cur_y*graphics_mode_width)+cur_x
            if ((current_index > len(screen_pixels)) or (current_index < 0))\
                or (cur_y >= graphics_mode_height) or (cur_x >= graphics_mode_width)\
                    or (cur_y < 0) or (cur_x < 0):
                drawCanvas.delete(drawing_line)
                return
            draw_pixel_atindex(current_index)
            
    drawCanvas.delete(drawing_line)

def set_undo_released(o):
    global button_held
    button_held = False
    
def change_mode(mod):
    global pxbutton
    global linebutton
    global circlebutton
    global rectbutton
    global selectbutton
    global draw_mode
    global drawCanvas
    global draw_mode
    global selector_rect
    if selector_rect != None:
        drawCanvas.delete(selector_rect)
        #selector_rect = None
    draw_mode = mod
    drawCanvas.unbind("<ButtonRelease-3>")
    drawCanvas.unbind("<ButtonRelease-1>")
    drawCanvas.unbind("<Button-3>")
    drawCanvas.unbind("<Button-1>")
    drawCanvas.unbind("<B1-Motion>")
    drawCanvas.unbind("<B3-Motion>")
    global cutbutton 
    global copybutton 
    global pastebutton 
    cutbutton.config(state=tk.DISABLED)
    copybutton.config(state=tk.DISABLED)
    pastebutton.config(state=tk.DISABLED)
    pxbutton.config(relief=tk.RAISED)
    linebutton.config(relief=tk.RAISED)
    circlebutton.config(relief=tk.RAISED)
    rectbutton.config(relief=tk.RAISED)
    selectbutton.config(relief=tk.RAISED)
    global editMenu
    editMenu.entryconfigure(0, state=tk.DISABLED)
    editMenu.entryconfigure(1, state=tk.DISABLED)
    editMenu.entryconfigure(2, state=tk.DISABLED)
    #'LINE', 'CIRCLE', 'RECT', 'SELECT', 'PX'
    if mod=='LINE':
        linebutton.config(relief=tk.SUNKEN)
        drawCanvas.bind("<Button-1>", start_line)
        drawCanvas.bind("<B1-Motion>", move_line)
        drawCanvas.bind("<ButtonRelease-1>", paint_line)
        drawCanvas.bind("<Button-3>", set_scroll_orig)
        drawCanvas.bind("<B3-Motion>", scroll_drawwindow)
    elif mod=='CIRCLE':
        circlebutton.config(relief=tk.SUNKEN)
        drawCanvas.bind("<Button-1>", start_circle)
        drawCanvas.bind("<B1-Motion>", move_circle)
        drawCanvas.bind("<ButtonRelease-1>", paint_circle)
        drawCanvas.bind("<Button-3>", start_circle)
        drawCanvas.bind("<B3-Motion>", move_circle)
        drawCanvas.bind("<ButtonRelease-3>", paint_and_fill_circle)
    elif mod=='RECT':
        rectbutton.config(relief=tk.SUNKEN)
        drawCanvas.bind("<Button-1>", start_rect)
        drawCanvas.bind("<B1-Motion>", move_rect)
        drawCanvas.bind("<ButtonRelease-1>", paint_rect)
        drawCanvas.bind("<Button-3>", start_rect)
        drawCanvas.bind("<B3-Motion>", move_rect)
        drawCanvas.bind("<ButtonRelease-3>", paint_and_fill_rect)
    elif mod=='SELECT':
        selectbutton.config(relief=tk.SUNKEN)
        drawCanvas.bind("<Button-1>", start_select)
        drawCanvas.bind("<B1-Motion>", move_select)
        drawCanvas.bind("<Button-3>", set_scroll_orig)
        drawCanvas.bind("<B3-Motion>", scroll_drawwindow)
        editMenu.entryconfigure(0, state=tk.NORMAL)
        editMenu.entryconfigure(1, state=tk.NORMAL)
        editMenu.entryconfigure(2, state=tk.NORMAL)
        cutbutton.config(state=tk.NORMAL)
        copybutton.config(state=tk.NORMAL)
        pastebutton.config(state=tk.NORMAL)
    elif mod=='PX':
        pxbutton.config(relief=tk.SUNKEN)
        drawCanvas.bind("<Button-1>", clicked_loc)
        drawCanvas.bind("<B1-Motion>", clicked_loc)
        drawCanvas.bind("<ButtonRelease-1>", set_undo_released)
        drawCanvas.bind("<Button-3>", set_scroll_orig)
        drawCanvas.bind("<B3-Motion>", scroll_drawwindow)


def export_pal_data():
    asmpalfile = ''
    asmpalfile = tk.filedialog.asksaveasfilename(title='Save MSX2 palette z80 data', filetypes=( ('z80 assembly data', '*.z80'), ('z80 assembly data', '*.Z80'), ('All files', '*.*')))
    if asmpalfile == '' or type(asmpalfile)==tuple:
        return 
    if asmpalfile[-4:].upper() != '.Z80':
        asmpalfile = asmpalfile + '.z80'
    outdata = []
    outdata.append('; Palette data made with MSX2 Spriter\n')
    outdata.append(';  Write in sequence to R#16!')
    global palette_display
    i = 0
    while i < 16:
        # byte 1 = '0RRR0BBB'
        # byte 2 = '00000GGG'
        #print(palette_display[i].myVal[1:2])
        ob1 = format(math.floor(int(palette_display[i].myVal[1:2],16)/2),'03b')
        ob2 = format(math.floor(int(palette_display[i].myVal[2:3],16)/2),'03b')
        ob3 = format(math.floor(int(palette_display[i].myVal[3:4],16)/2),'03b')
        b1 = '0' + ob1 + '0' + ob3
        b2 = '00000' + ob2
        b1 = format(int(b1,2), '02x')
        b2 = format(int(b2,2), '02x')
        if i % 4 == 0:
            outdata.append('\n DB ')
        outdata.append(' ${}, ${},'.format(b1, b2))
        i += 1
        # Disgusting, but manually erase the commas
    outdata[6] = outdata[6][:-1]
    outdata[11] = outdata[11][:-1]
    outdata[16] = outdata[16][:-1]
    outdata = ''.join(outdata)[:-1]
    f = None 
    try:
        f = open(asmpalfile, 'w')
        for s in outdata:
            f.write(s)
        messagebox.showinfo('Save OK', message='Palette export successful!')
    except:
        messagebox.showerror('Error', message='Export failed.')
    finally:
        f.close()

def export_z80():
    asmfile = ''
    asmfile = tk.filedialog.asksaveasfilename(title='Save MSX2 bitmap assembler data', filetypes=(('Z80 assembly data', '*.z80'),('Z80 assembly data', '*.Z80'), ('All files', '*.*')))
    if asmfile == '' or type(asmfile) == tuple:
        return 
    if asmfile[-4:].upper() != '.Z80':
        asmfile = asmfile + '.z80'
    outdata = []
    outdata.append('; Made with MSX2 Bitmapper')
    outdata.append(';')
    global graphic_mode
    global graphics_mode_height
    outdata.append('; Graphic mode: ' + graphic_mode)
    outdata.append('; Vertical res: ' + str(graphics_mode_height))
    if graphics_mode_height == 212:
        outdata.append(';  (Be sure to set bit 7 of R#9!)')
    if (graphic_mode == 'G4') or (graphic_mode == 'G5'):
        if graphics_mode_height == 212:
            outdata.append('; Size in hex: $7000')
        else:
            outdata.append('; Size in hex: $6000')
    else:
        if graphics_mode_height == 212:
            outdata.append('; Size in hex: $D400')
        else:
            outdata.append("; Size in hex: $C000")
    if (graphic_mode == 'G4') or (graphic_mode == 'G6'):
        ### G4 SPECS
        # 0x7000 length in hex (27,136 bytes) for 256x212
        # each pixel is 4 bits x> yv based on palette number.
        # e.g. $42, $1b = 4, 2, 1, 11 (MSB > LSB)
        ### G6 SPECS
        # 0xD400 in hex (54,272 bytes) for 512x212
        # as G4, each pixel is 4 bits, but width is double res.
        # e.g. $42, $1b = 4, 2, 1, 11
        y = 0
        while y < graphics_mode_height:
            x = 0
            thisrowout = ' DB  '
            while x < graphics_mode_width:
                thisbyteout = ''
                px_a = screen_data[(y*graphics_mode_width)+x]
                px_a = str(px_a).format('1x')
                x += 1
                px_b = screen_data[(y*graphics_mode_width)+x]
                px_b = str(px_b).format('1x')
                thisbyteout += '$' + px_a + px_b + ', '
                thisrowout += thisbyteout
                x += 1
            outdata.append(thisrowout)
            y += 1
    elif (graphic_mode == 'G5'):
        ### G5 SPECS
        # 0x7000 in hex (27,136 bytes) for 512x212
        # each pixel is 2 bits per color based on palette index
        # e.g. $55, $DC = 1, 1, 1, 1, 3, 1, 3, 0 (MSB > LSB)
        y = 0
        while y < graphics_mode_height:
            x = 0
            thisrowout = ' DB  '
            incr = (y*graphics_mode_width)
            while x < graphics_mode_width:
                thisbyteout = ''
                px_a = screen_data[incr+x]
                px_a = format(px_a,'02b')
                x += 1
                px_b = screen_data[incr+x]
                px_b = format(px_b,'02b')
                x += 1
                px_c = screen_data[incr+x]
                px_c = format(px_c,'02b')
                x += 1
                px_d = screen_data[incr+x]
                px_d = format(px_d,'02b')
                x += 1
                fullbyte = px_a + px_b + px_c + px_d 
                fullbyte = format(int(fullbyte,2),'02x')
                thisbyteout += '$' + fullbyte + ', '
                thisrowout += thisbyteout 
            outdata.append(thisrowout)
            y += 1
    elif (graphic_mode == 'G7'):
        ### G7 SPECS
        # 0xD400 in hex (54,272 bytes) for 256x212
        # each pixel is 1 full byte RGB332.
        # e.g. $5B = #26F
        y = 0
        while y < graphics_mode_height:
            x = 0
            thisrowout = ' DB  '
            while x < graphics_mode_width:
                px = screen_data[(y*graphics_mode_width)+x]
                px_a = px[1]
                px_b = px[2]
                px_c = px[3]
                px_a = round(int(px_a,16)*(7/15))
                px_b = round(int(px_b,16)*(7/15))
                px_c = int(px_c,16)*(7/15)
                px_c = round(px_c * (3/7))
                px_a = format(px_a, '03b')
                px_b = format(px_b, '03b')
                px_c = format(px_c, '02b')
                fullbyte = px_a + px_b + px_c 
                fullbyte = format(int(fullbyte,2), '02x')
                fullbyte = '$' + fullbyte + ', '
                thisrowout += fullbyte 
                x += 1
            outdata.append(thisrowout)
            y += 1
    try:
        if asmfile[-4:].upper() != '.Z80':
            asmfile = asmfile + '.z80'
        f = open(asmfile, 'w')
        for s in outdata:
            f.write(s)
            f.write('\n')
        messagebox.showinfo('Export OK!', message='Z80 export successful.')
    except:
        messagebox.showerror('Export failed', message='Something went wrong!\nExport failed.')
    finally:
        if(f):
            f.close()

drawing_circle = None
circle_origin = [-1,-1]

def draw_pixel_atindex(p, size=1):
    global drawCanvas 
    global screen_pixels 
    global hex_palette 
    global selected_palette_no 
    global graphic_mode 
    global screen_data
    if p > len(screen_pixels):
        return
    if p < 0:
        return 
    drawCanvas.itemconfig(screen_pixels[p], fill=hex_palette[selected_palette_no])
    if graphic_mode != 'G7':
        screen_data[p] = selected_palette_no
    else:
        screen_data[p] = hex_palette[selected_palette_no]
    global pxsize
    size = int(pxsize.get())
    if size < 1:
        size = 1
    elif size > 9:
        size = 9
    pxsize.delete(0,tk.END)
    pxsize.insert(0,size)
    x = p % graphics_mode_width
    y = math.floor(p / graphics_mode_width)
    #print(x, y)
    if size > 1:
        #TODO: possible toggle for double-high brush size
        #TODO: possible toggle for diamond vs square 
        #atm only pixel-perfect square
        size_loop = size - 1
        if size_loop % 2 == 0: #is pixel size odd?   
            tp_origin_y = y - ((size_loop)/2)
            tp_origin_x = x - ((size_loop)/2)
        else: #is pixel size even?
            tp_origin_y = y - ((size_loop-1)/2)
            tp_origin_x = x - ((size_loop-1)/2)
        paint_square_brush(size, tp_origin_y, tp_origin_x)
        ####

def paint_square_brush(size, tp_origin_y, tp_origin_x):
    global graphics_mode_width 
    global drawCanvas 
    global screen_pixels 
    global hex_palette 
    global selected_palette_no 
    global graphic_mode 
    global screen_data 
    iy = 0
    while iy < size:
        if tp_origin_y + iy < 0:
            iy += 1
            continue
        ix = 0
        while ix < size:
            if (tp_origin_x + ix) >= graphics_mode_width:
                ix += 1
                continue
            if (tp_origin_x + ix) < 0:
                ix += 1
                continue
            tp = int(((tp_origin_y+iy)*graphics_mode_width) + (tp_origin_x+ix) )
            if tp > len(screen_pixels):
                ix += 1
                continue
            drawCanvas.itemconfig(screen_pixels[tp], fill=hex_palette[selected_palette_no])
            if graphic_mode != 'G7':
                screen_data[tp] = selected_palette_no
            else:
                screen_data[tp] = hex_palette[selected_palette_no]
            ix += 1
        iy += 1

def paint_diamond_brush(size, tp_origin_y, tp_origin_x):
    global graphics_mode_width 
    global drawCanvas 
    global screen_pixels 
    global hex_palette 
    global selected_palette_no 
    global graphic_mode 
    global screen_data 
    
    if tp_origin_x < 0:
        return
    iy = -size
    while iy < size:
        if tp_origin_y + iy < 0:
            iy += 1
            continue
        ix = -size
        while ix < size:
            if abs(ix) + abs(iy) >= size:
                ix += 1
                continue
            if (tp_origin_x + ix) >= graphics_mode_width:
                ix += 1
                continue
            if (tp_origin_x + ix) < 0:
                ix += 1
                continue
            tp = int(((tp_origin_y+iy)*graphics_mode_width) + (tp_origin_x+ix) )
            if tp > len(screen_pixels):
                ix += 1
                continue
            drawCanvas.itemconfig(screen_pixels[tp], fill=hex_palette[selected_palette_no])
            if graphic_mode != 'G7':
                screen_data[tp] = selected_palette_no
            else:
                screen_data[tp] = hex_palette[selected_palette_no]
            ix += 1
        iy += 1

'''returns tuple of 0,0 based x,y offset of drawCanvas'''
def get_canvas_offset():
    global drawCanvas
    global draw_scroll_x
    global draw_scroll_y
    global zoom_scale
    global graphics_mode_width
    scr_x = draw_scroll_x.get()
    scr_y = draw_scroll_y.get() 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])
    yofs = scr_y[0] * float(fscr[3])
    return (xofs, yofs)

def start_circle(o):
    global drawCanvas
    global drawing_circle
    ofs = get_canvas_offset()
    x = o.x+ofs[0]
    y = o.y+ofs[1]
    global circle_origin
    circle_origin[0] = x 
    circle_origin[1] = y
    drawing_circle = drawCanvas.create_oval(x, y, x, y, fill='', outline='white')
    
def move_circle(o):
    global drawCanvas 
    global drawing_circle 
    global circle_origin
    ofs = get_canvas_offset()
    x = o.x+ofs[0]
    y = o.y+ofs[1]
    drawCanvas.coords(drawing_circle, circle_origin[0], circle_origin[1], x, y)
    
def paint_circle(o, shouldFill = False):
    global drawCanvas
    global drawing_circle 
    set_undo_point()
    circ_coords = drawCanvas.coords(drawing_circle)
    mp = ((circ_coords[0]+circ_coords[2])/2, (circ_coords[1]+circ_coords[3])/2) #midpoint in expanded point size
    global app_scale 
    global zoom_scale 
    global y_ratio 
    mp_xy = (math.floor((mp[0] / (app_scale*zoom_scale))), math.floor((mp[1] / (app_scale*zoom_scale*y_ratio))))
    x_rad = math.floor(abs(circ_coords[2] - circ_coords[0]) / (app_scale*zoom_scale)/2)
    y_rad = math.floor(abs(circ_coords[3] - circ_coords[1]) / (app_scale*zoom_scale*y_ratio)/2)
    if x_rad < 1:
        x_rad = 1
    if y_rad < 1:
        y_rad = 1
    global graphics_mode_width
    last_y = math.floor( math.sqrt( (1 - (0/x_rad)**2)*y_rad**2) )
    i =  0

    while i < x_rad:
        # i is now the x position - e.g. negative 20 to positive 20
        dif_y = math.floor( math.sqrt( (1 - (i/x_rad)**2)*y_rad**2) )
        cur_xpx = mp_xy[0] + i
        cur_ypx = mp_xy[1] - dif_y 
        p = tileindex(cur_xpx, cur_ypx)
        if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        cur_xpx = mp_xy[0] - i
        cur_ypx = mp_xy[1] - dif_y 
        p = tileindex(cur_xpx, cur_ypx)
        if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        cur_xpx = mp_xy[0] + i
        cur_ypx = mp_xy[1] + dif_y 
        p = tileindex(cur_xpx, cur_ypx)
        if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        cur_xpx = mp_xy[0] - i
        cur_ypx = mp_xy[1] + dif_y 
        p = tileindex(cur_xpx, cur_ypx)
        if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        ystep = last_y - dif_y
        skip = 1
        while ystep > 1:
            # did we step down more than one?
            cur_xpx = mp_xy[0] + i
            cur_ypx = (mp_xy[1]-skip) - dif_y 
            p = tileindex(cur_xpx, cur_ypx)
            if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
                draw_pixel_atindex(p)

            cur_xpx = mp_xy[0] - i
            cur_ypx = (mp_xy[1]-skip) - dif_y 
            p = tileindex(cur_xpx, cur_ypx)
            if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
                draw_pixel_atindex(p)

            cur_xpx = mp_xy[0] + i
            cur_ypx = (mp_xy[1]+skip) + dif_y 
            p = tileindex(cur_xpx, cur_ypx)
            if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
                draw_pixel_atindex(p)

            cur_xpx = mp_xy[0] - i
            cur_ypx = (mp_xy[1]+skip) + dif_y 
            p = tileindex(cur_xpx, cur_ypx)
            if (cur_xpx < graphics_mode_width) and (cur_ypx < graphics_mode_height) and \
            (cur_xpx >= 0) and (cur_ypx >= 0) and (p >=0) and (p < len(screen_pixels)):
                draw_pixel_atindex(p)

            skip += 1
            ystep -= 1
        last_y = dif_y 
        i += 1
    # finalize the line by taking last_y and printing that up and down equal spaces
    i = 0
    txa = mp_xy[0] - x_rad
    txb = mp_xy[0] + x_rad     
    while i < last_y:
        # +/-0 indicates the X axis.
        ty = mp_xy[1] + i 
        p = tileindex(txa, ty)
        if (txa < graphics_mode_width) and (ty < graphics_mode_height) and \
            (txa >= 0) and (ty >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        p = tileindex(txb, ty)
        if (txb < graphics_mode_width) and (ty < graphics_mode_height) and \
            (txb >= 0) and (ty >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        ty = mp_xy[1] - i 
        p = tileindex(txa, ty)
        if (txa < graphics_mode_width) and (ty < graphics_mode_height) and \
            (txa >= 0) and (ty >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        p = tileindex(txb, ty)
        if (txb < graphics_mode_width) and (ty < graphics_mode_height) and \
            (txb >= 0) and (ty >= 0) and (p >=0) and (p < len(screen_pixels)):
            draw_pixel_atindex(p)

        i += 1

    # Do fill?
    if shouldFill:
        height = math.floor(((mp_xy[1] + y_rad) - (mp_xy[1] - y_rad)) / 2)
        width = math.floor(((mp_xy[0] + x_rad) - ( mp_xy[0] - x_rad)) / 2)

        y_pos = height * -1
        x_pos = width * -1

        while y_pos <= height:
            while x_pos <= width:
                if (x_pos * x_pos * height * height) + (y_pos * y_pos * width * width) <= (height * height * width * width):
                    x = mp_xy[0] + x_pos
                    y = mp_xy[1] + y_pos

                    if x >= 0 and x < graphics_mode_width:
                        p = tileindex(x, y)

                        # prevent drawing off bounds
                        if p >= 0 and p < len(screen_pixels):
                            drawCanvas.itemconfig(screen_pixels[p], fill=hex_palette[selected_palette_no])

                x_pos += 1

            x_pos = width * -1
            y_pos += 1


    drawCanvas.delete(drawing_circle)
    return

def paint_and_fill_circle(o):
    paint_circle(o, True)

def tileindex(x, y):
    global graphics_mode_width
    return (y*graphics_mode_width)+x 



drawing_rect = None 
rect_start = [-1,-1]

def start_rect(o):
    global drawCanvas 
    global rect_start
    global drawing_rect 
    ofs = get_canvas_offset()
    rect_start[0] = o.x + ofs[0] 
    rect_start[1] = o.y + ofs[1]
    drawing_rect = drawCanvas.create_rectangle(rect_start[0], rect_start[1], rect_start[0], rect_start[1], outline='white')

def move_rect(o):
    global drawCanvas
    global rect_start 
    global drawing_rect 
    ofs = get_canvas_offset()
    nx = o.x + ofs[0]
    ny = o.y + ofs[1]
    drawCanvas.coords(drawing_rect, rect_start[0], rect_start[1], nx, ny)
    
def paint_rect(o, shouldFill = False):
    global line_startpos # tuple so OK !
    global rect_start
    global drawCanvas
    global drawing_rect
    global zoom_scale 
    global app_scale 
    set_undo_point()
    # need four lines
    ofs = get_canvas_offset()
    boundx = drawCanvas.winfo_width()*zoom_scale
    p1 = xypos(rect_start[0]-ofs[0], rect_start[1]-ofs[1])
    p2 = xypos(o.x, rect_start[1]-ofs[1])
    p3 = xypos(rect_start[0]-ofs[0], o.y)
    p4 = xypos(o.x, o.y)
    line_startpos = (rect_start[0], rect_start[1])
    paint_line(p2, undo=False) # top
    line_startpos = (p2.x+ofs[0], p2.y+ofs[1])
    if o.x <= boundx:
        if o.x >= 0 and o.x < boundx: # left out of bounds?
            paint_line(p4, undo=False) 
    line_startpos = (p1.x+ofs[0], p1.y+ofs[1])
    paint_line(p3, undo=False) # left 
    line_startpos = (p3.x+ofs[0], p3.y+ofs[1])
    paint_line(p4, undo=False) # bottom

    if shouldFill: 
        x_start = p1.x
        x_end = p2.x

        if x_start > x_end:
            temp = x_start
            x_start = x_end
            x_end = temp
        
        while x_start < x_end:
            line_startpos = (x_start, p1.y)
            paint_line(xypos(x_start, p3.y))
            x_start += 1

    drawCanvas.delete(drawing_rect) 

def paint_and_fill_rect(o):
    paint_rect(o, True)


selector_start = [-1,-1]

def start_select(o):
    global drawCanvas
    global selector_rect 
    global selector_start 
    ofs = get_canvas_offset()
    selector_start = [ofs[0]+o.x, ofs[1]+o.y]
    global app_scale 
    global zoom_scale 
    global y_ratio 
    x1 = math.floor(selector_start[0] / (app_scale*zoom_scale)) * app_scale*zoom_scale
    y1 = math.floor(selector_start[1] / (app_scale*zoom_scale*y_ratio)) * app_scale*zoom_scale*y_ratio
    selector_start[0] = x1
    selector_start[1] = y1
    global copy_w
    global copy_h
    if copy_w > 0 or copy_h > 0:
        x2 = x1 + (copy_w * app_scale * zoom_scale)
        y2 = y1 + (copy_h * app_scale * zoom_scale * y_ratio)
    else:
        x2 = x1 + (app_scale*zoom_scale)
        y2 = y1 + (app_scale*zoom_scale*y_ratio)
    drawCanvas.delete(selector_rect)
    selector_rect = drawCanvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=max(1, (app_scale*zoom_scale)/8), dash=(4,4))
    
selector_end = [-1,-1]

def move_select(o):
    global drawCanvas 
    global selector_rect 
    global selector_start 
    global selector_end
    ofs = get_canvas_offset()
    selector_end[0] = max(math.floor((ofs[0]+o.x)/(app_scale*zoom_scale)) * app_scale * zoom_scale, selector_start[0]+(app_scale*zoom_scale))
    selector_end[1] = max(math.floor((ofs[1]+o.y)/(app_scale*zoom_scale*y_ratio)) * app_scale * zoom_scale * y_ratio, selector_start[1]+(app_scale*zoom_scale*y_ratio))
    drawCanvas.coords(selector_rect, selector_start[0], selector_start[1], selector_end[0], selector_end[1])


copy_buffer = []
copy_w = -1
copy_h = -1

def copy_data(cut=False):
    global selector_start 
    global selector_end 
    global draw_mode 
    global copy_buffer 
    if draw_mode != 'SELECT':
        return
    copy_buffer = []
    global app_scale 
    global zoom_scale 
    global y_ratio 
    global copy_w
    global copy_h
    copy_w = math.floor(abs(selector_end[0] - selector_start[0])/(app_scale*zoom_scale))
    copy_h = math.floor(abs(selector_end[1] - selector_start[1])/(app_scale*zoom_scale*y_ratio))
    x1 = math.floor(selector_start[0] / (app_scale*zoom_scale))
    y1 = math.floor(selector_start[1] / (app_scale*zoom_scale*y_ratio))
    global graphics_mode_width
    global graphic_mode
    global drawCanvas
    px_start = (y1*graphics_mode_width)+x1
    iy = 0
    while iy < copy_h:
        ix = 0
        while ix < copy_w:
            p = px_start+(iy*graphics_mode_width)+ix
            copy_buffer.append(screen_data[p])
            if cut == True:
                if graphic_mode == 'G7':
                    screen_data[p] = hex_palette[0]
                else:
                    screen_data[p] = 0
                drawCanvas.itemconfig(screen_pixels[p], fill=hex_palette[0])
            ix += 1
        iy += 1

     
def paste_data():
    global selector_start 
    global selector_end 
    
    global app_scale 
    global zoom_scale 
    global y_ratio 
    set_undo_point()
    x1 = math.floor(selector_start[0] / (app_scale*zoom_scale))
    y1 = math.floor(selector_start[1] / (app_scale*zoom_scale*y_ratio))
    global graphics_mode_width 
    px_start = (y1*graphics_mode_width)+x1 
    global copy_h
    global copy_w
    global drawCanvas
    global copy_buffer
    global graphics_mode_height
    iy = 0
    while iy < copy_h:
        if y1 + iy > graphics_mode_height:
            break
        ix = 0
        while ix < copy_w:
            if x1 + ix >= graphics_mode_width:
                ix += 1
                continue
            p = px_start+(iy*graphics_mode_width)+ix
            if p > len(screen_pixels):
                return 
            c = copy_buffer[(iy*copy_w)+ix]
            screen_data[p] = c
            if graphic_mode != 'G7':
                drawCanvas.itemconfig(screen_pixels[p], fill=hex_palette[c])
            else:
                drawCanvas.itemconfig(screen_pixels[p], fill=c)
            ix += 1
        iy += 1

def cut_data():
    set_undo_point()
    copy_data(cut=True)
    
undo_history = []

def set_undo_point():
    global undo_history 
    global screen_data 
    #print('Undo added.')
    if len(undo_history) >= 100:
        undo_history.pop(0)
    undo_history.append(list(screen_data))

redo_history = []

def undo_last():
    global undo_history 
    global screen_data 
    global redo_history 
    if len(undo_history) == 0:
        return
    if len(redo_history) >= 100:
        redo_history.pop(0)
    redo_history.append(list(screen_data))
    screen_data = list(undo_history.pop())
    repaint_screen()

def redo_last():
    global screen_data 
    global redo_history 
    if len(redo_history) == 0:
        return 
    set_undo_point()
    screen_data = list(redo_history.pop())
    repaint_screen()
    return 


def keyboard_monitor(obj):
    if obj.state & 4 == 4:
        if obj.keysym == 'c':
            copy_data()
        elif obj.keysym == 'v':
            paste_data()
        elif obj.keysym == 'x':
            cut_data()
        elif obj.keysym == 'z':
            undo_last()
        elif obj.keysym == 'y':
            redo_last()
        elif obj.keysym == 's':
            save_normal()
            return 

class make_new(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('New bitmap')
        self.b_4_192 = tk.Button(self, text='GRAPHIC 4 (192)', command=lambda:self.new('G4', False))#.grid(row=0,column=0)
        self.b_4_192.grid(row=2, column=0)
        self.b_4_212 = tk.Button(self, text='GRAPHIC 4 (212)', command=lambda:self.new('G4', True))#.grid(row=0,column=1)
        self.b_4_212.grid(row=2, column=2)
        self.b_5_192 = tk.Button(self, text='GRAPHIC 5 (192)', command=lambda:self.new('G5', False))#.grid(row=1,column=0)
        self.b_5_192.grid(row=4, column=0)
        self.b_5_212 = tk.Button(self, text='GRAPHIC 5 (212)', command=lambda:self.new('G5', True))#.grid(row=1,column=1)
        self.b_5_212.grid(row=4, column=2)
        self.b_6_192 = tk.Button(self, text='GRAPHIC 6 (192)', command=lambda:self.new('G6', False))#.grid(row=2,column=0)
        self.b_6_192.grid(row=6, column=0)
        self.b_6_212 = tk.Button(self, text='GRAPHIC 6 (212)', command=lambda:self.new('G6', True))#.grid(row=2,column=1)
        self.b_6_212.grid(row=6, column=2)
        self.b_7_192 = tk.Button(self, text='GRAPHIC 7 (192)', command=lambda:self.new('G7', False))#.grid(row=3,column=0)
        self.b_7_192.grid(row=8, column=0)
        self.b_7_212 = tk.Button(self, text='GRAPHIC 7 (212)', command=lambda:self.new('G7', True))#.grid(row=3,column=1)
        self.b_7_212.grid(row=8, column=2)
        self.lb_b4a = tk.Label(master=self, text='SCREEN-5, 256x192\n16 colors')
        self.lb_b4a.grid(row=3, column=0)
        self.lb_b4b = tk.Label(master=self, text='SCREEN-5, 256x212\n16 colors')
        self.lb_b4b.grid(row=3, column=2)
        self.lb_b5a = tk.Label(master=self, text='SCREEN-6, 512x192\n4 colors')
        self.lb_b5a.grid(row=5, column=0)
        self.lb_b5b = tk.Label(master=self, text='SCREEN-6, 512x212\n4 colors')
        self.lb_b5b.grid(row=5, column=2)
        self.lb_b6a = tk.Label(master=self, text='SCREEN-7, 512x192\n16 colors')
        self.lb_b6a.grid(row=7, column=0)
        self.lb_b6b = tk.Label(master=self, text='SCREEN-7, 512x212\n16 colors')
        self.lb_b6b.grid(row=7, column=2)
        self.lb_b7a = tk.Label(master=self, text='SCREEN-8, 256x192\n256 colors')
        self.lb_b7a.grid(row=9, column=0)
        self.lb_b7b = tk.Label(master=self, text='SCREEN-8, 256x212\n256 colors')
        self.lb_b7b.grid(row=9, column=2)
        self.lbl = tk.Label(master=self, text='Select a graphics mode!')
        self.lbl.grid(row=0,columnspan=4)

    def destroy(self):
        self.withdraw()

    def new(self, mode, expanded):
        global palette_display
        palette_display[0].clicked(0)
        new_file(mode, expanded)
        global undo_history 
        global redo_history
        undo_history = []
        redo_history = []
        self.withdraw()


newwin = None
if newwin:
    newwin.mainloop()

def open_new_window():
    a = tk.messagebox.askyesnocancel('Save?', message='Save current bitmap before\nstarting a new one?')
    if a == True:
        save_normal()
        global m2bfilename
        if m2bfilename == '' or type(m2bfilename)==tuple:
            return
    elif a == None:
        return
    global newwin
    if not newwin:
        newwin = make_new()
    else:
        newwin.deiconify()
    
def px_square():
    global editMenu 
    editMenu.entryconfigure(4, label="✓Pixel brush: Square")
    editMenu.entryconfigure(5, label="Pixel brush: Diamond")
    global brush_style
    brush_style = 'square'
    return
def px_diamond():
    global editMenu 
    editMenu.entryconfigure(4, label="Pixel brush: Square")
    editMenu.entryconfigure(5, label="✓Pixel brush: Diamond")
    global brush_style
    brush_style = 'diamond'
    return

def show_about():
    tk.messagebox.showinfo("About", message='MSX2 Bitmapper v1.0\n(c)2019 Ben Ferguson\n\nhttps://github.com/bferguson3/msx2tools\n\nMade in Python3!')


app.bind("<Key>", keyboard_monitor)

scalebutton = tk.Button(win, command=toggle_scale)
menuBar = tk.Menu(app)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label='New...', command=open_new_window)
fileMenu.add_command(label='Save (Ctrl+S)...', command=save_normal)
fileMenu.add_command(label='Load...', command=load_m2b)
fileMenu.add_separator()
fileMenu.add_command(label='Export as z80 assembly...', command=export_z80)
fileMenu.add_command(label='Export palette as z80...', command=export_pal_data)
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=client_exit)
editMenu = tk.Menu(menuBar, tearoff=0)
editMenu.add_command(label='Cut (Ctrl+X)', command=cut_data)
editMenu.add_command(label='Copy (Ctrl+C)', command=copy_data)
editMenu.add_command(label='Paste (Ctrl+V)', command=paste_data)
editMenu.add_separator()
editMenu.add_command(label='✓Pixel brush: Square', command=px_square)
editMenu.add_command(label='Pixel brush: Diamond', command=px_diamond)
editMenu.add_separator()
editMenu.add_command(label='Undo (Ctrl+Z)', command=undo_last)
editMenu.add_command(label='Redo (Ctrl+Y)', command=redo_last)
helpMenu = tk.Menu(menuBar, tearoff=0)
helpMenu.add_command(label='About', command=show_about)
toolbar = tk.Frame(win, width=600, height=30, relief=tk.RAISED)
savebutton = tk.Button(toolbar, image=save_icon, width=20, height=20, command=save_normal)
savebutton.grid(row=0,column=0)
pxbutton = tk.Button(toolbar, image=dotbmp, width=20, height=20, relief=tk.SUNKEN, command=lambda:change_mode('PX'))#px_mode)
pxbutton.grid(row=0, column=1, padx=(20,0), sticky='w')
linebutton = tk.Button(toolbar, image=line_icon, width=20, height=20, command=lambda:change_mode('LINE'))#line_mode)
linebutton.grid(row=0, column=2)
circlebutton = tk.Button(toolbar, image=circle_icon, width=20, height=20, command=lambda:change_mode('CIRCLE'))
circlebutton.grid(row=0, column=3)
rectbutton = tk.Button(toolbar, image=rect_icon, width=20, height=20, command=lambda:change_mode('RECT'))
rectbutton.grid(row=0, column=4)
pxlbl = tk.Label(toolbar, text='Px:')
pxlbl.grid(row=0,column=5)
pxsize = tk.Entry(toolbar, width=2)
pxsize.grid(row=0,column=6)
pxsize.insert(0,1)
selectbutton = tk.Button(toolbar, image=select_icon, width=20, height=20, command=lambda:change_mode('SELECT'))
selectbutton.grid(row=0, column=7, padx=(20,0))
cutbutton = tk.Button(toolbar, image=cut_icon, width=20, height=20, command=cut_data)
copybutton = tk.Button(toolbar, image=copy_icon, width=20, height=20, command=copy_data)
pastebutton = tk.Button(toolbar, image=paste_icon, width=20, height=20, command=paste_data)
cutbutton.configure(state=tk.DISABLED)
copybutton.configure(state=tk.DISABLED)
pastebutton.configure(state=tk.DISABLED)
cutbutton.grid(row=0, column=8)
copybutton.grid(row=0, column=9)
pastebutton.grid(row=0, column=10)
undobutton = tk.Button(toolbar, image=undo_icon, width=20, height=20, command=undo_last)
redobutton = tk.Button(toolbar, image=redo_icon, height=20, width=20, command=redo_last)
undobutton.grid(row=0, column=11, padx=(20,0))
redobutton.grid(row=0, column=12)
scalebutton = tk.Button(toolbar, image=scale_icon, width=20, height=20, command=toggle_scale)
scalebutton.grid(row=0, column=13, padx=(20,0), sticky='w')
zoom1button = tk.Button(toolbar, image=zoom1_icon, width=20, height=20, command=zoom_1x, relief=tk.SUNKEN)
zoom1button.grid(row=0, column=14, sticky='w')
zoom2button = tk.Button(toolbar, image=zoom2_icon, width=20, height=20, command=zoom_2x)
zoom2button.grid(row=0, column=15, sticky='w')
zoom4button = tk.Button(toolbar, image=zoom4_icon, width=20, height=20, command=zoom_4x)
zoom4button.grid(row=0, column=16, sticky='w')
zoom8button = tk.Button(toolbar, image=zoom8_icon, width=20, height=20, command=zoom_8x)
zoom8button.grid(row=0, column=17, sticky='w')

toolbar.grid(row=0, columnspan=12)
menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)
menuBar.add_cascade(label='Help', menu=helpMenu)
app.config(menu=menuBar) 

init_screen_data(mode='G4', expanded=False)
init_screen_pixels()
toggle_scale(1)
editMenu.entryconfigure(0, state=tk.DISABLED)
editMenu.entryconfigure(1, state=tk.DISABLED)
editMenu.entryconfigure(2, state=tk.DISABLED)

drawCanvas.bind("<Button-1>", clicked_loc)
drawCanvas.bind("<B1-Motion>", clicked_loc)
drawCanvas.bind("<Button-3>", set_scroll_orig)
drawCanvas.bind("<B3-Motion>", scroll_drawwindow)
drawCanvas.bind("<ButtonRelease-1>", set_undo_released)
# run the app
app.resizable(False, False)
app.protocol("WM_DELETE_WINDOW", client_exit)
app.title("MSX2 Bitmapper")
app.mainloop()