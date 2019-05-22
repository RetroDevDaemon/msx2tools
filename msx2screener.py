#########################################################
# MSX2 Screener
#
# (c) 2019 Ben Ferguson
#
# Use Python 3! (Coded in 3.7.1)
# 
# v1.21: Added compression to file format.
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
import sys 
import os 
import zipfile

# MSX2 default 16-color palette, in integer strings
defaultIntegerPalette = [
    '000', '000', '161', '373',
    '117', '237', '511', '267',
    '711', '733', '661', '664',
    '141', '625', '555', '777'
]

dotdata = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x00, 0x10, 0x00, 0x28, 0x00, 0x5c, 0x00, 0x2e, 0x00, 0x17, 0x80, 0x0b, 0xc0, 0x05, 0xe0, 0x02, 0x70, 0x01, 0xb8, 0x00, 0x54, 0x00, 0x24, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00
};
"""
boxdata = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00,0x00, 0x00,
0x54, 0x15,0x00, 0x20,
0x04, 0x00,0x00, 0x20,
0x04, 0x00,0x00, 0x20,
0x04, 0x00,0x00, 0x20,
0x04, 0x00,0x00, 0x20,
0x04, 0x00,0xa8, 0x2a,
0x00, 0x00,0x00, 0x00
};
"""
save_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xfc, 0x3f, 0x1e, 0x78, 0x5e, 0x78, 0x5e, 0x78, 0x1e, 0x78, 0xfe, 0x7f, 0xfe, 0x7f, 0x7e, 0x7e, 0xbe, 0x7d, 0xbe, 0x7c, 0x7e, 0x7e, 0xfe, 0x7f, 0xfe, 0x6f, 0xfc, 0x3f, 0x00, 0x00
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
integerPalette = defaultIntegerPalette.copy()

# TK Setup
app = tk.Tk()
app.title('MSX2 Screener')

boxbmp = tk.BitmapImage(data=boxdata)
dotbmp = tk.BitmapImage(data=dotdata)
save_icon = tk.BitmapImage(data=save_icon_data)
cut_icon = tk.BitmapImage(data=cut_icon_data)
copy_icon = tk.BitmapImage(data=copy_icon_data)
paste_icon = tk.BitmapImage(data=paste_icon_data)
undo_icon = tk.BitmapImage(data=undo_icon_data)
redo_icon = tk.BitmapImage(data=redo_icon_data)
# Global def 
win = None 
screenCanvas = None 
loaded_tiles = False
screenScale = 2.5
iconScale = 2
tileSize = 8
tilePalettes = []
i = 0
while i < 3:
    tilePalettes.append(None)
    i += 1
m2pfilename = ''
z80filename = ''
m2cfilename = ''
tile_data = [] 
i = 0 
while i < 3:
    j = 0
    blank = []
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
#######

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

#nopattern_error = None
displayed_nopat_warn = False
screentiles = []
i = 0
while i < (256*3):
    screentiles.append(0)
    i += 1

last_tile_printed = -1
last_tile_used = -1
button_not_released = False 

def set_undo_release(o):
    global button_not_released
    button_not_released = False 

undo_history = []
redo_history = []

def add_undo_point():
    global undo_history
    global screentiles 
    undo_history.append(screentiles.copy())
    if len(undo_history) > 100:
        undo_history.pop(0)
    
def undo_last():
    global undo_history
    global screentiles
    global redo_history
    if len(undo_history) < 1:
        return
    redo_history.append(screentiles.copy())
    if len(redo_history) > 100:
        redo_history.pop(0)
    
    screentiles = undo_history.pop()
    refresh_whole_screen()

def redo_last():
    global undo_history
    global redo_history
    global screentiles 
    if len(redo_history) > 0:
        undo_history.append(screentiles.copy())
        screentiles = redo_history.pop()
        refresh_whole_screen()
    

def draw_tile(obj):
    if loaded_tiles == False:
        global displayed_nopat_warn
        if displayed_nopat_warn == False:
            displayed_nopat_warn = True 
            nopattern_error = messagebox.showinfo("Error","No patterns loaded.\nLoad an M2P file first!", type='ok')
            if nopattern_error == 'ok':
                displayed_nopat_warn = False
        return
    xt = math.floor(obj.x / (screenScale*8))
    yt = math.floor(obj.y / (screenScale*8))
    # whatever tile number we are within our tab (tab doesn't matter), set that value 0-255 
    # into screentiles[].
    oyt = yt
    global selected_tile_num
    global last_tile_used
    global last_tile_printed
    global button_not_released
    tab = 0
    if yt > 7:
        yt -= 8
        tab += 1
    if yt > 7:
        yt -= 8
        tab += 1
    if (oyt*32)+xt == last_tile_printed and last_tile_used == selected_tile_data[tab]:
        return
    if selected_tile_data[tab] == []:
        return
    last_tile_used = selected_tile_num 
    if button_not_released == False: 
        add_undo_point()
        button_not_released = True 
    if obj.x > 0 and obj.x <= screenCanvas.winfo_width() and obj.y > 0 and obj.y <= screenCanvas.winfo_height()\
        and selected_tile_data[tab] != None:
        if screentiles[(oyt*32)+xt] == selected_tile_num[tab] and last_tile_printed > -1:
            return
        screentiles[(oyt*32)+xt] = selected_tile_num[tab]
        xp = 0
        while xp < 8:
            yp = 0
            while yp < 8:
                paint = convertIntColorToHex(integerPalette[selected_tile_data[tab][(yp*8)+xp]])
                screenCanvas.itemconfig(screenpixels[(tab*32*64*8)+(yt*32*64)+(xt*64)+(yp*8)+xp], fill=paint)
                yp += 1
            xp += 1
    global no_changes_made
    no_changes_made = False
    last_tile_printed = (oyt*32)+xt


def refresh_whole_screen():
    loadingt = screenCanvas.create_text(300,200, text='Refreshing...', fill='black', font=('Times New Roman',24))
    loadings = screenCanvas.create_text(302,202, text="Refreshing...", fill='white', font=('Times New Roman',24))
    screenCanvas.update_idletasks()
    i = 0
    while i < 3:
        xt = 0
        while xt < 32:
            yt = 0
            while yt < 8:
                tilepaint = screentiles[(i*256)+(yt*32)+xt]
                tiletopaint = tile_data[(i*256)+tilepaint]
                if tiletopaint == []:
                    RedrawScreenGrid(0)
                    screenCanvas.delete(loadingt)
                    screenCanvas.delete(loadings)
                    return
                xp = 0
                while xp < 8:
                    yp = 0
                    while yp < 8:
                        paint = convertIntColorToHex(integerPalette[tiletopaint[(yp*8)+xp]])
                        screenCanvas.itemconfig(screenpixels[(i*32*64*8)+(yt*32*64)+(xt*64)+(yp*8)+xp], fill=paint)
                        yp += 1 #y pixel
                    xp += 1 #x pixel
                yt += 1
            xt += 1 #tile
        i += 1 #tab
    RedrawScreenGrid(0)
    screenCanvas.delete(loadingt)
    screenCanvas.delete(loadings)
last_tile_erased = -1

def erase_tile(obj):
    global last_tile_used
    global button_not_released
    last_tile_used = -1
    if loaded_tiles == False:
        return 
    xt = math.floor(obj.x / (screenScale*8))
    yt = math.floor(obj.y / (screenScale*8))
    oyt = yt
    tab = 0
    global last_tile_erased
    if (oyt*32)+xt == last_tile_erased:
        return
    if yt > 7:
        yt -= 8
        tab += 1
    if yt > 7:
        yt -= 8
        tab += 1
    if button_not_released == False: 
        add_undo_point()
        button_not_released = True 
    screentiles[(oyt*32)+xt] = 0
    if obj.x > 0 and obj.x <= screenCanvas.winfo_width() and obj.y > 0 and obj.y <= screenCanvas.winfo_height():
        #and selected_tile_data[tab] != None:
        if screentiles[(oyt*32)+xt] == tile_data[(tab*256)+0] and last_tile_erased > -1:
            return
        xp = 0
        while xp < 8:
            yp = 0
            while yp < 8:
                paint = convertIntColorToHex(integerPalette[tile_data[(tab*256)+0][(yp*8)+xp]])
                screenCanvas.itemconfig(screenpixels[(tab*32*64*8)+(yt*32*64)+(xt*64)+(yp*8)+xp], fill=paint)
                yp += 1
            xp += 1
    global no_changes_made
    no_changes_made = False


def select_tile0(obj):
    select_tile(0, obj.x, obj.y)
def select_tile1(obj):
    select_tile(1, obj.x, obj.y)
def select_tile2(obj):
    select_tile(2, obj.x, obj.y) 

selected_tile_data = []
selected_tile_num = []
i = 0
while i < 3:
    selected_tile_data.append(None)
    selected_tile_num.append(None)
    i += 1

def select_tile(tilepalnum, xpos, ypos):
    xt = math.floor(xpos/(iconScale*8))
    yt = math.floor(ypos/(iconScale*8))
    global selected_tile_data
    global selected_tile_num
    selected_tile_data[tilepalnum] = tile_data[(tilepalnum*256)+(yt*32)+xt]
    selected_tile_num[tilepalnum] = (yt*32)+xt 
    DrawTileSelector(tilepalnum, xt, yt)

tile_selector = []
i = 0
while i < 3:
    tile_selector.append(None)
    i += 1

def EraseTileSelectors():
    global tile_selector
    i = 0
    while i < 3:
        tilePalettes[i].delete(tile_selector[i])
        i += 1

def DrawTileSelector(tilepal, x, y):
    global tile_selector
    if tile_selector[tilepal] != None:
        tilePalettes[tilepal].delete(tile_selector[tilepal])
    tox = x * (tileSize*iconScale)
    toy = y * (tileSize*iconScale)
    tile_selector[tilepal] = tilePalettes[tilepal].create_rectangle(tox, toy, tox+(tileSize*iconScale), toy+(tileSize*iconScale), width=2, outline='white')

area_selector = None
selection_size = (0,0) 

def DrawAreaSelector(x, y, w=1, h=1):
    #default size 1, 1 
    global area_selector
    if area_selector != None:
        screenCanvas.delete(area_selector)
    sx = x * (tileSize*screenScale)
    sy = y * (tileSize*screenScale)
    tx = sx + (tileSize*screenScale*w)
    ty = sy + (tileSize*screenScale*h)
    area_selector = screenCanvas.create_rectangle(sx, sy, tx, ty, width=2, outline='white')
    global selection_size 
    selection_size = (w, h)
    return

tile_pal_grid = []
i = 0
while i < 3:
    blank = []
    tile_pal_grid.append(blank)
    i += 1

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
            tile_pal_grid[i].append(tilePalettes[i].create_line(x*(tileSize*iconScale), 0, x*(tileSize*iconScale), (iconScale*tileSize*8), fill='grey'))
            x += 1
        y = 0 
        while y < 24:
            tile_pal_grid[i].append(tilePalettes[i].create_line(0, y*(tileSize*iconScale), (tileSize*iconScale*32), y*(tileSize*iconScale), fill='grey'))
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

screen_grid = []

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
        screenCanvas.bind("<ButtonRelease-1>", RedrawScreenGrid)
        screenCanvas.bind("<ButtonRelease-3>", RedrawScreenGrid)
        screenCanvas.bind("<ButtonRelease-1>", set_undo_release, "+")
        screenCanvas.bind("<ButtonRelease-3>", set_undo_release, "+")
    # then clear it
    screenCanvas.delete("all")
    # set pos 
    screenCanvas.grid(row=3, column=3, rowspan=10, columnspan=10)
    # and draw 32x24 grid
    x = 0
    while x < 32:
        screen_grid.append(screenCanvas.create_line(x*(screenScale*tileSize), 0, x*(screenScale*tileSize), (tileSize*screenScale*24), fill='grey'))
        x += 1
    y = 0
    while y < 24:
        if y % 8 == 0:
            screen_grid.append(screenCanvas.create_line(0, y*(screenScale*tileSize), (tileSize*screenScale*32), y*(screenScale*tileSize), fill='grey', width=2))    
        else:
            screen_grid.append(screenCanvas.create_line(0, y*(screenScale*tileSize), (tileSize*screenScale*32), y*(screenScale*tileSize), fill='grey'))
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

def RedrawScreenGrid(ob):
    d = 0
    while d < (32+24):
        screenCanvas.tag_raise(screen_grid[d])
        d += 1

def RedrawTileGrid():
    i = 0
    while i < 3:
        d = 0
        while d < (32+24):
            tilePalettes[i].tag_raise(tile_pal_grid[i][d])
            d += 1
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
    RedrawTileGrid()


def import_m2p():
    global m2pfilename 
    m2pfilename = ''
    f = None 
    z = None 
    m2pfilename = tk.filedialog.askopenfilename(title='Load MSX2 Spriter file', filetypes=( ('MSX2 Spriter pattern file', '*.m2p'),('All files', '*.*') ))
    if m2pfilename == '' or type(m2pfilename) == tuple:
        return
    else:
        inbuffer = 'm2p'
        zipped = False 
        try:
            if zipfile.is_zipfile(m2pfilename):
                zipped = True
                z = zipfile.ZipFile(m2pfilename)
                f = z.open(inbuffer, 'r')
                data = f.readline().decode("utf-8")
            else:
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
                    if zipped:
                        data = f.readline().decode("utf-8").split(',')
                    else:
                        data = f.readline().split(',')
                    #tdat = data.split(',')
                    p = 0
                    while p < 64:
                        data[p] = int(data[p])
                        p += 1
                    tile_data[(n*256)+s] = data
                    s += 1
                selected_tile_data[n] = []
                n += 1
            EraseTileSelectors()
            LoadTileIcons()
            global loaded_tiles
            loaded_tiles = True 
        except IOError:
            messagebox.showerror("I/O error", message="Failed to load file. Check drives and permissions and try again.")
        #except:
        #    messagebox.showerror("Unexpected error", message="Unknown error loading file. Ensure the file is a proper M2P file.")
        finally:
            if(f):
                f.close()
            if(z):
                z.close()
    refresh_whole_screen()

def launch_app():
    global win 
    global undo_history
    global redo_history
    if win == None:
        win = tk.Frame(master=app, width=800, height=600)
        win.grid(row=32, columnspan=32)
    undo_history = []
    redo_history = []
    # open screen draw window
    InitScreenWindow()
    # open 3x tile palettes
    InitTilePalettes() 

no_changes_made = True 
saved = False

def client_exit():
    global no_changes_made
    if no_changes_made == True:
        sys.exit()
    else:
        result = messagebox.askquestion("Quit", "Save changes before quit?", icon='warning', type='yesnocancel')
        if result == 'yes':
            global saved 
            saved = False 
            save_normal()
            if saved == True:
                sys.exit()
            else:
                global filename 
                filename = ''
                return 
        elif result == 'no':
            sys.exit()
        elif result == 'cancel':
            return

def new_screen():
    global loaded_tiles 
    global undo_history
    global redo_history
    if loaded_tiles == False:
        messagebox.showwarning("No patterns loaded", message='No pattern file imported!\nOpening import pattern dialog.', type='ok')
        import_m2p()
    else:  
        resp = messagebox.askyesno('Load new pattern?', message='Select Yes to load a different M2P file,\nor No to use the same patterns.', type='yesno')
        if resp == True:
            import_m2p()
        else:
            pass
    if loaded_tiles == False:
        messagebox.showwarning('No pattern loaded', message="You can't draw without\nloading a pattern file!")
        return # because they cancelled.
    screentiles = []
    i = 0
    while i < (256*3):
        screentiles.append(0)
        i += 1
    undo_history = []
    redo_history = []
    refresh_whole_screen()
    return 

def load_m2c():
    # ask to change imported m2p
    # if none is imported, show warning
    global loaded_tiles
    global undo_history
    global redo_history
    if loaded_tiles == False:
        messagebox.showwarning("No patterns loaded", message='No pattern file imported!\nOpening import pattern dialog.', type='ok')
        import_m2p()
    else:  
        resp = messagebox.askyesno('Load new pattern?', message='Select Yes to load a different M2P file,\nor No to use the same patterns.', type='yesno')
        if resp == True:
            import_m2p()
        else:
            pass
    if loaded_tiles == False:
        return # because they cancelled.
    global m2cfilename
    m2cfilename = tk.filedialog.askopenfilename(title='Load MSX2 Screener file', filetypes=( ('MSX2 Screener screen file', '*.m2c'),('All files', '*.*') ))
    if m2cfilename == '' or type(m2cfilename) == tuple:
        return
    f = None 
    z = None 
    #zipped = False 
    inbuffer = 'm2c'
    try:
        if zipfile.is_zipfile(m2cfilename):
            #zipped = True 
            z = zipfile.ZipFile(m2cfilename)
            f = z.open(inbuffer, 'r')
            indata = f.readline().decode("utf-8")
        else:
            f = open(m2cfilename, 'r')
            indata = f.readline()
        #indata = f.readline()
        indata = indata.split(',')
        indata.pop()
        global screentiles
        ## remove this?
        i = 0
        while i < (256*3):
            screentiles[i] = int(indata[i])
            i += 1
        undo_history = []
        redo_history = []
        refresh_whole_screen()
    except IOError:
        messagebox.showerror("Load failed", message="I/O error loading file. Check drive and permissions and try again.")
    except:
        messagebox.showerror("Load failed", message="Unknown error loading file. This might be a bug!")
    finally:
        if f != None:
            f.close()
        if(z):
            z.close()
    # now that tiles are confirmed, open m2c dialog

def export_z80():
    global z80filename
    z80filename = tk.filedialog.asksaveasfilename(title='Save z80 screen data file', filetypes=( ('z80 screen data file', '*.z80'),('All files', '*.*') ))
    if z80filename == '' or type(z80filename)==tuple:
        return
    if z80filename[-4:].upper() != '.Z80':
        z80filename = z80filename + '.z80'
   
    outdata = []
    outdata.append("; Created with MSX2 Screener")
    outdata.append("; ")
    i = 0
    while i < 96:
        outstr = ' DB  '
        j = 0
        while j < 8:
            outstr = outstr + '${:02x}, '.format(screentiles[(i*8)+j])
            j += 1
        outstr = outstr[:-2]
        outdata.append(outstr)
        i += 1

    f = None 
    try:
        f = open(z80filename, 'w')
        for s in outdata:
            f.write(s)
            f.write('\n')
        messagebox.showinfo('Export OK', message='Z80 data file exported successfully.')
    except IOError:
        messagebox.showerror("Export failed", message="I/O error exporting file. Check drive and permissions and try again.")
    except:
        messagebox.showerror("Export failed", message="Unknown error exporting file. This might be a bug!")
    finally:
        if f != None:
            f.close()


def save_m2c():
    global m2cfilename
    # save with global filename already set.
    # it's just a csv of 768 values.
    f = None
    z = None 
    outbuffer = 'm2c'
    try:
        f = open(outbuffer, 'w')
        #f = open(m2cfilename, 'w')
        for s in screentiles:
            f.write(str(s) +',')
        f.close()
        with zipfile.ZipFile(m2cfilename, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(outbuffer)
        global saved 
        saved = True 
        messagebox.showinfo("Save OK", message='Save successful!')
    except IOError:
        messagebox.showerror("Save failed", message="I/O error saving file. Check drive and permissions and try again.")
    except:
        messagebox.showerror("Save failed", message="Unknown error saving file. This might be a bug!")
    finally:
        os.remove('m2c')
        #if f != None:
        #    f.close()

def save_normal():
    global m2cfilename
    if m2cfilename == '':
        save_as()
    else:
        save_m2c()

def save_as():
    global m2cfilename
    m2cfilename = tk.filedialog.asksaveasfilename(title='Save MSX2 Screener file', filetypes=( ('MSX2 Screener screen file', '*.m2c'),('All files', '*.*') ))
    if m2cfilename == '' or type(m2cfilename)==tuple:
        return
    if m2cfilename[-4:].upper() != '.M2C':
        m2cfilename = m2cfilename + '.m2c'
    save_m2c()

def open_about():
    messagebox.showinfo(title='About', message='MSX2 Screener tool v1.2\n(c)2019 Ben Ferguson\nAll rights reserved n such.(Created in Python!)\n\nInfo link: https://github.com/bferguson3/msx2spriter')

topleft_sel = -1

def start_selection(obj):
    x = math.floor(obj.x/(screenScale*tileSize))
    y = math.floor(obj.y/(screenScale*tileSize))
    ti = (y*32)+x 
    global topleft_sel 
    topleft_sel = ti 
    DrawAreaSelector(x, y)
    return 

def drag_selection(obj):
    x = math.floor(obj.x/(screenScale*tileSize))
    y = math.floor(obj.y/(screenScale*tileSize))
    ti = (y*32)+x 
    global topleft_sel 
    if ti != topleft_sel:
        ax = topleft_sel % 32
        ay = math.floor(topleft_sel/32)
        tx = x-ax+1
        ty = y-ay+1
        if tx < 1:
            tx = 1
        if ty < 1:
            ty = 1
        DrawAreaSelector(ax, ay, tx, ty) 
    return

copy_size = (0,0)
copy_buffer = []

def copy_selection():
    global topleft_sel
    global selection_size
    #top left is tile number
    #selection size is tiles wide and high (x,y)
    global copy_size
    global copy_buffer
    global screentiles
    copy_buffer = []
    copy_size = selection_size
    i = 0
    while i < copy_size[1]: #y size
        j = 0
        while j < copy_size[0]: #x size
            copy_buffer.append(screentiles[topleft_sel+(i*32)+j])
            j += 1
        i += 1
    #print(copy_buffer)
    return

def cut_selection():
    global topleft_sel
    global selection_size
    global copy_size
    global copy_buffer
    global screentiles
    global no_changes_made
    no_changes_made = False
    add_undo_point()
    copy_buffer = []
    copy_size = selection_size
    i = 0
    while i < copy_size[1]: #y size
        j = 0
        while j < copy_size[0]: #x size
            copy_buffer.append(screentiles[topleft_sel+(i*32)+j])
            screentiles[topleft_sel+(i*32)+j] = 0
            j += 1
        i += 1
    refresh_whole_screen()


def paste_selection():
    global topleft_sel
    global copy_size 
    global copy_buffer 
    global screentiles
    col = topleft_sel % 32 
    add_undo_point()
    i = 0
    while i < copy_size[1]:
        j = 0
        while j < copy_size[0]:
            if topleft_sel + (i*32) + j < len(screentiles):
                if col + j < 32:
                    screentiles[topleft_sel + (i*32) + j] = copy_buffer[(i*copy_size[0])+j]
            j += 1
        i += 1
    refresh_whole_screen()
    return

def draw_mode():
    global selbutton
    global pxbutton
    global interface_mode
    global area_selector
    interface_mode = 'DRAW'
    pxbutton.configure(relief=tk.SUNKEN)
    selbutton.configure(relief=tk.RAISED)
    screenCanvas.bind("<Button-1>", draw_tile)
    screenCanvas.bind("<B1-Motion>", draw_tile)
    screenCanvas.bind("<Button-3>", erase_tile)
    screenCanvas.bind("<B3-Motion>", erase_tile)
    screenCanvas.bind("<ButtonRelease-1>", RedrawScreenGrid)
    screenCanvas.bind("<ButtonRelease-3>", RedrawScreenGrid)
    screenCanvas.bind("<ButtonRelease-1>", set_undo_release, "+")
    screenCanvas.bind("<ButtonRelease-3>", set_undo_release, "+")
    if area_selector != None:
        screenCanvas.delete(area_selector)
    editMenu.entryconfigure(0, state=tk.DISABLED)
    editMenu.entryconfigure(1, state=tk.DISABLED)
    editMenu.entryconfigure(2, state=tk.DISABLED)
    global cutbutton 
    global copybutton 
    global pastebutton 
    cutbutton.configure(state=tk.DISABLED)
    copybutton.configure(state=tk.DISABLED)
    pastebutton.configure(state=tk.DISABLED)
    return
def select_mode():
    global selbutton
    global pxbutton
    global interface_mode
    interface_mode = 'SELECT'
    pxbutton.configure(relief=tk.RAISED)
    selbutton.configure(relief=tk.SUNKEN)
    screenCanvas.bind("<Button-1>", start_selection)
    screenCanvas.bind("<B1-Motion>", drag_selection)
    screenCanvas.unbind("<Button-3>")#, erase_tile)
    screenCanvas.unbind("<B3-Motion>")#, erase_tile)
    screenCanvas.unbind("<ButtonRelease-1>")#, RedrawScreenGrid)
    screenCanvas.unbind("<ButtonRelease-3>")#, RedrawScreenGrid)
    editMenu.entryconfigure(0, state=tk.NORMAL)
    editMenu.entryconfigure(1, state=tk.NORMAL)
    editMenu.entryconfigure(2, state=tk.NORMAL)
    global cutbutton 
    global copybutton 
    global pastebutton 
    cutbutton.configure(state=tk.NORMAL)
    copybutton.configure(state=tk.NORMAL)
    pastebutton.configure(state=tk.NORMAL)
    
    return 

def kb_monitor(obj):
    if obj.state & 4 == 4:
        if obj.keysym == 'c':
            copy_selection()
            return
        elif obj.keysym == 'v':
            paste_selection()
            return
        elif obj.keysym == 'x':
            cut_selection()
        elif obj.keysym == 'z':
            undo_last()
        elif obj.keysym == 'y':
            redo_last()
        elif obj.keysym == 's':
            save_normal()

    
menuBar = tk.Menu(app)
fileMenu = tk.Menu(menuBar, tearoff=0)
editMenu = tk.Menu(menuBar, tearoff=0)
helpMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label='New screen file', command=new_screen) #also ask to change m2p
fileMenu.add_command(label="Save (Ctrl+S)", command=save_normal)
fileMenu.add_command(label="Save as .M2C file...", command=save_as)
fileMenu.add_command(label="Load .M2C file...", command=load_m2c) #ask to change m2p
fileMenu.add_command(label="Export as z80 screen data...", command=export_z80)
fileMenu.add_separator()
fileMenu.add_command(label='Import .M2P patterns...', command=import_m2p) #do not change m2c!
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=client_exit)
editMenu.add_command(label="Cut (Ctrl+X)", command=cut_selection, state=tk.DISABLED)
editMenu.add_command(label="Copy (Ctrl+C)", command=copy_selection, state=tk.DISABLED)
editMenu.add_command(label="Paste (Ctrl+V)", command=paste_selection, state=tk.DISABLED)
editMenu.add_separator()
editMenu.add_command(label="Undo (Ctrl+Z)", command=undo_last)
editMenu.add_command(label="Redo (Ctrl+Y)", command=redo_last)
editMenu.add_separator()
editMenu.add_command(label='Configure RMB...', state=tk.DISABLED)
helpMenu.add_command(label='About...', command=open_about)
menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label='Edit', menu=editMenu)
menuBar.add_cascade(label='Help', menu=helpMenu)
toolbar = tk.Frame(win, width=600, height=30, relief=tk.RAISED)
savebutton = tk.Button(toolbar, image=save_icon, width=20, height=20, command=save_normal)
pxbutton = tk.Button(toolbar, image=dotbmp, width=20, height=20, relief=tk.SUNKEN, command=draw_mode)
selbutton = tk.Button(toolbar, image=boxbmp, width=20, height=20, command=select_mode)
cutbutton = tk.Button(toolbar, image=cut_icon, width=20, height=20, command=cut_selection, state=tk.DISABLED)
copybutton = tk.Button(toolbar, image=copy_icon, width=20, height=20, command=copy_selection, state=tk.DISABLED)
pastebutton = tk.Button(toolbar, image=paste_icon, width=20, height=20, command=paste_selection, state=tk.DISABLED)
undobutton = tk.Button(toolbar, image=undo_icon, width=20, height=20, command=undo_last)
redobutton = tk.Button(toolbar, image=redo_icon, width=20, height=20, command=redo_last)

savebutton.grid(row=0,column=0)
pxbutton.grid(row=0, column=1, padx=(20,0))
selbutton.grid(row=0,column=2)
cutbutton.grid(row=0, column=3, padx=(20,0))
copybutton.grid(row=0,column=4)
pastebutton.grid(row=0,column=5)
undobutton.grid(row=0, column=6, padx=(20,0))
redobutton.grid(row=0,column=7)


toolbar.grid(row=0)
app.config(menu=menuBar) 

app.bind("<Key>", kb_monitor)

launch_app()
# Run the app
app.resizable(False, False)
app.protocol("WM_DELETE_WINDOW", client_exit)
tk.Label(win, text='Screen view:').grid(row=2, column=1, columnspan=3)
tk.Label(win, text='Pattern 0').grid(row=2, column=15, columnspan=3)
tk.Label(win, text='Pattern 1').grid(row=5, column=15, columnspan=3)
tk.Label(win, text='Pattern 2').grid(row=8, column=15, columnspan=3)

app.mainloop()
