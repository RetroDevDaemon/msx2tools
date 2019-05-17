# bitmat wip

import tkinter as tk 
import sys 
import math 

# define TK
app = tk.Tk()

graphics_mode_width = 256
graphics_mode_192 = 192
graphics_mode_212 = 212
graphics_mode_height = graphics_mode_192
app_scale = 1
zoom_scale = 8
screen_data = []
screen_pixels = []
y_ratio = (3/4)

###### BIT MAP DATA #######
dotdata = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x00, 0x10, 0x00, 0x28, 0x00, 0x5c, 0x00, 0x2e, 0x00, 0x17, 0x80, 0x0b, 0xc0, 0x05, 0xe0, 0x02, 0x70, 0x01, 0xb8, 0x00, 0x54, 0x00, 0x24, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00
};
"""
dotbmp = tk.BitmapImage(data=dotdata)

# init screen data
def init_screen_data(mode='G4', expanded=False):
    global screen_data
    global graphics_mode_width
    global graphics_mode_height 
    global graphics_mode_192 
    global graphics_mode_212 
    global y_ratio
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

palette_selectors = []

def populate_palette():

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

drawCanvas.bind("<Button-1>", clicked_loc)
drawCanvas.bind("<B1-Motion>", clicked_loc)

max_scale = False

def toggle_scale(scale=0):
    #used in 'd' and 'drawCanvas'
    sx = app.winfo_screenwidth()
    sy = app.winfo_screenheight()
    #print(sx)
    global max_scale
    global app_scale 
    if max_scale == True:
        app_scale = 1
        max_scale = False 
        drawCanvas.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale*y_ratio, scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
        zoom_screen_pixels()
        app.geometry('{}x{}'.format(int((graphics_mode_width*app_scale)+(150*app_scale)), int((graphics_mode_height*app_scale*y_ratio)+(150*app_scale))))
        return

    tscale = app_scale+1
    if (graphics_mode_height*tscale*y_ratio)+(150*tscale) > sy:
        app_scale = sy/((graphics_mode_height*y_ratio)+150)
        max_scale = True
    elif (graphics_mode_width*tscale)+(150*tscale) > sx:
        app_scale = sx/((graphics_mode_width)+150)
        max_scale = True
    drawCanvas.config(width=graphics_mode_width*app_scale, height=graphics_mode_height*app_scale*y_ratio, scrollregion=(0,0,graphics_mode_width*app_scale*zoom_scale, graphics_mode_height*app_scale*zoom_scale*y_ratio))
    zoom_screen_pixels()
    app.geometry('{}x{}'.format(int((graphics_mode_width*app_scale)+(150*app_scale)), int((graphics_mode_height*app_scale*y_ratio)+(150*app_scale))))

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

selected_palette_no = 1
hex_palette = ['#000', '#fff']

def color_pixel(x, y):
    global screen_data
    global screen_pixels 
    global graphics_mode_width
    global selected_palette_no
    global hex_palette
    tp = (y*graphics_mode_width) + x
    screen_data[tp] = selected_palette_no 
    drawCanvas.itemconfig(screen_pixels[tp], fill=hex_palette[selected_palette_no])

def draw_mode():
    return 
def client_exit():
    sys.exit()

menuBar = tk.Menu(app)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=client_exit)
toolbar = tk.Frame(win, width=600, height=30, relief=tk.RAISED)
pxbutton = tk.Button(toolbar, image=dotbmp, width=20, height=20, relief=tk.SUNKEN, command=draw_mode)
pxbutton.grid(row=0, column=1, padx=(20,0))
toolbar.grid(row=0)
menuBar.add_cascade(label="File", menu=fileMenu)
app.config(menu=menuBar) 


init_screen_data(mode='G6', expanded=True)
init_screen_pixels()
toggle_scale(2)

# run the app
app.mainloop()