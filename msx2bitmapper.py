# bitmat wip

import tkinter as tk 
import sys 
import math 

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

dotbmp = tk.BitmapImage(data=dotdata)
scale_icon = tk.BitmapImage(data=scale_icon_data)
zoom1_icon = tk.BitmapImage(data=zoom1_icon_data)
zoom2_icon = tk.BitmapImage(data=zoom2_icon_data)
zoom4_icon = tk.BitmapImage(data=zoom4_icon_data)
zoom8_icon = tk.BitmapImage(data=zoom8_icon_data)


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
        screen_data.append(0)
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
d.grid(row = 1, column=1, rowspan=20, columnspan=20)
drawCanvas = tk.Canvas(d, width=256*app_scale, height=graphics_mode_height*app_scale*y_ratio, background='black', scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
drawCanvas.grid(row=1, column=1, rowspan=20, columnspan=20)
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
        palette_display[i].grid(row=i + 1, column=32, sticky='ne')
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


drawCanvas.bind("<Button-1>", clicked_loc)
drawCanvas.bind("<B1-Motion>", clicked_loc)
drawCanvas.bind("<Button-3>", set_scroll_orig)
drawCanvas.bind("<B3-Motion>", scroll_drawwindow)

max_scale = True

def toggle_scale(scale=0):
    #used in 'd' and 'drawCanvas'
    sx = app.winfo_screenwidth()
    sy = app.winfo_screenheight()
    global max_scale
    global app_scale 
    global graphic_mode 
    if graphic_mode == 'G4' or graphic_mode == 'G7':
        ys = 30
    else:
        ys = 50
    tscale = app_scale+1
    if max_scale == True:
        app_scale = 1
        tscale = 1
        max_scale = False 
    if (graphics_mode_height*tscale*y_ratio)+(ys*tscale)+30 > sy:
        #print('broke y')
        app_scale = sy/(((graphics_mode_height*y_ratio)+30)+ys)
        max_scale = True
    elif (graphics_mode_width*tscale)+(150*tscale) > sx:
        #print('broke x')
        app_scale = sx/((graphics_mode_width)+150)
        max_scale = True
    else:
        app_scale = tscale
    drawCanvas.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale*y_ratio, scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
    zoom_screen_pixels()
    rescale_palette()
    app.geometry('{}x{}'.format(int((graphics_mode_width*app_scale)+(150)), int((graphics_mode_height*app_scale*y_ratio)+(ys*app_scale)+60)))

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

def color_pixel(x, y):
    global drawCanvas
    global graphics_mode_width
    global graphics_mode_height
    if (x >= graphics_mode_width) or (y >= graphics_mode_height):
        return
    if (x < 0) or (y < 0):
        return
    global screen_data
    global screen_pixels 
    global selected_palette_no
    global hex_palette
    tp = (y*graphics_mode_width) + x
    screen_data[tp] = selected_palette_no
    drawCanvas.itemconfig(screen_pixels[tp], fill=hex_palette[selected_palette_no])

def draw_mode():
    return 

def client_exit():
    sys.exit()
    
def newg4():
    global app_scale
    init_screen_data(mode='G4', expanded=False)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg4e():
    global app_scale
    init_screen_data(mode='G4', expanded=True)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg5():
    global app_scale
    init_screen_data(mode='G5', expanded=False)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg5e():
    global app_scale
    init_screen_data(mode='G5', expanded=True)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg6():
    global app_scale
    init_screen_data(mode='G6', expanded=False)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg6e():
    global app_scale
    init_screen_data(mode='G6', expanded=True)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg7():
    global app_scale
    init_screen_data(mode='G7', expanded=False)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()
def newg7e():
    global app_scale
    init_screen_data(mode='G7', expanded=True)
    init_screen_pixels()
    app_scale -= 1
    toggle_scale()

m2bfilename = ''

from tkinter import filedialog, messagebox

def save_normal():
    global m2bfilename 
    if m2bfilename == '':
        m2bfilename = tk.filedialog.asksaveasfilename(title='Save MSX2 Bitmapper file', filetypes=( ('MSX2 Bitmapper file', '*.m2b'),('All files', '*.*') ))
    if m2bfilename == '' or type(m2bfilename) == tuple:
        return
    if m2bfilename[-4:].upper() != '.M2B':
        m2bfilename = m2bfilename + '.M2B'
    save_bitmap()

def save_bitmap():
    global m2bfilename
    global graphic_mode
    global screen_pixels
    global graphics_mode_height
    global drawCanvas
    #if graphic_mode == 'G7':
        # output hex color vals
    f = None 
    try:
        f = open(m2bfilename, "w")
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
        tk.messagebox.showinfo('Save successful!', message='Bitmap file saved successfully.')
    except:
        tk.messagebox.showerror('Error', message='Error while saving file.')
    finally:
        f.close()
    # else:
    #     f = None 
    #     # output palette itself
    #     try:
    #         f = open(m2bfilename, 'w')
    #         f.write(graphic_mode + '\n')
    #         f.write(str(graphics_mode_height)+'\n')
    #         for c in palette_display:
    #             f.write(str(c.myVal)+',')
    #         f.write('\n')
    #         for c in screen_data:
    #             f.write(str(c)+',')
    #         tk.messagebox.showinfo('Save successful!', message='Bitmap file saved successfully.')
    #     except:
    #         tk.messagebox.showerror('Error', message='Error while saving file.')
    #     finally:
    #         f.close()

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
    m2bfilename = tk.filedialog.askopenfilename(title='Load MSX2 Bitmapper file', filetypes=( ('MSX2 Bitmapper file', '*.m2b'),('All files', '*.*') ))
    if m2bfilename == '' or type(m2bfilename) == tuple:
        return 
    try: 
        f = open(m2bfilename, 'r')
        gm = f.readline()
        gm = gm[0:2]
        pw = f.readline()
        pw = pw[0:3]
        if (gm == 'G4') or (gm == 'G5') or (gm == 'G6') or (gm == 'G7'):
            graphic_mode = gm
        if (pw == 212):
            expanded = True 
        else:
            expanded = False
        # i forgot to do palette!
        pl = f.readline()
        pl = pl.split(',')
        pl.pop()
        global hex_palette
        i = 0
        while i < (len(pl)):
            hex_palette[i] = pl[i]
            i += 1
        add_palette_display()
        indata = f.readline()
        indata = indata.split(',')
        indata.pop()
        refresh_entire_screen(expanded, indata)
    except:
        tk.messagebox.showerror('Error loading', message='File could not be loaded.')
    finally:
        f.close()
        
scalebutton = tk.Button(win, text='W', command=toggle_scale)
zoombutton = tk.Button(win, text='Z', command=toggle_zoom)
menuBar = tk.Menu(app)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label='New G4 bitmap (192)', command=newg4)
fileMenu.add_command(label='New G4 bitmap (212)', command=newg4e)
fileMenu.add_command(label='New G5 bitmap (192)', command=newg5)
fileMenu.add_command(label='New G5 bitmap (212)', command=newg5e)
fileMenu.add_command(label='New G6 bitmap (192)', command=newg6)
fileMenu.add_command(label='New G6 bitmap (212)', command=newg6e)
fileMenu.add_command(label='New G7 bitmap (192)', command=newg7)
fileMenu.add_command(label='New G7 bitmap (212)', command=newg7e)
fileMenu.add_command(label='Save', command=save_normal)
fileMenu.add_command(label='Load...', command=load_m2b)
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=client_exit)
toolbar = tk.Frame(win, width=600, height=30, relief=tk.RAISED)
pxbutton = tk.Button(toolbar, image=dotbmp, width=20, height=20, relief=tk.SUNKEN, command=draw_mode)
pxbutton.grid(row=0, column=1, padx=(20,0), sticky='w')
scalebutton = tk.Button(toolbar, image=scale_icon, width=20, height=20, command=toggle_scale)
scalebutton.grid(row=0, column=2, padx=(20,0), sticky='w')
zoom1button = tk.Button(toolbar, image=zoom1_icon, width=20, height=20, command=zoom_1x, relief=tk.SUNKEN)
zoom1button.grid(row=0, column=3, sticky='w')
zoom2button = tk.Button(toolbar, image=zoom2_icon, width=20, height=20, command=zoom_2x)
zoom2button.grid(row=0, column=4, sticky='w')
zoom4button = tk.Button(toolbar, image=zoom4_icon, width=20, height=20, command=zoom_4x)
zoom4button.grid(row=0, column=5, sticky='w')
zoom8button = tk.Button(toolbar, image=zoom8_icon, width=20, height=20, command=zoom_8x)
zoom8button.grid(row=0, column=6, sticky='w')

toolbar.grid(row=0, columnspan=5)
menuBar.add_cascade(label="File", menu=fileMenu)
app.config(menu=menuBar) 

init_screen_data(mode='G4', expanded=False)
init_screen_pixels()
#add_palette_display()
toggle_scale(1)
#selected_palette_no = 15
#palette_display[selected_palette_no].setVal('#FFF')
# run the app
app.resizable(False, False)
app.protocol("WM_DELETE_WINDOW", client_exit)
app.title("MSX2 Bitmapper")
app.mainloop()