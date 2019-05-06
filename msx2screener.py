#########################################################
# MSX2 Screener
#
# (c) 2019 Ben Ferguson
#
# Use Python 3! (Coded in 3.7.1)
# 
# v1.00: First release
# 
#
# Assembles z80 byte data for GRAPHIC3 (screen 4)
#  screen arrangements for use with compilers.
# Easy point-and-click interface.
# 
##########################################################

import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox 
import math 

# MSX2 default 16-color palette, in integer strings
defaultIntegerPalette = [
    '000', '000', '161', '373',
    '117', '237', '511', '267',
    '711', '733', '661', '664',
    '141', '625', '555', '777'
]

integerPalette = defaultIntegerPalette.copy()

# TK Setup
app = tk.Tk()
app.title('MSX2 Spriter')

# Global def 
win = None 
screenCanvas = None 
screenScale = 2.5
iconScale = 2
tileSize = 8
tilePalettes = []
i = 0
while i < 3:
    tilePalettes.append(None)
    i += 1
m2pfilename = ''
tile_data = [] 
i = 0 
while i < 3:
    j = 0
    blank = []
    #tile_data.append(blank)
    while j < 256:
        s = 0
        tile_data.append(blank)
        j += 1
    i += 1
screenpixels = []
tilepixels = []
i = 0
while i < 3:
    j = 0
    blank = []
    tilepixels.append(blank)
    while j < 32:
        s = 0
        while s < 8:
            p = 0
            while p < 8:
                r = 0
                while r < 8:
                    screenpixels.append(blank)
                    tilepixels[i].append(blank)
                    r += 1
                p += 1
            s += 1
        j += 1
    i += 1


def convertIntColorToHex(intstr):
    tempPalVals = []
    tempPalVals.append('#')
    a = math.floor((int(intstr[:-2]) / 7) * 255)
    tempPalVals.append(hex(a)[2:])
    if a == 0:
        tempPalVals.append('0')
    a = math.floor((int(intstr[1:-1]) / 7) * 255)
    tempPalVals.append(hex(a)[2:])
    if a == 0:
        tempPalVals.append('0')
    a = math.floor((int(intstr[2:]) / 7) * 255)
    tempPalVals.append(hex(a)[2:])
    if a == 0:
        tempPalVals.append('0')
    tempPalVals = ''.join(tempPalVals)
    return tempPalVals

def draw_tile(obj):
    xt = math.floor(obj.x / (screenScale*8))
    yt = math.floor(obj.y / (screenScale*8))
    print(str(xt) + ' ' + str(yt))

def erase_tile(obj):
    xt = math.floor(obj.x / (screenScale*8))
    yt = math.floor(obj.y / (screenScale*8))
    print(str(xt) + ' ' + str(yt))

def select_tile0(obj):
    select_tile(0, obj.x, obj.y)
def select_tile1(obj):
    select_tile(1, obj.x, obj.y)
def select_tile2(obj):
    select_tile(2, obj.x, obj.y)

def select_tile(tilepalnum, xpos, ypos):
    xt = math.floor(xpos/(iconScale*8))
    yt = math.floor(ypos/(iconScale*8))
    print(str(tilepalnum)+' '+str(xt)+' '+str(yt))
    DrawTileSelector(tilepalnum, xpos, ypos)

tile_selector = None
#i = 0
#while i < 4:
#    tile_selector.append(None)
#    i += 1

def DrawTileSelector(tilepal, x, y):
    # redundant?
    if tile_selector == None:
        #i = 0
        #while i < 4:
        tilePalettes[tilepal].delete(tile_selector)
        #    i += 1
    tile_selector = tilePalettes[tilepal].create_rectangle(x, y, x+(tileSize*iconScale), y+(tileSize*iconScale), width=2, outline='white')


def InitTilePalettes():
    global tilePalettes
    # if tile palettes don't exist, create them, fill with c0
    i = 0
    while i < 3:
        if tilePalettes[i] == None:
            tilePalettes[i] = tk.Canvas(win, background=convertIntColorToHex(integerPalette[0]), width=(tileSize*32*iconScale), height=(tileSize*8*iconScale))
        # clear them 
        tilePalettes[i].delete("all")
        # align
        tilePalettes[i].grid(row=4+(i*3), column=16)
        # then draw grid
        x = 0
        while x < 32:
            tilePalettes[i].create_line(x*(tileSize*iconScale), 0, x*(tileSize*iconScale), (iconScale*tileSize*8), fill='grey')
            x += 1
        y = 0 
        while y < 24:
            tilePalettes[i].create_line(0, y*(tileSize*iconScale), (tileSize*iconScale*32), y*(tileSize*iconScale), fill='grey')
            y += 1
        i += 1
    # and bind clicks
    i = 0
    while i < 3:
        # and populate it with 32x8x64 pixels
        xt = 0
        while xt < 32:
            yt = 0
            while yt < 8:
                xp = 0
                while xp < 8:
                    yp = 0
                    while yp < 8: # assign to tilepixels
                        tilepixels[i][(yt*32*64)+(xt*64)+(yp*8)+xp] = tilePalettes[i].create_rectangle( (xp*iconScale)+(xt*8*iconScale),\
                             ((yp*iconScale)+(iconScale*8*yt),\
                             ((xp*iconScale)+(xt*8*iconScale))+iconScale,\
                             ((yp*iconScale)+(iconScale*8*yt))+iconScale), outline='')
                        yp += 1
                    xp += 1
                yt += 1
            xt += 1
        i += 1
    tilePalettes[0].bind("<Button-1>", select_tile0)
    tilePalettes[1].bind("<Button-1>", select_tile1)
    tilePalettes[2].bind("<Button-1>", select_tile2)

def InitScreenWindow():
    global screenCanvas
    # if the canvas doesn't exist, create it, fill with color 0 in hex
    if screenCanvas == None:
        screenCanvas = tk.Canvas(win, background=convertIntColorToHex(integerPalette[0]), width=(screenScale*32*tileSize), height=(screenScale*24*tileSize))
        # and bind click events
        screenCanvas.bind("<Button-1>", draw_tile)
        screenCanvas.bind("<B1-Motion>", draw_tile)
        screenCanvas.bind("<Button-3>", erase_tile)
        screenCanvas.bind("<B3-Motion>", erase_tile)
    # then clear it
    screenCanvas.delete("all")
    # set pos 
    screenCanvas.grid(row=3, column=3, rowspan=10, columnspan=10)
    # and draw 32x24 grid
    x = 0
    while x < 32:
        screenCanvas.create_line(x*(screenScale*tileSize), 0, x*(screenScale*tileSize), (tileSize*screenScale*24), fill='grey')
        x += 1
    y = 0
    while y < 24:
        screenCanvas.create_line(0, y*(screenScale*tileSize), (tileSize*screenScale*32), y*(screenScale*tileSize), fill='grey')
        y += 1
    # then populate it with 3x32x8x(8x8) pixels
    i = 0
    while i < 3:
        xt = 0
        while xt < 32:
            yt = 0
            while yt < 8:
                xp = 0
                while xp < 8:
                    yp = 0
                    while yp < 8: #assign to screenpixels
                        screenpixels[(i*256*64)+(yt*32*64)+(xt*64)+(yp*8)+xp] = screenCanvas.create_rectangle( (xp*screenScale)+(xt*8*screenScale),\
                             ((yp*screenScale)+(screenScale*8*yt)+(i*screenScale*8*8),\
                             ((xp*screenScale)+(xt*8*screenScale))+screenScale,\
                             ((yp*screenScale)+(screenScale*8*yt))+(i*screenScale*8*8)+screenScale), outline='')
                        yp += 1
                    xp += 1
                yt += 1
            xt += 1
        i += 1

def RedrawTileGrid():
    i = 0
    while i < 3:
        x = 0
        while x < 32:
            tilePalettes[i].create_line(x*(tileSize*iconScale), 0, x*(tileSize*iconScale), (iconScale*tileSize*8), fill='grey')
            x += 1
        y = 0 
        while y < 24:
            tilePalettes[i].create_line(0, y*(tileSize*iconScale), (tileSize*iconScale*32), y*(tileSize*iconScale), fill='grey')
            y += 1
        i += 1

def LoadTileIcons():
    i = 0
    while i < 3:
        xt = 0
        while xt < 32:
            yt = 0
            while yt < 8:
                xp = 0
                while xp < 8:
                    yp = 0
                    while yp < 8: #assign to screenpixels
                        paint = convertIntColorToHex(integerPalette[tile_data[(i*256)+(yt*32)+xt][(yp*8)+xp]])
                        tilePalettes[i].itemconfig(tilepixels[i][(yt*32*64)+(xt*64)+(yp*8)+xp], fill=paint)
                        yp += 1
                    xp += 1
                yt += 1
            xt += 1
        i += 1
    #print(tile_data[(2*256)+(227)])
    RedrawTileGrid()


def import_m2p():
    global m2pfilename 
    m2pfilename = ''
    f = None 
    m2pfilename = tk.filedialog.askopenfilename(title='Load MSX2 Spriter file', filetypes=( ('MSX2 Spriter pattern file', '*.m2p'),('All files', '*.*') ))
    if m2pfilename == '' or type(m2pfilename) == tuple:
        return
    else:
        try:
            f=open(m2pfilename,'r')
            # read in palette
            data = f.readline()
            global integerPalette
            palette_vals = data.split(',')
            i = 0
            while i < 16:
                if palette_vals[i] == 'trans':
                    palette_vals[i] = '000'
                integerPalette[i] = palette_vals[i]
                i += 1
            # now read in pattern data to tile_data
            n = 0
            while n < 3:
                s = 0
                while s < 256:
                    data = f.readline()
                    tdat = data.split(',')
                    p = 0
                    while p < 64:
                        tdat[p] = int(tdat[p])
                        p += 1
                    tile_data[(n*256)+s] = tdat
                    s += 1
                n += 1
            LoadTileIcons()
        except IOError:
            messagebox.showerror("I/O error", message="Failed to load file. Check drives and permissions and try again.")
        except:
            messagebox.showerror("Unexpected error", message="Unknown error loading file. Ensure the file is a proper M2P file.")
        finally:
            if(f):
                f.close()

def launch_app():
    global win 
    
    if win == None:
        win = tk.Frame(master=app, width=800, height=600)
        win.grid(row=32, columnspan=32)

    # open screen draw window
    InitScreenWindow()
    # open 3x tile palettes
    InitTilePalettes() 

def client_exit():
    quit()

menuBar = tk.Menu(app)
fileMenu = fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label='Import .M2P patterns...', command=import_m2p)
fileMenu.add_command(label='Quit', command=client_exit)
menuBar.add_cascade(label="File", menu=fileMenu)
app.config(menu=menuBar) 

launch_app()
# Run the app
app.resizable(False, False)
app.protocol("WM_DELETE_WINDOW", client_exit)
app.mainloop()