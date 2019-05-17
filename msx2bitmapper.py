# bitmat wip

import tkinter as tk 
import sys 
import math 

graphics_mode_width = 256
graphics_mode_192 = 192
graphics_mode_212 = 212
graphics_mode_height = graphics_mode_192
app_scale = 1
zoom_scale = 8
screen_data = []
screen_pixels = []
x_ratio = (4/3)
y_ratio = (3/4)

# init screen data
def init_screen_data(mode='G4', expanded=False):
    global screen_data
    global graphics_mode_width
    global graphics_mode_height 
    global graphics_mode_192 
    global graphics_mode_212 
    global x_ratio 
    global y_ratio
    if (mode == 'G4') or (mode == 'G7'):
        graphics_mode_width = 256
        #x_ratio = (4/3)
        y_ratio = (3/4)
    elif (mode == 'G5') or (mode == 'G6'):
        graphics_mode_width = 512
        #x_ratio = (4/3)
        y_ratio = (6/4)
    if expanded == False:
        graphics_mode_height = graphics_mode_192 
    else:
        graphics_mode_height = graphics_mode_212
    
    screen_data = []
    i = 0
    while i < (graphics_mode_width*graphics_mode_height):
        screen_data.append(0)
        i += 1
    #init_screen_pixels()

grid_lines=[]

def init_canvas_grid():
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
        p = drawCanvas.create_line(i*w, 0, i*w, y2, fill='grey')
        grid_lines.append(p)
        i += 1
    l = graphics_mode_height 
    x2 = (app_scale*zoom_scale*graphics_mode_width)
    i = 0
    while i < l:
        p = drawCanvas.create_line(0, i*h, x2, i*h, fill='grey')
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
        i += 1
    #i = 0
    l = graphics_mode_height 
    x2 = (app_scale*zoom_scale*graphics_mode_width)
    i = 0
    while i < l:
        drawCanvas.coords(grid_lines[i+graphics_mode_width], 0, i*h, x2, i*h)
        i += 1
    return

def init_screen_pixels():
    global screen_pixels
    global drawCanvas
    global app_scale 
    global zoom_scale 
    global screen_data
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

# define TK
app = tk.Tk()

# define base window dimensions
#app.geometry('{}x{}'.format(int(graphics_mode_width*app_scale+(80*app_scale)), int(graphics_mode_height*app_scale*y_ratio+(40*app_scale))))
app.config(background='black')

win = tk.Frame(master=app, background='black')
win.grid(row=0, column=0)

class drawFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

d = drawFrame(win, padx=20, pady=20, width=256*app_scale, height=graphics_mode_height*app_scale*y_ratio, background='black')
d.grid(rowspan=20, columnspan=20)
drawCanvas = tk.Canvas(d, width=256*app_scale, height=graphics_mode_height*app_scale*y_ratio, background='black', scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
drawCanvas.grid(row=0, column=0, rowspan=20, columnspan=20)
d.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale)
#drawCanvas.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale*y_ratio, scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
#app.geometry('{}x{}'.format(int(graphics_mode_width*app_scale+(80*app_scale)), int(graphics_mode_height*app_scale*y_ratio+(40*app_scale))))        

draw_scroll_y = tk.Scrollbar(d, orient=tk.VERTICAL, command=drawCanvas.yview)
draw_scroll_y.grid(row=0, rowspan=20, column=21, sticky='ns')
draw_scroll_x = tk.Scrollbar(d, orient=tk.HORIZONTAL, command=drawCanvas.xview)
draw_scroll_x.grid(row=21, column=0, columnspan=20, sticky='ew')

drawCanvas.config(xscrollcommand=draw_scroll_x.set, yscrollcommand=draw_scroll_y.set)

def print_loc(o):
    global drawCanvas 
    global app_scale 
    global zoom_scale 
    scr_x = draw_scroll_x.get() 
    fscr = drawCanvas.cget('scrollregion')
    fscr = fscr.split(' ')
    xofs = scr_x[0] * float(fscr[2])  # should be 1:1 px left bounding
    px = math.floor((xofs+o.x) / (app_scale*zoom_scale))
    scr_y = draw_scroll_y.get()
    yofs = scr_y[0] * float(fscr[3])
    py = math.floor((yofs + o.y) / (app_scale*zoom_scale*y_ratio))
    print(px, py)

drawCanvas.bind("<Button-1>", print_loc)

def toggle_scale(scale=0):
    #used in 'd' and 'drawCanvas'
    sx = app.winfo_screenwidth()
    #print(sx)
    global app_scale 
    if scale == 0:
        app_scale += 1
        if graphics_mode_width*app_scale > sx:
            app_scale = 1
    else:
        app_scale = scale
        if graphics_mode_width*app_scale > sx:
            app_scale = 1
    d.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale)
    drawCanvas.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale*y_ratio, scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
    zoom_screen_pixels()
    #update_canvas_grid()
    app.geometry('{}x{}'.format(int(graphics_mode_width*app_scale+(80*app_scale)), int(graphics_mode_height*app_scale*y_ratio+(40*app_scale))))

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

def toggle_zoom():
    global zoom_scale
    if zoom_scale == 2:
        zoom_scale = 4
    elif zoom_scale == 1:
        zoom_scale = 2
    elif zoom_scale == 4:
        zoom_scale = 8
    elif zoom_scale == 8:
        zoom_scale = 1
    drawCanvas.config(scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
    zoom_screen_pixels()
    

scalebutton = tk.Button(win, text='Toggle scale', command=toggle_scale)
scalebutton.grid(row=1, column=21, sticky='n')
zoombutton = tk.Button(win, text='Toggle zoom', command=toggle_zoom)
zoombutton.grid(row=2, column=21, sticky='n')

init_screen_data(mode='G7', expanded=False)
init_screen_pixels()
toggle_scale(1)

# run the app
app.mainloop()