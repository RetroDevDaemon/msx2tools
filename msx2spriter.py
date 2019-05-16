#########################################################
# MSX2 Spriter
#
# (c) 2019 Ben Ferguson
#  (w/contributions from jlbeard83)
# Use Python 3! (Coded in 3.7.1)
# 
# v1.28: Added icons and flip h/v.
#           
# Assembles z80 byte data for GRAPHIC3 (screen 4)
#  / sprite M2 and pattern graphics for use with compilers.
# Easy point-and-click interface.
# 
##########################################################

# Imports 
import tkinter as tk
import sys 
import math 

patternMode = False

## button bitmaps
drawpx_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0x00, 0x10, 0x00, 0x28, 0x00, 0x5c, 0x00, 0x2e, 0x00, 0x17, 0x80, 0x0b, 0xc0, 0x05, 0xe0, 0x02, 0x70, 0x01, 0xb8, 0x00, 0x54, 0x00, 0x24, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00
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

horiz_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xfe, 0x7f, 0x56, 0x40, 0xaa, 0x40, 0x56, 0x40, 0xaa, 0x50, 0x0e, 0x70, 0xff, 0xff, 0x0e, 0x70, 0xaa, 0x50, 0x56, 0x40, 0xaa, 0x40, 0x56, 0x40, 0xaa, 0x40, 0xfe, 0x7f, 0x00, 0x00
};
"""

vert_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x01, 0xfe, 0x7f, 0xaa, 0x6b, 0xd6, 0x57, 0x2a, 0x69, 0x56, 0x55, 0x2a, 0x69, 0x56, 0x55, 0x02, 0x41, 0x02, 0x41, 0x02, 0x41, 0x02, 0x41, 0xc2, 0x47, 0x82, 0x43, 0xfe, 0x7f, 0x00, 0x01
};
"""
save_icon_data = """
#define im_width 16
#define im_height 16
static char im_bits[] = {
0x00, 0x00, 0xfc, 0x3f, 0x1e, 0x78, 0x5e, 0x78, 0x5e, 0x78, 0x1e, 0x78, 0xfe, 0x7f, 0xfe, 0x7f, 0x7e, 0x7e, 0xbe, 0x7d, 0xbe, 0x7c, 0x7e, 0x7e, 0xfe, 0x7f, 0xfe, 0x6f, 0xfc, 0x3f, 0x00, 0x00
};
"""


## GLOBALS - MUST BE REFD IN INIT DEF
r0 = None 
r1 = None 
s0 = None
s1 = None 
l0 = None 
l1 = None 
l2 = None 
l3 = None 
buu = None
bdd = None 
win = None
bl = None 
br = None 
bu = None 
bd = None
sr = None 
sl = None 
su = None 
sd = None
smallpixels1 = []
smallpixels2 = []
smallpixels3 = []
smallpixels4 = []
palette_display = []
smallpatternpx = []
intpal = [] 
pixelSize = 16
spriteSize = 16
icon_selected = 0
pattern_y_ofs = 0
pattern_x_ofs = 0
pattern_page = 0
page_ofs = 0
iconwidth = 128
iconcanvascolumn = 8
last_pixel_colored = -1
copybuffer = None
last_color_used = -1

# MSX2 default 16-color palette, in integer strings
defaultIntegerPalette = [
    '000', '000', '161', '373',
    '117', '237', '511', '267',
    '711', '733', '661', '664',
    '141', '625', '555', '777'
]
##

# Each above integer must be divided by 7 then converted to hex.
displayPalette = []

# TK Setup
app = tk.Tk()
app.title('MSX2 Spriter')

drawpx_icon = tk.BitmapImage(data=drawpx_data)
cut_icon = tk.BitmapImage(data=cut_icon_data)
copy_icon = tk.BitmapImage(data=copy_icon_data)
paste_icon = tk.BitmapImage(data=paste_icon_data)
undo_icon = tk.BitmapImage(data=undo_icon_data)
redo_icon = tk.BitmapImage(data=redo_icon_data)
horiz_icon = tk.BitmapImage(data=horiz_icon_data)
vert_icon = tk.BitmapImage(data=vert_icon_data)
save_icon = tk.BitmapImage(data=save_icon_data)

# First, convert the integer palette to hexadecimal palette.    
def convert_int_pal_to_hex(integerPalette):
    global displayPalette
    displayPalette = None
    displayPalette = []
    i = 0
    while i < 16:
        if integerPalette[i] == 'trans':
            integerPalette[i] = '000'
        tempPalVals = []
        tempPalVals.append('#')
        a = math.floor((int(integerPalette[i][:-2]) / 7) * 255)
        tempPalVals.append(hex(a)[2:])
        if a == 0:
            tempPalVals.append('0')
        a = math.floor((int(integerPalette[i][1:-1]) / 7) * 255)
        tempPalVals.append(hex(a)[2:])
        if a == 0:
            tempPalVals.append('0')
        a = math.floor((int(integerPalette[i][2:]) / 7) * 255)
        tempPalVals.append(hex(a)[2:])
        if a == 0:
            tempPalVals.append('0')
        displayPalette.append(tempPalVals)
        displayPalette[i] = ''.join(displayPalette[i])
        i += 1
 #

# To convert HTML color back to 3-bit RGB values
def convert_hex_pal_to_binary():
    return 0


# some globals
numSel = 0
currentColor = '000'
is_drawing_held = False
mask = tk.IntVar()
mask.set(1)
currentPalNo = 0

# Stop global drawing toggle
def stop_draw(ob):
    global is_drawing_held
    is_drawing_held = False

# Do I still need these?
app.bind("<ButtonRelease-1>", stop_draw)

# Converts a 3-bit RGB string value (e.g. 111) to html hex (e.g. #242424)
def single_intcol_to_hex(col):
    #global currentColor
    if col[:-2] == 'tra':
        return '#000000'
    a = math.floor((int(col[:-2]) / 7) * 255)
    b = hex(a)[2:]
    if b == '0':
        b = '00'
    c = math.floor((int(col[1:-1]) / 7) * 255)
    d = hex(c)[2:]
    if d == '0':
        d = '00'
    e = math.floor((int(col[2:]) / 7) * 255)
    f = hex(e)[2:]
    if f == '0':
        f = '00'
    ret = '#'
    ret += b 
    ret += d 
    ret += f
    return ret 

# for screener, selectioncanvas will be a new class.
# for spriter, is faster to just redraw.

# Define the palette button class
class PaletteButton(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.lbl = 0
        self.lbl2 = 0
        self.selector=[]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.clicked)
    
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
        global currentColor
        global currentPalNo
        currentColor = self.myVal
        i = 0
        while i < 16:
            if palette_display[i] == self:
                currentPalNo = i
                break
            i += 1
        # set widget texts:
        global pal_mod
        set_text(pal_mod[0], currentColor[:-2])
        set_text(pal_mod[1], currentColor[1:-1])
        set_text(pal_mod[2], currentColor[2:])
        # assign global selector variable to whoever I am
        global numSel 
        c = 0
        while c < 16:
            if palette_display[c] == self:
                numSel = c 
                break
            c += 1 
         #
 #

# Need a method to delete/insert
def set_text(obj, text):
    obj.delete(0,tk.END)
    obj.insert(0,text)
    return

# Just in case, have a deselect all function
def unclick_all():
    b = 0
    while b < len(palette_display):
        palette_display[b].unclicked()
        b += 1
 #
# Button size
scale = 30

# Display the palette and add it to the canvas.

def add_palette_display():
    global palette_display
    palette_display = []
    i = 0
    while i < 16:
        palette_display.append(PaletteButton(win, width=scale, height=scale, background=displayPalette[i]))
        palette_display[i].grid(row=1, column=i+1)
        palette_display[i].setVal(intpal[i])
        #if i == 0:
        #    palette_display[i].myVal = 'trans'
        i += 1

# Refreshes the palette colors
def updatePaletteDisplay():
    i = 0
    global palette_display
    global displayPalette
    while i < 16:
        palette_display[i].configure(background=displayPalette[i])
        palette_display[i].setVal(intpal[i])
        #if i == 0:
        #    palette_display[i].myVal = 'trans'
        i += 1
    return 

# Updates the current palette to the inputted values
def applyColorToSel():
    # 1) ensure input values are between 0-7 
    global currentColor
    oldcol = single_intcol_to_hex(currentColor)
    if oldcol != intpal[0]:
        i = 0
        while i < 3:
            if float(pal_mod[i].get()) < 0:
                set_text(pal_mod[i], '0')
            elif float(pal_mod[i].get()) > 7:
                set_text(pal_mod[i], '7')
            i += 1
        # 2) set the RGB values into intpal[selnum]
        i = 0
        intpal[numSel] = ''
        while i < 3:
            intpal[numSel] += pal_mod[i].get()
            i += 1
        convert_int_pal_to_hex(intpal) # assigns to display palette
        updatePaletteDisplay()
        currentColor = intpal[numSel]
        paintcol = single_intcol_to_hex(currentColor)
        find_and_replace_pixels(oldcol, paintcol)
        refresh_display(True)
    #return


# Changes all color of type x to type y 
def find_and_replace_pixels(oldcolor, newcolor):
    for n in pixels:
        if drawCanvas.itemcget(n, 'fill') == oldcolor:
            drawCanvas.itemconfig(n, fill=newcolor)
    #return

# Changes the palette back to the default and re-paints image
def resetSelectedColor():
    global currentColor
    oldcol = single_intcol_to_hex(currentColor)
    if oldcol != intpal[0]:#'grey':
        intpal[numSel] = defaultIntegerPalette[numSel]
        convert_int_pal_to_hex(intpal)
        currentColor = intpal[numSel]
        paintcol = single_intcol_to_hex(currentColor)
        updatePaletteDisplay()
        find_and_replace_pixels(oldcol, paintcol)
    refresh_display(True)
    #return

pal_mod = []

def add_labels_andpalmod():
    global win 
    global pal_mod
    # Add palette modifier functions to the canvas.
    # and their labels
    tk.Label(win, text='Color R:').grid(row=2, column=2, columnspan=2)
    tk.Label(win, text='G:').grid(row=2, column=4, columnspan=2)
    tk.Label(win, text='B:').grid(row=2, column=6, columnspan=2)
    # and their buttons.
    tk.Button(win, text='Apply', command=applyColorToSel).grid(row=2, column=9, columnspan=2)
    tk.Button(win, text='Reset', command=resetSelectedColor).grid(row=2, column=11, columnspan=2)
    pal_mod = []
    i = 0
    j = 0
    while j < 6:
        e = tk.Entry(win, width=2)
        pal_mod.append(e)
        pal_mod[i].grid(row=2, column=j+3, columnspan=2)
        j += 2
        i += 1
 #

# Only 1 color per row in sprite mode 2!
def repaint_row(row):
    global currentColor
    i = 0
    while i < spriteSize:
        # TODO update 'grey' to transparent variable
        if mask.get() == 1:
            if pixels_mask1[(row*spriteSize)+i] != 0: 
                pixels_mask1[(row*spriteSize)+i] = currentPalNo
        if mask.get() == 2:
            if pixels_mask2[(row*spriteSize)+i] != 0:
                pixels_mask2[(row*spriteSize)+i] = currentPalNo    
        i += 1

last_mask = -1
button_not_released = False
# Actually paints the pixel and changes the pal number in the mask array
def color_pixel(ob):
    x_px = math.floor(ob.x/pixelSize) 
    y_px = math.floor(ob.y/pixelSize)
    global last_pixel_colored 
    global numSel
    global last_color_used
    global last_mask
    global button_not_released
    if last_pixel_colored == (y_px*spriteSize)+x_px and last_color_used == currentPalNo and last_mask == mask.get():
        return 
    if ob.x < 0 or ob.x >= (spriteSize*pixelSize) or ob.y < 0 or ob.y >= (spriteSize*pixelSize):
        return
    last_pixel_colored = (y_px*spriteSize) + x_px 
    if button_not_released == False: 
        add_undo_point(icon_selected)
        button_not_released = True 
    if patternMode == False:
        if mask.get() == 1:
            pixels_mask1[(y_px*spriteSize)+x_px] = currentPalNo
        if mask.get() == 2:
            pixels_mask2[(y_px*spriteSize)+x_px] = currentPalNo
        if numSel != 0:# and currentColor != intpal[0]:#if numSel != 0:#if currentColor != 'trans':
            repaint_row(y_px)
        maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        maskdata[page_ofs + (icon_selected*2)+1] = pixels_mask2.copy()
    else:
        prevcol = pixels_mask1[(y_px*spriteSize)+x_px]
        pixels_mask1[(y_px*spriteSize)+x_px] = currentPalNo 
        patterndata[icon_selected] = pixels_mask1.copy()
        repaint_pattern_row(y_px, prevcol)
        #a = 0
    if last_color_used == currentPalNo:
        refresh_display(False, last_pixel_colored)
    else:
        last_color_used = currentPalNo
        refresh_display(False, -1)
    last_mask = mask.get()
    

def get_palno_from_rgb(rgb):
    i = 1
    while i < 16:
        if intpal[i] == rgb:
            return i 
        i += 1
    return None

def repaint_pattern_row(yrow, prevcol):
    color1 = patterndata[icon_selected][(yrow*8)]
    color2 = None
    activecolor = currentPalNo#get_palno_from_rgb(currentColor) #single_intcol_to_hex(currentColor)

    threeflag = False 
    i = 0
    while i < 8:
        thispx = patterndata[icon_selected][(yrow*8)+i]
        if color2 == None:
            if thispx != color1:
                color2 = thispx 
        if color2 != None and thispx != color1 and thispx != color2:
            threeflag = True 
        i += 1
    if threeflag:
        # now search the row for every instance of prevcol and overwrite it with activecolor by changing patterndata[icon_selected].
        i = 0
        while i < 8:
            if patterndata[icon_selected][(yrow*8)+i] == prevcol:# and activecolor != None:
                if activecolor == None:
                    activecolor = 0
                pixels_mask1[(yrow*8)+i] = activecolor
                patterndata[icon_selected][(yrow*8)+i] = activecolor
            i += 1
    
def erase_pixel(ob):
    global currentColor
    global currentPalNo
    global numSel 
    oldp = currentPalNo
    oldc = currentColor + '.'
    olds = numSel
    currentColor = intpal[0]
    currentPalNo = 0
    numSel = 0
    color_pixel(ob)
    numSel = olds
    currentPalNo = oldp
    currentColor = oldc[:-1]
    

# Both layers enabled?
def update_orlayer(px = -1):
    global palette_display
    global pixels_mask1 
    global pixels_mask2 
    orpixels = pixels_mask1.copy()
    if px == -1:
        i = 0
        while i < (spriteSize*spriteSize):
            if orpixels[i] != 0 and pixels_mask2[i] != 0:
                orpixels[i] = orpixels[i] | pixels_mask2[i] 
            elif orpixels[i] == 0 and pixels_mask2[i] != 0:
                orpixels[i] = pixels_mask2[i] 
            topaint = single_intcol_to_hex(intpal[0])#'grey'
            cur_px = orpixels[i]
            stip = 'gray75'
            if cur_px != 0:#palette_display[cur_px].myVal != intpal[0]:#'trans'
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
                stip = ''
            drawCanvas.itemconfig(pixels[i], fill=topaint, stipple=stip)
            i += 1
    else:
        i = 0
        y = math.floor(px/spriteSize)
        while i < (spriteSize):
            tpx = (y*spriteSize)+i
            if orpixels[tpx] != 0 and pixels_mask2[tpx] != 0:
                orpixels[tpx] = orpixels[tpx] | pixels_mask2[tpx] 
            elif orpixels[tpx] == 0 and pixels_mask2[tpx] != 0:
                orpixels[tpx] = pixels_mask2[tpx] 
            topaint = single_intcol_to_hex(intpal[0])#'grey'
            cur_px = orpixels[tpx]
            stip = 'gray75'
            if cur_px != 0:#palette_display[cur_px].myVal != intpal[0]:#'trans'
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
                stip = ''
            drawCanvas.itemconfig(pixels[tpx], fill=topaint, stipple=stip)
            i += 1
    #return

# Just layer 2 enabled
def update_layermask_2(px = -1):
    i = 0
    global pixels_mask2
    global palette_display
    if px == -1:
        while i < (spriteSize*spriteSize):
            topaint = single_intcol_to_hex(intpal[0])#'grey'
            cur_px = pixels_mask2[i]
            stip = 'gray75'
            if cur_px != 0:#palette_display[cur_px].myVal != intpal[0]:#'trans'
                stip = ''
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
            drawCanvas.itemconfig(pixels[i], fill=topaint, stipple=stip)
            i += 1
    else:
        i = 0
        y = math.floor(px/spriteSize)
        while i < spriteSize:
            tpx = (y*spriteSize)+i
            topaint = single_intcol_to_hex(intpal[0])#'grey'
            cur_px = pixels_mask2[tpx]
            stip = 'gray75'
            if cur_px != 0:
                stip = ''
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
            drawCanvas.itemconfig(pixels[tpx], fill=topaint, stipple=stip)
            i += 1
    #return 

# Just layer 1 enabled
def update_layermask_1(px = -1):
    i = 0
    global pixels_mask1
    global palette_display
    if px == -1:
        while i < (spriteSize * spriteSize):
            topaint = single_intcol_to_hex(intpal[0])#'grey'
            cur_px = pixels_mask1[i]
            stip = 'gray75'
            if cur_px != 0:#palette_display[cur_px].myVal != intpal[0]:#'trans'
                stip = ''
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
            if patternMode == True:
                stip = ''
            drawCanvas.itemconfig(pixels[i], fill=topaint, stipple=stip)
            i += 1
    else:
        i = 0
        y = math.floor(px/spriteSize)
        while i < spriteSize:
            tpx = (y*spriteSize)+i
            topaint = single_intcol_to_hex(intpal[0])#'grey'
            cur_px = pixels_mask1[tpx]
            stip = 'gray75'
            if cur_px != 0:
                stip = ''
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
            if patternMode == True:
                stip = ''
            drawCanvas.itemconfig(pixels[tpx], fill=topaint, stipple=stip)
            i += 1
    #return 

drawCanvas = None
def init_draw_canvas():
    global drawCanvas
    global spriteSize
    global pixelSize 
    if drawCanvas != None: 
        drawCanvas.delete("all")
        drawCanvas.grid(row=3, column=0, columnspan=10, rowspan=10)
    else: 
    # Add sub-canvas for drawing, and palette value arrays
        drawCanvas = tk.Canvas(win, background='white', width=pixelSize*spriteSize, height=pixelSize*spriteSize)
        drawCanvas.grid(row=3, column=0, columnspan=10, rowspan=10)

# populate with pixel grid
pixels = []
# the mask arrays are actual PALETTE values 0-15.
pixels_mask1 = []
pixels_mask2 = []
def reset_pixels_display():
    global pixels 
    global pixels_mask1 
    global pixels_mask2 
    global pixelSize 
    global spriteSize 
    pixels = [] 
    pixels_mask1 = []
    pixels_mask2 = []
    i = 0
    while i < spriteSize:
        j = 0
        while j < spriteSize:
            #create_rectangle's
            pixels.append(drawCanvas.create_rectangle(j*pixelSize, i*pixelSize, (j+1)*pixelSize, (i+1)*pixelSize, outline='grey', fill=single_intcol_to_hex(intpal[0]), stipple='gray75'))
            pixels_mask1.append(0)
            pixels_mask2.append(0)
            j += 1
        i += 1
 #
 
# Radial bools have to be defined as tk variables
show_m1 = tk.BooleanVar()
show_m1.set(True)
show_m2 = tk.BooleanVar()
show_m2.set(True)

# Universally updates all 256 pixels
def refresh_display(allicons=False, px=-1):
    global patternMode 
    if show_m1.get() == True and show_m2.get() == True:
        update_orlayer(px)
    elif show_m1.get() == True and show_m2.get() == False:
        if patternMode == False:
            update_layermask_1(px)
        else:
            update_layermask_1()
    elif show_m2.get() == True and show_m1.get() == False:
        update_layermask_2(px)
    if allicons == False:
        global icon_selected 
        if patternMode == False:
            update_icon_window(icon_selected)
        else:
            update_icon_window()
    else:
        if patternMode == False:
            i = 0
            while i < 4:
                update_icon_window(i)
                i += 1
        else:
           update_pattern_icons()
 #
##

# set all 32 pages of mask data...
maskdata = []
templatepx = []
def reset_mask_data():
    global maskdata
    global templatepx
    maskdata = []
    templatepx = []
    i = 0
    while i < (spriteSize*spriteSize): #256
        templatepx.append(0)
        i += 1
    i = 0
    while i < 32:
        temp = templatepx.copy()
        maskdata.append(temp)
        i += 1

##
patterndata = []
def reset_pattern_data():
    global patterndata 
    global templatepx 
    patterndata = []
    templatepx = []
    i = 0 
    while i < (spriteSize*spriteSize): #64
        templatepx.append(0)
        i += 1
    i = 0
    while i < 768:
        temp = templatepx.copy()
        patterndata.append(temp)
        i += 1
##        

pattern_icon_selected = 0
spr_selector=[]
i = 0
while i < 4:
    spr_selector.append(None)
    i += 1

def draw_pattern_selector(icnum):
    global spr_selector
    if spr_selector[0] != None:
        i = 0
        while i < 4:
            iconCanvas.delete(spr_selector[i])
            i += 1
    tw = math.floor(iconwidth/8)
    xa = ((icnum % 8)) * tw + 2
    ya = math.floor(icnum/8) * tw + 2
    #if icnum >= 0 and icnum < 32:
    if pattern_x_ofs > ((icon_selected % 32) - 8) and pattern_x_ofs < ((icon_selected % 32) + 1)\
        and pattern_y_ofs > (math.floor(icon_selected/32) - 4) and pattern_y_ofs < (math.floor(icon_selected/32) + 1):
        spr_selector[0] = iconCanvas.create_line(xa+2, ya+2, xa+2, ya+tw+2, width=2, fill='white')
        spr_selector[1] = iconCanvas.create_line(xa+2, ya+2, xa+tw+2, ya+2, width=2, fill='white')
        spr_selector[2] = iconCanvas.create_line(xa+tw+2, ya+2, xa+tw+2, ya+tw+2, width=2, fill='white')
        spr_selector[3] = iconCanvas.create_line(xa+2, ya+tw+2, xa+tw+2, ya+tw+2, width=2, fill='white')

def draw_sprite_selector(sprnum):
    global spr_selector
    if spr_selector[0] != None:
        i = 0
        while i < 4:
            iconCanvas.delete(spr_selector[i])
            i += 1
    if sprnum == 0:
        xa = 0
        ya = 0
    elif sprnum == 1:
        xa = 64
        ya = 0
    elif sprnum == 2:
        xa = 0
        ya = 64
    elif sprnum == 3:
        xa = 64
        ya = 64
    spr_selector[0] = iconCanvas.create_line(xa+2, ya+2, xa+2, ya+64+2, width=2, fill='white')
    spr_selector[1] = iconCanvas.create_line(xa+2, ya+2, xa+64+2, ya+2, width=2, fill='white')
    spr_selector[2] = iconCanvas.create_line(xa+64+2, ya+2, xa+64+2, ya+64+2, width=2, fill='white')
    spr_selector[3] = iconCanvas.create_line(xa+2, ya+64+2, xa+64+2, ya+64+2, width=2, fill='white')


def select_from_icon(obj):
    global page_ofs
    global icon_selected
    global pixels_mask1
    global pixels_mask2
    global pattern_icon_selected
    # first, copy current pixel mask into maskdata[].
    if patternMode == False:
        if icon_selected == 0:
            maskdata[0+page_ofs] = pixels_mask1.copy()
            maskdata[1+page_ofs] = pixels_mask2.copy()
        elif icon_selected == 1:
            maskdata[2+page_ofs] = pixels_mask1.copy()
            maskdata[3+page_ofs] = pixels_mask2.copy()
        elif icon_selected == 2:
            maskdata[4+page_ofs] = pixels_mask1.copy()
            maskdata[5+page_ofs] = pixels_mask2.copy()
        elif icon_selected == 3:
            maskdata[6+page_ofs] = pixels_mask1.copy()
            maskdata[7+page_ofs] = pixels_mask2.copy()
    # now, copy maskdata back to drawn pixel mask.
        if (obj.x < 64) and (obj.y < 64):
            # selection top left 
            icon_selected = 0
            pixels_mask1 = maskdata[0+page_ofs].copy()
            pixels_mask2 = maskdata[1+page_ofs].copy()
        elif (obj.x > 64) and (obj.y < 64):
            icon_selected = 1
            pixels_mask1 = maskdata[2+page_ofs].copy()
            pixels_mask2 = maskdata[3+page_ofs].copy()
        elif (obj.x < 64) and (obj.y > 64):
            icon_selected = 2
            pixels_mask1 = maskdata[4+page_ofs].copy()
            pixels_mask2 = maskdata[5+page_ofs].copy()
        elif (obj.x > 64) and (obj.y > 64):
            icon_selected = 3
            pixels_mask1 = maskdata[6+page_ofs].copy()
            pixels_mask2 = maskdata[7+page_ofs].copy()
        update_label_txt()
        draw_sprite_selector(icon_selected)
    else:
        # PATTERN MODE!
        # copy current mask (pixels_mask1) into patterndata
        # then check position
        ## and set pixels_mask1 as patterndata[x].copy
        # use obj.x and obj.y 
        patterndata[icon_selected] = pixels_mask1.copy()
        if obj.x < iconCanvas.winfo_width()-6 and obj.y < iconCanvas.winfo_height()-6\
            and obj.x > 0 and obj.y > 0:
            sel_ptn = math.floor(obj.y/32) + pattern_y_ofs 
            sel_ptn = (sel_ptn*32) + math.floor(obj.x/32) + pattern_x_ofs 
            icon_selected = sel_ptn 
            pixels_mask1 = patterndata[sel_ptn].copy()
            pattern_icon_selected = math.floor(obj.x/32) + (math.floor(obj.y/32)*8)
            l0.configure(text='Pattern {}\nX: {} Y: {}'.format(sel_ptn, (math.floor(obj.x/32) + pattern_x_ofs), (math.floor(obj.y/32) + pattern_y_ofs) ))
            l1.configure(text="Table {} / 3".format(math.floor((icon_selected/256)+1)))
    refresh_display(False)


iconCanvas = None 
def init_icon_canvases():
    global iconcanvascolumn
    global iconCanvas
    if iconCanvas != None: 
        iconCanvas.delete("all")
        iconCanvas.configure(width=iconwidth+2,height=128+2)
        iconCanvas.grid(row=3, column=iconcanvascolumn, columnspan=8, rowspan=8)
    else:
        #iconCanvas = None 
        iconCanvas = tk.Canvas(win,background='grey',width=iconwidth+2,height=128+2)
        iconCanvas.grid(row=3, column=iconcanvascolumn, columnspan=8, rowspan=8)
        iconCanvas.bind("<Button-1>", select_from_icon)

def update_label_txt():
    global r0 
    global r1 
    global s0 
    global s1
    global l0 
    global l1
    global l2
    global l3
    if patternMode == False:
        global icon_selected
        global page_ofs 
        t = 'Mask {}'.format(str((icon_selected*2)+page_ofs))
        r0.config(text=t)
        t = 'Mask {}'.format(str((icon_selected*2)+1+page_ofs))
        r1.config(text=t)
        t = 'Show {}'.format(str((icon_selected*2)+page_ofs))
        s0.config(text=t)
        t = 'Show {}'.format(str((icon_selected*2)+1+page_ofs))
        s1.config(text=t)
        # also l0-l3
        t = '{} - {}'.format(str(page_ofs+0), str(page_ofs+1))
        l0.config(text=t)
        t = '{} - {}'.format(str(page_ofs+2), str(page_ofs+3))
        l1.config(text=t)
        t = '{} - {}'.format(str(page_ofs+4), str(page_ofs+5))
        l2.config(text=t)
        t = '{} - {}'.format(str(page_ofs+6), str(page_ofs+7))
        l3.config(text=t)
    #return 
smalsize = 4

def update_icon_window(win_no=None):
    global icon_selected
    global smallpixels1
    global smallpixels2
    global smallpixels3
    global smallpixels4
    if patternMode == False:
        # Both layers!
        global page_ofs 
        orpixels = maskdata[(win_no*2)+page_ofs].copy() 
        or2pixels = maskdata[(win_no*2)+page_ofs+1].copy()
        i = 0
        while i < (spriteSize*spriteSize):
            if orpixels[i] != 0 and or2pixels[i] != 0:
                orpixels[i] = orpixels[i] | or2pixels[i] 
            elif orpixels[i] == 0 and or2pixels[i] != 0:
                orpixels[i] = or2pixels[i] 
            #topaint = 'grey'
            topaint = single_intcol_to_hex(intpal[0])
            cur_px = orpixels[i]
            stip = 'gray25'
            if cur_px != 0:#palette_display[cur_px].myVal != intpal[0]:#'trans':
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
                stip = ''
            if win_no == 0:
                iconCanvas.itemconfig(smallpixels1[i], fill=topaint, stipple=stip)
            elif win_no == 1:
                iconCanvas.itemconfig(smallpixels2[i], fill=topaint, stipple=stip)
            elif win_no == 2:
                iconCanvas.itemconfig(smallpixels3[i], fill=topaint, stipple=stip)
            elif win_no == 3:
                iconCanvas.itemconfig(smallpixels4[i], fill=topaint, stipple=stip)
            i += 1
    else:
        # PATTERN MODE DRAWS!
        # need to reduce icon_selected by offsets.
        global pattern_y_ofs 
        global pattern_x_ofs 
        global pattern_icon_selected
        if (icon_selected >= (pattern_x_ofs+(pattern_y_ofs*32)) and icon_selected <= 7+(pattern_x_ofs+(pattern_y_ofs*32)))\
            or (icon_selected >= (pattern_x_ofs+(pattern_y_ofs*32))+32 and icon_selected <= 7+(pattern_x_ofs+(pattern_y_ofs*32))+32)\
            or (icon_selected >= (pattern_x_ofs+(pattern_y_ofs*32))+64 and icon_selected <= 7+(pattern_x_ofs+(pattern_y_ofs*32))+64)\
            or (icon_selected >= (pattern_x_ofs+(pattern_y_ofs*32))+96 and icon_selected <= 7+(pattern_x_ofs+(pattern_y_ofs*32))+96):
            i = 0
            while i < spriteSize*spriteSize:
                cur_px = patterndata[icon_selected][i]
                intval = palette_display[cur_px].myVal
                topaint = single_intcol_to_hex(intval)
                iconCanvas.itemconfig(smallpatternpx[pattern_icon_selected][i], fill=topaint)
                i += 1
            draw_pattern_selector(pattern_icon_selected)

def update_pattern_icons():
    # use this to only refresh the icon view when turning pages
    # loop 1: patterndata = 0-31
    # render smallpatternpx 0-7 with data 0-7+xoffset
    i = 0
    while i < 8:
        p = 0
        while p < (spriteSize*spriteSize):
            px = patterndata[i+pattern_x_ofs+(pattern_y_ofs*32)][p]
            intval = palette_display[px].myVal
            topaint = single_intcol_to_hex(intval)
            iconCanvas.itemconfig(smallpatternpx[i][p], fill=topaint)
            #row 2?
            px = patterndata[i+pattern_x_ofs+(pattern_y_ofs*32)+32][p]
            intval = palette_display[px].myVal
            topaint = single_intcol_to_hex(intval)
            iconCanvas.itemconfig(smallpatternpx[i+8][p], fill=topaint)
            #row 3
            px = patterndata[i+pattern_x_ofs+(pattern_y_ofs*32)+64][p]
            intval = palette_display[px].myVal
            topaint = single_intcol_to_hex(intval)
            iconCanvas.itemconfig(smallpatternpx[i+16][p], fill=topaint)
            #row 4
            px = patterndata[i+pattern_x_ofs+(pattern_y_ofs*32)+(32*3)][p]
            intval = palette_display[px].myVal
            topaint = single_intcol_to_hex(intval)
            iconCanvas.itemconfig(smallpatternpx[i+24][p], fill=topaint)
            p += 1
        i+=1
    draw_pattern_selector(pattern_icon_selected)

# 2. add pagination to sprite view panel
def page_back():
    global page_ofs
    global pixels_mask1
    global pixels_mask2 
    maskdata[(icon_selected*2)+page_ofs] = pixels_mask1.copy()
    maskdata[(icon_selected*2)+page_ofs+1] = pixels_mask2.copy()
    # change page_ofs by 8
    # 0-7 (0), 8-15 (8), 16-23 (16), 24-31 (24)
    if page_ofs == 0:
        page_ofs = 24
    else:
        page_ofs = page_ofs - 8 
    # change pixels mask
    pixels_mask1 = maskdata[(icon_selected*2)+page_ofs].copy()
    pixels_mask2 = maskdata[(icon_selected*2)+page_ofs+1].copy()
    update_label_txt()
    refresh_display(True)
    #return 
def page_forward():
    global page_ofs
    global pixels_mask1
    global pixels_mask2 
    maskdata[(icon_selected*2)+page_ofs] = pixels_mask1.copy()
    maskdata[(icon_selected*2)+page_ofs+1] = pixels_mask2.copy()
    if page_ofs == 24:
        page_ofs = 0
    else: 
        page_ofs = page_ofs + 8
    # change pixels mask
    pixels_mask1 = maskdata[(icon_selected*2)+page_ofs].copy()
    pixels_mask2 = maskdata[(icon_selected*2)+page_ofs+1].copy()
    update_label_txt()
    refresh_display(True)
    #return 

from tkinter import filedialog

def save_pattern_as():
    global patternMode
    patternMode = True 
    save_as()
def save_sprite_as():
    global patternMode
    patternMode = False 
    save_as()

def save_as():
    global filename 
    global patternMode
    if patternMode == True:
        filename = tk.filedialog.asksaveasfilename(title='Save MSX2 Spriter file', filetypes=( ('MSX2 Spriter pattern file', '*.m2p'),('All files', '*.*') ))
    else:
        filename = tk.filedialog.asksaveasfilename(title='Save MSX2 Spriter file', filetypes=( ('MSX2 Spriter sprite file', '*.m2s'),('All files', '*.*') ))
    if filename == '' or type(filename)==tuple:
        return 
    if patternMode == True:
        savem2p()
    else:
        savem2s()
    #return
def load_as(reset=False):
    global filename 
    global patternMode 
    if reset == True:
        initialize_new(patternMode, True)
    if patternMode == False:
        loadm2s()
    else:
        loadm2p()
def load_pattern_as():
    global filename 
    global patternMode
    filename = tk.filedialog.askopenfilename(title='Load MSX2 Spriter file', filetypes=( ('MSX2 Spriter pattern file', '*.m2p'),('All files', '*.*') ))
    if filename == '':
        return 
    if type(filename) == tuple:
        return 
    reset = False 
    if patternMode != True:
        patternMode = True
        reset = True
    load_as(reset)
    #return 
def load_sprite_as():
    global filename 
    global patternMode
    filename = tk.filedialog.askopenfilename(title='Load MSX2 Spriter file', filetypes=( ('MSX2 Spriter sprite file', '*.m2s'),('All files', '*.*') ))
    if filename == '':
        return 
    if type(filename) == tuple:
        return
    reset = False
    if patternMode != False:
        patternMode = False
        reset = True 
    load_as(reset)

## Z80 ASSEMBLY EXPORT - THE GOOD SHIT ##   
def export_asm_pattern():
    global asmfile 
    asmfile = ''
    asmfile = tk.filedialog.asksaveasfilename(title='Save MSX2 pattern assembly data', filetypes=( ('Z80 assembly data', '*.z80'),('All files', '*.*') ))
    if asmfile == '' or type(asmfile) == tuple:
        return 
    if asmfile[-4:].upper() != '.Z80':
            asmfile = asmfile + '.z80'
    outdata = []
    outdata_c = []
    colors_array = []
    outdata.append("; Made with MSX2 Spriter")
    outdata.append(";")
    outdata.append("; Pattern generator data")
    outdata.append("; VDP location default @ $0000")
    out_check = []
    p = 0
    while p < 3:
        i = 0
        out_check.append(0)
        while i < (256):
            j = 0
            while j < (spriteSize*spriteSize):
                if patterndata[(p*256)+i][j] != 0:
                    out_check[p] = 1
                j += 1
            i += 1
        p += 1
    #
    pl = 0
    while pl < 3:
        if out_check[pl] == 1:
            outdata.append(";;;;;;;;;;;;;;;;;;")
            outdata.append("; Pattern table {}".format(pl+1))
            # determine palette values for color 0 and color 1
            tl = 0
            while tl < 256:
                rl = 0
                #outdata.append (" DB  ")
                rowout = []
                rowout.append(" DB  ")
                thisbyteout = ''
                while rl < 8:
                    #c1 = None 
                    c2 = None 
                    c1 = patterndata[(pl*256)+tl][0+(rl*8)]
                    cl = 1 
                    while cl < 8:
                        if patterndata[(pl*256)+tl][cl+(rl*8)] != c1:
                            c2 = patterndata[(pl*256)+tl][cl+(rl*8)]
                        if c2 != None:
                            cl = 8
                        cl += 1 #col loop
                    if c2 == None:
                        c2 = 0
                    ## now convert to binary
                    c1b = format(c1, '04b')
                    c2b = format(c2, '04b')
                    colors_array.append('{}{}'.format(c2b, c1b))
                    #now colors_array has color byte
                    reformatrow = []
                    clp = 0 
                    while clp < 8:
                        if patterndata[(pl*256)+tl][clp+(rl*8)] == c1:
                            #is this pixel color 0?
                            reformatrow.append('0')
                        elif patterndata[(pl*256)+tl][clp+(rl*8)] == c2:
                            reformatrow.append('1')
                        clp += 1
                    thisbyteout = ''.join(reformatrow)
                    thisbyteout = '$' + format(int(thisbyteout,2), '02x') + ', '
                    rowout.append(thisbyteout)
                    rl += 1 #row loop
                rowout = ''.join(rowout)[:-2] + ' ; {}'.format(tl)
                outdata.append(rowout)
                tl += 1 #tile loop
        pl += 1 #pattern loop
    outdata_c.append("; Made with MSX2 Spriter")
    outdata_c.append(";")
    outdata_c.append("; Pattern colors table")
    outdata_c.append("; VDP Location default @ $2000")
    pl = 0
    while pl < 3:
        if out_check[pl] == 1:
            outdata_c.append(";;;;;;;;;;;;;;;;;")
            outdata_c.append("; Table {} colors".format(pl+1))
            tl = 0
            while tl < 256:
                rl = 0
                rowout = []
                rowout.append(" DB  ")
                thisbyteout = ''
                while rl < 8:
                    thisbyteout = colors_array[0]
                    thisbyteout = '$' + format(int(thisbyteout,2), '02x') + ', '
                    colors_array.pop(0)
                    rowout.append(thisbyteout)
                    rl += 1 # row loop
                rowout = ''.join(rowout)[:-2] + ' ; {}'.format(tl)
                outdata_c.append(rowout)
                tl += 1 #tile loop
        pl += 1 #pattern loop
    f_c = None
    try:
        cfile = ''
        if asmfile[-4:].upper() != '.Z80':
            asmfile = asmfile + '.z80'
            cfile = asmfile + '_colors.z80'
        else: 
            cfile = asmfile[:-4] + '_colors.z80'
        f = open(asmfile, 'w')
        for s in outdata:
            f.write(s)
            f.write('\n')
        f_c = open(cfile, 'w')
        for s in outdata_c:
            f_c.write(s)
            f_c.write('\n')
        messagebox.showinfo("Save OK", message="Save successful.")
    except IOError:
        messagebox.showerror("Export failed", message="I/O error exporting file. Check drive and permissions and try again.")
    except:
        messagebox.showerror("Export failed", message="Unknown error exporting file. This might be a bug!")
    finally:
        if f != None:
            f.close()
        if f_c != None:
            f_c.close()

    return  

def export_asm_data():
    global patternMode
    if patternMode == True:
        messagebox.showwarning("Error","Saving not supported for tile mode.")
        return 
    
    global asmfile 
    asmfile = ''
    asmfile = tk.filedialog.asksaveasfilename(title='Save MSX2 sprite assembly data', filetypes=( ('Z80 assembly data', '*.z80'),('All files', '*.*') ))
    if asmfile == '' or type(asmfile) == tuple:
        return 
    if asmfile[-4:].upper() != '.Z80':
            asmfile = asmfile + '.z80'
    outdata = []
    outdata.append("; Made with MSX2 Spriter")
    # first, check to see what patterns need exporting.
    # iterate through maskdata[], and set val to 1.
    out_check = []
    i = 0
    while i < 32:
        j = 0
        out_check.append(0)
        while j < (spriteSize*spriteSize):
            if maskdata[i][j] != 0:
                out_check[i] = 1
            j += 1
        i += 1
    # Gotta do palette shit first 
    i = 0
    while i < 32:
        if out_check[i] == 1:
            outdata.append('; Color mask {}'.format(i))
            # top
            y = 0
            curline = []
            curline.append(' DB ')
            while y < 8:
                outb = ''
                x = 0
                while x < 16:
                    # convert maskdata[i][(y*16)+x] to hex
                    md = maskdata[i][(y*16)+x]
                    if md > 0:
                        if i % 2 == 0:
                            outb = '{:02x}'.format(md)
                        else:
                            md += 64
                            outb = '{:02x}'.format(md)
                    x += 1
                y += 1
                if outb == '':
                    curline.append(' $00,')
                else:
                    curline.append(' ${},'.format(outb))
            curline = ''.join(curline)[:-1]
            outdata.append(curline)
            # bottom
            y = 8
            curline = []
            curline.append(' DB ')
            while y < 16:
                outb = ''
                x = 0
                while x < 16:
                    # convert maskdata[i][(y*16)+x] to hex
                    md = maskdata[i][(y*16)+x]
                    if md > 0:
                        if i % 2 == 0:
                            outb = '{:02x}'.format(md)
                        else:
                            md += 64
                            outb = '{:02x}'.format(md)
                    x += 1
                y += 1
                if outb == '':
                    curline.append(' $00,')
                else:
                    curline.append(' ${},'.format(outb))
            curline = ''.join(curline)[:-1]
            outdata.append(curline)

        i += 1
    # NOW do sprite stuff
    i = 0
    while i < 32:
        if out_check[i] == 1:
            # top left first
            outdata.append('; Mask {}'.format(i))
            y = 0
            curline = []
            curline.append (' DB ')
            while y < 8:
                outb = []
                x = 0
                while x < 8:
                    if maskdata[i][(y*16)+x] != 0:
                        outb.append('1')
                    else: 
                        outb.append('0')
                    x += 1
                y += 1
                curbin = int(''.join(outb),2)
                curbin = "{:02x}".format(curbin)
                curline.append(' ${},'.format(curbin))
            curline = ''.join(curline)[:-1]
            outdata.append(curline)
            # bottom left
            y = 8
            curline = []
            curline.append (' DB ')
            while y < 16:
                outb = []
                x = 0
                while x < 8:
                    if maskdata[i][(y*16)+x] != 0:
                        outb.append('1')
                    else: 
                        outb.append('0')
                    x += 1
                y += 1
                curbin = int(''.join(outb),2)
                curbin = "{:02x}".format(curbin)
                curline.append(' ${},'.format(curbin))
            curline = ''.join(curline)[:-1]
            outdata.append(curline)
            # top right
            y = 0
            curline = []
            curline.append (' DB ')
            while y < 8:
                outb = []
                x = 8
                while x < 16:
                    if maskdata[i][(y*16)+x] != 0:
                        outb.append('1')
                    else: 
                        outb.append('0')
                    x += 1
                y += 1
                curbin = int(''.join(outb),2)
                curbin = "{:02x}".format(curbin)
                curline.append(' ${},'.format(curbin))
            curline = ''.join(curline)[:-1]
            outdata.append(curline)
            # bottom right
            y = 8
            curline = []
            curline.append (' DB ')
            while y < 16:
                outb = []
                x = 8
                while x < 16:
                    if maskdata[i][(y*16)+x] != 0:
                        outb.append('1')
                    else: 
                        outb.append('0')
                    x += 1
                y += 1
                curbin = int(''.join(outb),2)
                curbin = "{:02x}".format(curbin)
                curline.append(' ${},'.format(curbin))
            curline = ''.join(curline)[:-1]
            outdata.append(curline)
        i += 1

    try:
        f = open(asmfile, 'w')
        for s in outdata:
            f.write(s)
            f.write('\n')
        messagebox.showinfo("Save OK", message="Save successful.")
    except IOError:
        messagebox.showerror("Export failed", message="I/O error exporting file. Check drive and permissions and try again.")
    except:
        messagebox.showerror("Export failed", message="Unknown error exporting file. This might be a bug!")
    finally:
        if f != None:
            f.close()
        

def export_pal_data():
    asmpalfile = ''
    asmpalfile = tk.filedialog.asksaveasfilename(title='Save MSX2 palette assembly data', filetypes=( ('Z80 assembly data', '*.z80'),('All files', '*.*') ))
    if asmpalfile == '' or type(asmpalfile)==tuple:
        return 
    if asmpalfile[-4:].upper() != '.Z80':
            asmpalfile = asmpalfile + '.z80'
    outdata = []
    outdata.append('; Palette data made with MSX2 Spriter\n')
    outdata.append(';  Write in sequence to R#16!')
    # 16 colors
    i = 0
    while i < 16:
        # byte 1 = '0RRR0BBB'
        # byte 2 = '00000GGG'
        # RED:
        if i != 0:
            ob1 = "{0:b}".format(int(intpal[i][:-2])) 
        else:
            ob1 = '000'
        if len(ob1) == 1:
            ob1 = '00' + ob1
        elif len(ob1) == 2:
            ob1 = '0' + ob1 
        # BLUE:
        if i != 0:
            ob2 = int(intpal[i][2:])
            ob2 = "{0:b}".format(ob2)
        else:
            ob2 = '000'
        if len(ob2) == 1:
            ob2 = '00' + ob2
        elif len(ob2) == 2:
            ob2 = '0' + ob2
        # GREEN:
        if i != 0:
            ob3 = "{0:b}".format(int(intpal[i][1:-1]))
        else:
            ob3 = '000'
        if len(ob3) == 1:
            ob3 = '00' + ob3
        elif len(ob3) == 2:
            ob3 = '0' + ob3 
        b1 = '0' + ob1 + '0' + ob2 
        b2 = '00000' + ob3
        ob1 = "{:02x}".format(int(b1,2))
        ob2 = "{:02x}".format(int(b2,2))
        if i % 4 == 0:
            outdata.append("\n DB ")
        outdata.append(" ${}, ${},".format(ob1,ob2))
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
        messagebox.showinfo("Save OK", message="Save successful.")
    except IOError:
        messagebox.showerror("Export failed", message="I/O error exporting file. Check drive and permissions and try again.")
    except:
        messagebox.showerror("Export failed", message="Unknown error exporting file. This might be a bug!")
    finally:
        f.close()

import tkinter.messagebox as messagebox

def loadm2p():
    global filename 
    global spriteSize
    spriteSize = 8
    f = None 
    try: 
        f = open(filename, 'r')
        data = f.readline()
        global palette_display
        global currentColor 
        palette_vals = data.split(',')
        i = 0
        while i < 16:
            if palette_vals[i] == 'trans':
                palette_vals[i] = '000'
            palette_display[i].myVal = palette_vals[i]
            currentColor = i 
            i += 1
        resetPalette(palette_vals)
        currentColor = intpal[0]
        j = 0
        while j < (3*256):
            data = f.readline().split(',')
            data.pop()
            data_int=[]
            i = 0
            while i < (spriteSize*spriteSize):
                data_int.append(int(data[i]))
                patterndata[j][i] = data_int[i]
                i += 1
            global pixels_mask1
            global icon_selected
            pixels_mask1 = patterndata[0].copy()
            icon_selected = 0
            global pattern_x_ofs
            global pattern_y_ofs
            pattern_x_ofs = 0
            pattern_y_ofs = 0
            j += 1
        refresh_display(True)
    except IOError:
        messagebox.showerror("I/O error", message="Failed to load file. Check drives and permissions and try again.")
    except:
        messagebox.showerror("Unexpected error", message="Unknown error loading file. Ensure the file is a proper M2P file.")
    finally:
        if(f):
            f.close()


def loadm2s():
    global filename
    global spriteSize
    spriteSize = 16
    f = None 
    try:
        f = open(filename, 'r')
        data = f.readline()
        # reset palette data
        global palette_display
        global currentColor
        palette_vals = data.split(',')
        i = 0
        while i < 16:
            if palette_vals[i] == 'trans':
                palette_vals[i] == '000'
            palette_display[i].myVal = palette_vals[i]
            currentColor = i 
            i += 1
        resetPalette(palette_vals)
        currentColor = intpal[0]#'trans'
        # load in mf'in maskdata
        j = 0
        while j < 32:
            data = f.readline().split(',')
            data.pop()
            data_int = []
            i = 0 
            while i < (spriteSize*spriteSize):
                data_int.append(int(data[i]))
                maskdata[j][i] = data_int[i]
                i += 1
            if j == (page_ofs + icon_selected + 1):
                global pixels_mask1
                global pixels_mask2
                pixels_mask1 = maskdata[j-1].copy()
                pixels_mask2 = maskdata[j].copy()
            j += 1
        refresh_display(True)
    except IOError:
        messagebox.showerror("I/O error", message="Failed to load file. Check drives and permissions and try again.")
    except:
        messagebox.showerror("Unexpected error", message="Unknown error loading file. Ensure the file is a proper M2S file.")
    finally:
        if(f):
            f.close()

def resetPalette(newpal):
    global intpal 
    intpal = newpal 
    convert_int_pal_to_hex(intpal)
    updatePaletteDisplay()
    #return 

def savem2p():
    # save as MSX2 Spriter pattern file
    global filename 
    if filename == '' or type(filename)==tuple:
        return
    p = []
    f = None 
    for n in palette_display:
        p.append(n.myVal)
    try:
        if filename[-4:].upper() != '.M2P':
            filename = filename + '.m2p'
        f = open(filename, 'w')
        for item in p: 
            f.write('%s,' % item)
        for n in patterndata:
            f.write('\n')
            for item in n:
                f.write('%s,' % item)
        messagebox.showinfo("Save OK", message="Save successful.")
        global saved 
        saved = True 
    except IOError:
        #global filename 
        filename = ''
        messagebox.showerror("I/O error", message="Output error saving file. Check drives and permissions and try again.")
    except:
        #global filename 
        filename = ''
        messagebox.showerror("Unexpected error", message="Unknown error saving file. This might be a bug!!")
    finally:
        if(f):
            f.close()
    return

def savem2s():
    global filename
    p = []
    f = None 
    for n in palette_display:
        p.append(n.myVal)
    try:
        if filename[-4:].upper() != '.M2S':
            filename = filename + '.m2s'
        f = open(filename, 'w')
        for item in p: 
            f.write('%s,' % item)
        for n in maskdata:
            f.write('\n')
            for item in n:
                f.write('%s,'%item)
        messagebox.showinfo("Save OK", message="Save successful.")
        global saved 
        saved = True 
    except IOError:
        #global filename 
        filename = ''
        messagebox.showerror("I/O error", message="Output error saving file. Check drives and permissions and try again.")
    except:
        messagebox.showerror("Unexpected error", message="Unknown error saving file. This might be a bug!!")
    finally:
        if(f):
            f.close()

saved = False
# define menus
def client_exit():
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

def new_file():
    # ask if ok, if not, open save_normal dialog
    global patternMode
    global filename  
    global editMenu
    result = messagebox.askquestion("New file", "Save changes before creating new file?", icon='warning')
    if result == 'yes':
        global saved 
        saved = False 
        if patternMode == True:
            save_normal_pattern()
        else:
            save_normal_sprite()
        if saved==False:
            filename = '' 
            return 
    patternMode = False 
    tk.ACTIVE
    filename = ''
    initialize_new(patternMode)

def new_pattern_file():
    global patternMode
    global filename  
    global editMenu
    result = messagebox.askquestion("New file", "Save changes before creating new file?", icon='warning')
    if result == 'yes':
        global saved 
        saved = False
        if patternMode == True:
            save_normal_pattern()
        else:
            save_normal_sprite()
        if saved == False:
            filename = '' 
            return 
    patternMode = True
    filename = '' 
    initialize_new(patternMode)

def save_normal_sprite():
    global patternMode 
    patternMode = False 
    save_normal()
def save_normal_pattern():
    global patternMode 
    patternMode = True
    save_normal()

def save_normal():
    global filename
    if filename == '':
        save_as()
    else:
        global patternMode 
        if patternMode == False:
            savem2s()
        else:
            savem2p()
    #return

def cut_data():
    global maskdata
    global mask
    global copybuffer
    global icon_selected
    global page_ofs
    global pixels_mask1
    global pixels_mask2

    copybuffer = []
    
    add_undo_point()

    if patternMode == False:
        mask_ofs = mask.get() - 1

        if icon_selected == 0:
            maskdata_ofs = 0+page_ofs+mask_ofs
        elif icon_selected == 1:
            maskdata_ofs = 2+page_ofs+mask_ofs
        elif icon_selected == 2:
            maskdata_ofs = 4+page_ofs+mask_ofs
        elif icon_selected == 3:
            maskdata_ofs = 6+page_ofs+mask_ofs
        add_undo_point()
        copybuffer = maskdata[maskdata_ofs].copy()
        maskdata[maskdata_ofs] = []

        i = 0 
        while i < (spriteSize*spriteSize): #64
            maskdata[maskdata_ofs].append(0)
            i += 1

        if mask_ofs == 0:
            pixels_mask1 = maskdata[maskdata_ofs].copy()
        else:
            pixels_mask2 = maskdata[maskdata_ofs].copy()
    else:
        copybuffer = patterndata[icon_selected].copy()
        patterndata[icon_selected] = []

        i = 0
        while i < (spriteSize*spriteSize): #64
            patterndata[icon_selected].append(0)
            i += 1

        pixels_mask1 = patterndata[icon_selected].copy()

    refresh_display(True)

def copy_data():
    global maskdata
    global mask
    global copybuffer
    global icon_selected
    global page_ofs

    copybuffer = []
    
    if patternMode == False:
        mask_ofs = mask.get() - 1

        if icon_selected == 0:
            copybuffer = maskdata[0+page_ofs+mask_ofs].copy()
        elif icon_selected == 1:
            copybuffer = maskdata[2+page_ofs+mask_ofs].copy()
        elif icon_selected == 2:
            copybuffer = maskdata[4+page_ofs+mask_ofs].copy()
        elif icon_selected == 3:
            copybuffer = maskdata[6+page_ofs+mask_ofs].copy()
    else:
        copybuffer = patterndata[icon_selected].copy()

redo_history = []

def flip_horizontal():
    global maskdata
    global mask
    global icon_selected
    global page_ofs
    global pixels_mask1
    global pixels_mask2

    add_undo_point()

    if patternMode == False:
        mask_ofs = mask.get() - 1
        maskdata_ofs = page_ofs + mask_ofs

        if icon_selected == 1:
            maskdata_ofs += 2
        elif icon_selected == 2:
            maskdata_ofs += 4
        elif icon_selected == 3:
            maskdata_ofs += 6

        rowstart = 0
        rowend = spriteSize

        copiedmaskdata = maskdata[maskdata_ofs].copy()

        while rowstart < rowend:
            start = 0 + (rowstart * spriteSize)
            end = spriteSize + (rowstart * spriteSize) - 1

            while start < end:
                copiedmaskdata[start], copiedmaskdata[end] = copiedmaskdata[end], copiedmaskdata[start]
                start += 1
                end -= 1

            rowstart += 1

        maskdata[maskdata_ofs] = copiedmaskdata.copy()

        if mask_ofs == 0:
            pixels_mask1 = maskdata[maskdata_ofs].copy()
        else:
            pixels_mask2 = maskdata[maskdata_ofs].copy()
    else:
        rowstart = 0
        rowend = spriteSize

        copiedpatterndata = patterndata[icon_selected].copy()

        while rowstart < rowend:
            start = 0 + (rowstart * spriteSize)
            end = spriteSize + (rowstart * spriteSize ) - 1

            while start < end:
                copiedpatterndata[start], copiedpatterndata[end] = copiedpatterndata[end], copiedpatterndata[start]
                start += 1
                end -= 1

            rowstart += 1

        patterndata[icon_selected] = copiedpatterndata.copy()

        pixels_mask1 = patterndata[icon_selected].copy()

    refresh_display(True)

def flip_vertical():
    global maskdata
    global mask
    global icon_selected
    global page_ofs
    global pixels_mask1
    global pixels_mask2

    add_undo_point()

    if patternMode == False:
        mask_ofs = mask.get() - 1
        maskdata_ofs = page_ofs + mask_ofs

        if icon_selected == 1:
            maskdata_ofs += 2
        elif icon_selected == 2:
            maskdata_ofs += 4
        elif icon_selected == 3:
            maskdata_ofs += 6

        colstart = 0
        colend = spriteSize

        copiedmaskdata = maskdata[maskdata_ofs].copy()

        while colstart < colend:
            rowstart = 0
            rowend = spriteSize - 1

            while rowstart < rowend:
                cellstart = colstart + (rowstart * spriteSize)
                cellend = colstart + (rowend * spriteSize)

                copiedmaskdata[cellstart], copiedmaskdata[cellend] = copiedmaskdata[cellend], copiedmaskdata[cellstart]

                rowstart += 1
                rowend -= 1

            colstart += 1

        maskdata[maskdata_ofs] = copiedmaskdata.copy()

        if mask_ofs == 0:
            pixels_mask1 = maskdata[maskdata_ofs].copy()
        else:
            pixels_mask2 = maskdata[maskdata_ofs].copy()
    else:
        colstart = 0
        colend = spriteSize

        copiedpatterndata = patterndata[icon_selected].copy()

        while colstart < colend:
            rowstart = 0
            rowend = spriteSize - 1

            while rowstart < rowend:
                cellstart = colstart + (rowstart * spriteSize)
                cellend = colstart + (rowend * spriteSize)

                copiedpatterndata[cellstart], copiedpatterndata[cellend] = copiedpatterndata[cellend], copiedpatterndata[cellstart]

                rowstart += 1
                rowend -= 1

            colstart += 1

        patterndata[icon_selected] = copiedpatterndata.copy()
        pixels_mask1 = patterndata[icon_selected].copy()

    refresh_display(True)

def redo_last():
    global redo_history
    global maskdata 
    global patternMode 
    global patterndata 
    #
    if len(redo_history) > 0:
        add_undo_point()
        if patternMode == False:
            maskdata = redo_history.pop()
        else:
            patterndata = redo_history.pop()
        CopyMaskToDisplay()
        refresh_display(True)

undo_history = []
modified_icon_history = []


def SelectTarget(ic):
    global page_ofs
    global pixels_mask1
    global pixels_mask2 
    global icon_selected
    global patternMode
    if patternMode == False:
        if ic < 8:
            page_ofs = 0
        elif ic < 16:
            page_ofs = 8
        elif ic < 24:
            page_ofs = 16
        else:
            page_ofs = 24
        if ic % 2 == 0:
            pixels_mask1 = maskdata[ic].copy()
            pixels_mask2 = maskdata[ic+1].copy()
        else:
            pixels_mask1 = maskdata[ic-1].copy()
            pixels_mask2 = maskdata[ic].copy()
        icon_selected = int((ic%8)/2)
        update_label_txt()
        draw_sprite_selector(icon_selected)
    else:
        #TODO:
        global pattern_icon_selected
        global pattern_y_ofs 
        global pattern_x_ofs 
        topleft = (pattern_y_ofs*32) + pattern_x_ofs #<- has tile num 
        #print(topleft)
        if (ic >= topleft) and (ic <= (topleft+7)) or\
            (ic >= (topleft+32)) and (ic <= (topleft+39)) or\
            (ic >= (topleft+64)) and (ic <= (topleft+71)) or\
            (ic >= (topleft+96)) and (ic <= (topleft+103)):
                # we are visible!
                pixels_mask1 = patterndata[ic].copy() 
        else:
            #remember, ic is our TARGET icon.
            tr = math.floor(ic/32)
            if pattern_y_ofs < tr-3:
                pattern_y_ofs = tr-3
            if pattern_y_ofs > tr:
                pattern_y_ofs = tr
            tc = ic % 32
            if pattern_x_ofs < tc-7:
                pattern_x_ofs = tc-7
            if pattern_x_ofs > tc:
                pattern_x_ofs = tc 
            
            if pattern_y_ofs < 0:
                pattern_y_ofs = 0
            if pattern_x_ofs < 0:
               pattern_x_ofs = 0
        icon_selected = ic 
        pattern_icon_selected = get_pattern_sel_from_is()
        draw_pattern_selector(pattern_icon_selected)
            #otherwise, we need to adjust our x/y offsets.
    refresh_display(True)

def get_pattern_sel_from_is():
    global icon_selected
    global pattern_y_ofs
    global pattern_x_ofs 
    tp = icon_selected - (pattern_y_ofs*32)-pattern_x_ofs
    while tp > 31:
        tp -= 32-8
    return tp

def undo_last():
    global redo_history
    global undo_history
    global patternMode 
    global maskdata 
    global modified_icon_history
    global patterndata
    global last_pixel_colored
    if len(undo_history) < 1:
        return
    last_pixel_colored = -1
    if patternMode == False:
        redo_history.append(maskdata.copy())
        if len(redo_history) > 100:
            redo_history.pop(0)
        maskdata = undo_history.pop()
        CopyMaskToDisplay() 
#        SelectTarget(modified_icon_history.pop())
    else:
        redo_history.append(patterndata.copy())
        if len(redo_history) > 100:
            redo_history.pop(0)
        patterndata = undo_history.pop()
        CopyMaskToDisplay()
#        SelectTarget(modified_icon_history.pop())
    refresh_display(True)

def CopyMaskToDisplay():
    global icon_selected
    global page_ofs 
    global pixels_mask1
    global pixels_mask2
    global patternMode 
    global maskdata 
    global patterndata 
    if patternMode == False:
        ic = (icon_selected*2) + page_ofs + mask.get()-1
        if mask.get() == 1:
            pixels_mask1 = maskdata[ic].copy()
            pixels_mask2 = maskdata[ic+1].copy()
        elif mask.get() == 2:
            pixels_mask1 = maskdata[ic-1].copy()
            pixels_mask2 = maskdata[ic].copy()
    else:
        pixels_mask1 = patterndata[icon_selected].copy()

def paste_data():
    global maskdata
    global mask
    global copybuffer
    global icon_selected
    global page_ofs
    global pixels_mask1
    global pixels_mask2

    if not copybuffer:
        return
    
    add_undo_point()

    if patternMode == False:
        mask_ofs = mask.get() - 1

        if icon_selected == 0:
            maskdata[0+page_ofs+mask_ofs] = copybuffer.copy()
        elif icon_selected == 1:
            maskdata[2+page_ofs+mask_ofs] = copybuffer.copy()
        elif icon_selected == 2:
            maskdata[4+page_ofs+mask_ofs] = copybuffer.copy()
        elif icon_selected == 3:
            maskdata[6+page_ofs+mask_ofs] = copybuffer.copy()
        
        if mask_ofs == 0:
            pixels_mask1 = copybuffer.copy()
        else:
            pixels_mask2 = copybuffer.copy()
    else:
        patterndata[icon_selected] = copybuffer.copy()
        pixels_mask1 = copybuffer.copy()
    refresh_display(True)

def import_palette():
    global filename
    #global spriteSize
    #spriteSize = 16
    filename = tk.filedialog.askopenfilename(title='Load MSX2 sprite/pattern file', filetypes=( ('MSX2 Spriter file', '*.m2s;*.m2p'),('All files', '*.*') ))
    if filename == '':
        return 
    if type(filename) == tuple:
        return
    f = None 
    try:
        f = open(filename, 'r')
        data = f.readline()
        # reset palette data
        global palette_display
        global currentColor
        palette_vals = data.split(',')
        i = 0
        while i < 16:
            if palette_vals[i] == 'trans':
                palette_vals[i] == '000'
            palette_display[i].myVal = palette_vals[i]
            currentColor = i 
            i += 1
        resetPalette(palette_vals)
        currentColor = intpal[0]
        #unclick_all()
        refresh_display(True)
        messagebox.showinfo(title='Import successful', message='Palette imported successfully!')
    except IOError:
        messagebox.showerror("I/O error", message="Failed to load file. Check drives and permissions and try again.")
    except:
        messagebox.showerror("Unexpected error", message="Unknown error loading file. Ensure the file is a proper M2S file.")
    finally:
        if(f):
            f.close()

def open_about():
    messagebox.showinfo(title='About', message='MSX2 Spriter tool v1.28\n(c)2019 Ben Ferguson\nAll rights reserved n such.(Created in Python!)\n\nInfo link: https://github.com/bferguson3/msx2spriter')


menuBar = tk.Menu(app)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label="New sprite file", command=new_file)
fileMenu.add_command(label="New pattern file", command=new_pattern_file)
fileMenu.add_command(label="Save (Ctrl+S)", command=save_normal_sprite) #2
fileMenu.add_command(label="Save As .M2S...", command=save_sprite_as) #3
fileMenu.add_command(label="Load .M2S Sprite...", command=load_sprite_as)
fileMenu.add_command(label="Load .M2P Pattern...", command=load_pattern_as)
fileMenu.add_separator()
fileMenu.add_command(label="Export z80 sprite data...", command=export_asm_data) #7
fileMenu.add_command(label="Export z80 palette data...", command=export_pal_data)
fileMenu.add_separator()
fileMenu.add_command(label='Import palette from...', command=import_palette)
fileMenu.add_separator()
fileMenu.add_command(label="Quit", command=client_exit)
menuBar.add_cascade(label="File", menu=fileMenu)
editMenu = tk.Menu(menuBar, tearoff=0)
helpMenu = tk.Menu(menuBar, tearoff=0)
editMenu.add_command(label='Cut (Ctrl+X)', command=cut_data)
editMenu.add_command(label='Copy (Ctrl+C)', command=copy_data)
editMenu.add_command(label='Paste (Ctrl+V)', command=paste_data)
editMenu.add_separator()
editMenu.add_command(label="Undo (Ctrl+Z)", command=undo_last)
editMenu.add_command(label="Redo (Ctrl+Y)", command=redo_last)
editMenu.add_separator()
editMenu.add_command(label='Flip Horizontal', command=flip_horizontal)
editMenu.add_command(label='Flip Vertical', command=flip_vertical)
editMenu.add_separator()
editMenu.add_command(label='Config RMB...', state=tk.DISABLED)
helpMenu.add_command(label='About...', command=open_about)
menuBar.add_cascade(label='Edit', menu=editMenu)
menuBar.add_cascade(label='Help', menu=helpMenu)
toolbar = tk.Frame(win, width=600, height=30, relief=tk.RAISED)
savebutton = tk.Button(toolbar, image=save_icon, width=20, height=20, command=save_normal)
drawpxbutton = tk.Button(toolbar, image=drawpx_icon, width=20, height=20, relief=tk.SUNKEN)
cutbutton = tk.Button(toolbar, image=cut_icon, width=20, height=20, command=cut_data)
copybutton = tk.Button(toolbar, image=copy_icon, width=20, height=20, command=copy_data)
pastebutton = tk.Button(toolbar, image=paste_icon, width=20, height=20, command=paste_data)
undobutton = tk.Button(toolbar, image=undo_icon, width=20, height=20, command=undo_last)
redobutton = tk.Button(toolbar, image=redo_icon, width=20, height=20, command=redo_last)
horizbutton = tk.Button(toolbar, image=horiz_icon, width=20, height=20, command=flip_horizontal)
vertbutton = tk.Button(toolbar, image=vert_icon, width=20, height=20, command=flip_vertical)
savebutton.grid(row=0, column=0)
drawpxbutton.grid(row=0, column=1, padx=(20,0))
cutbutton.grid(row=0, column=2,padx=(20,0))
copybutton.grid(row=0, column=3)
pastebutton.grid(row=0, column=4)
undobutton.grid(row=0, column=5, padx=(20,0))
redobutton.grid(row=0, column=6)
horizbutton.grid(row=0, column=7, padx=(20,0))
vertbutton.grid(row=0, column=8)
toolbar.grid(row=0)

app.config(menu=menuBar) 


def pattern_move_back():
    global pattern_x_ofs
    global pattern_icon_selected
    if pattern_x_ofs > 0:
        pattern_icon_selected += 1
        pattern_x_ofs -= 1
    refresh_display(True)
def pattern_move_fwd():
    global pattern_x_ofs
    global pattern_icon_selected
    if pattern_x_ofs < (32-8):
        pattern_x_ofs += 1
        pattern_icon_selected -= 1
    refresh_display(True)
def pattern_move_up():
    global pattern_y_ofs
    global pattern_icon_selected
    if pattern_y_ofs > 0:
        pattern_y_ofs -= 1
        pattern_icon_selected += 8
    refresh_display(True)
    l1.configure(text="Table {} / 3".format(math.floor(pattern_y_ofs/8)+1))
def pattern_move_down():
    global pattern_y_ofs
    global pattern_icon_selected
    if pattern_y_ofs < (8*3)-4:
        pattern_y_ofs += 1
        pattern_icon_selected -= 8
    refresh_display(True)
    l1.configure(text="Table {} / 3".format(math.floor(pattern_y_ofs/8)+1)) 
    
def pattern_page_up():
    global pattern_y_ofs 
    global pattern_icon_selected
    if pattern_y_ofs > 7:
        pattern_y_ofs -= 8
        pattern_icon_selected += (8*8)
    else:
        while pattern_y_ofs > 0:
            pattern_y_ofs -= 1
            pattern_icon_selected += 8
    refresh_display(True)
    l1.configure(text="Table {} / 3".format(math.floor(pattern_y_ofs/8)+1))
def pattern_page_down():
    global pattern_y_ofs 
    global pattern_icon_selected
    if pattern_y_ofs < (8*3)-4-8:
        pattern_y_ofs += 8
        pattern_icon_selected -= (8*8)
    else:
        while pattern_y_ofs < (8*3)-4:
            pattern_y_ofs += 1
            pattern_icon_selected -= 8
    refresh_display(True)
    l1.configure(text="Table {} / 3".format(math.floor(pattern_y_ofs/8)+1)) 


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

# class undo_log(list):
#     # how to use:
#     # undo_log.append(data_to_revert, tilenum=num_of_tile_changed)
#     def __init__(self, *args, **kwargs):
#         list.__init__(self, *args, **kwargs)
#         self.undotile = list()
#     def append(self, tiledata, **kwargs):
#         super().append(tiledata)
#         for k,v in kwargs.items():
#             if k == 'tilenum':
#                 self.undotile.append(v)
#     def pop(self):
#         a = super().pop()
#         b = self.undotile.pop()
#         return a,b

# undosteps = undo_log()

def set_undo_release(o):
    global button_not_released
    button_not_released = False 

def add_undo_point(icon_s=-1):#, actualIcon=False):
    global undo_history
    global modified_icon_history
    global icon_selected 
    if icon_s == -1:
        icon_s = icon_selected
    if patternMode == False:
        global maskdata 
        #if len(undo_history) < 100:
        undo_history.append(maskdata.copy())
        if len(undo_history) > 100:
            undo_history.pop(0)
        modified_icon_history.append(page_ofs + (icon_s*2) + mask.get()-1) 
        if(len(modified_icon_history)) > 100:
            modified_icon_history.pop(0)
    else:
        global patterndata 
        undo_history.append(patterndata.copy())
        if len(undo_history) > 100:
            undo_history.pop(0)
        modified_icon_history.append(icon_selected)
        if len(modified_icon_history) > 100:
            modified_icon_history.pop(0)

def rotate_left(l, n):
    return l[n:] + l[:n]
def rotate_right(l, n):
    return l[-n:] + l[:-n]

def shift_right():
    global pixels_mask1
    global pixels_mask2
    global patternMode
    global page_ofs 
    global icon_selected
    if mask.get() == 1:# or patternMode == True:
        i = 0
        while i < (spriteSize*spriteSize):
            l = pixels_mask1[i:spriteSize+i]
            l = rotate_right(l, 1)
            pixels_mask1 = pixels_mask1[:i] + l + pixels_mask1[spriteSize+i:]
            i += spriteSize
        if patternMode == False:
            maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        else:
            patterndata[icon_selected] = pixels_mask1.copy()
    else:
        i = 0
        while i < (spriteSize*spriteSize):
            l = pixels_mask2[i:spriteSize+i]
            l = rotate_right(l, 1)
            pixels_mask2 = pixels_mask2[:i] + l + pixels_mask2[spriteSize+i:]
            i += spriteSize
        maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        maskdata[page_ofs + (icon_selected*2)+1] = pixels_mask2.copy()
    refresh_display(True)
     
def shift_left():
    global pixels_mask1
    global pixels_mask2
    global patternMode
    global page_ofs 
    global icon_selected
    if mask.get() == 1:# or patternMode == True:
        i = 0
        while i < (spriteSize*spriteSize):
            l = pixels_mask1[i:spriteSize+i]
            l = rotate_left(l, 1)
            pixels_mask1 = pixels_mask1[:i] + l + pixels_mask1[spriteSize+i:]
            i += spriteSize
        if patternMode == False:
            maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        else:
            patterndata[icon_selected] = pixels_mask1.copy()
    else:
        i = 0
        while i < (spriteSize*spriteSize):
            l = pixels_mask2[i:spriteSize+i]
            l = rotate_left(l, 1)
            pixels_mask2 = pixels_mask2[:i] + l + pixels_mask2[spriteSize+i:]
            i += spriteSize
        maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        maskdata[page_ofs + (icon_selected*2)+1] = pixels_mask2.copy()
    refresh_display(True)

def shift_down():
    global pixels_mask1
    global pixels_mask2
    global patternMode
    global page_ofs 
    global icon_selected
    if mask.get() == 1:# or patternMode == True:
        pixels_mask1 = rotate_right(pixels_mask1, spriteSize)
        if patternMode == False:
            maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        else:
            patterndata[icon_selected] = pixels_mask1.copy()
    else:
        pixels_mask2 = rotate_right(pixels_mask2, spriteSize)
        maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        maskdata[page_ofs + (icon_selected*2)+1] = pixels_mask2.copy()
    refresh_display(True) 
def shift_up():
    global pixels_mask1
    global pixels_mask2
    global patternMode
    global page_ofs 
    global icon_selected
    if mask.get() == 1:
        pixels_mask1 = rotate_left(pixels_mask1, spriteSize)
        if patternMode == False:
            maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        else:
            patterndata[icon_selected] = pixels_mask1.copy()
    else:
        pixels_mask2 = rotate_left(pixels_mask2, spriteSize)
        maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
        maskdata[page_ofs + (icon_selected*2)+1] = pixels_mask2.copy()
    refresh_display(True) 


def initialize_new(patternMode, loading=False):
    global intpal 
    intpal = defaultIntegerPalette.copy()
    convert_int_pal_to_hex(intpal)
    global palette_display
    global pixelSize 
    global spriteSize
    global icon_selected
    global pattern_x_ofs
    global pattern_y_ofs
    global pattern_page 
    global page_ofs 
    global iconwidth 
    global iconcanvascolumn 
    global win 
    global iconCanvas
    global drawCanvas
    global smallpixels1
    global smallpixels2
    global smallpixels3
    global smallpixels4
    global r0 
    global r1 
    global s0 
    global s1
    global l0 
    global l1
    global l2
    global l3
    global bu
    global bd 
    global bl 
    global br 
    global buu 
    global bdd
    global su
    global sd 
    global sr 
    global sl
    global smallpatternpx
    global last_pixel_colored
    global undo_history
    global redo_history
    undo_history = []
    redo_history = []
    last_pixel_colored = -1
    # Set up the default window frame
    if win == None:
        win = tk.Frame(master=app, width=800, height=600)
        win.grid(rowspan=16, columnspan=16)
    mask.set(1)
    if patternMode == True:
        show_m1.set(True)
        show_m2.set(False)
        pixelSize = 32
        spriteSize = 8
    else: 
        show_m1.set(True)
        show_m2.set(True)
        pixelSize = 16
        spriteSize = 16

    if patternMode == True:
        iconwidth = 256
        iconcanvascolumn = 10
    else:
        iconwidth = 128
        iconcanvascolumn = 8
    reset_mask_data()
    reset_pattern_data()
    init_draw_canvas()
    init_icon_canvases()
    add_palette_display()
    reset_pixels_display()
    add_labels_andpalmod()

    if r1:
        r1.destroy()
    if r0:
        r0.destroy()
    if s1:
        s1.destroy()
    if s0:
        s0.destroy()

    if patternMode == False:
        # add radials to swap between mask 1 and mask 2
        r1 = tk.Radiobutton(win, text='Mask 1', variable=mask, value=2, command=refresh_display)
        r1.grid(row=15, column=5, columnspan=3)
        r0 = tk.Radiobutton(win, text='Mask 0', variable=mask, value=1, command=refresh_display)
        r0.grid(row=15, column=2, columnspan=3)
        s1 = tk.Checkbutton(win, text='Show 1', variable=show_m2, command=refresh_display)
        s1.grid(row=16, column=5, columnspan=3)
        s0 = tk.Checkbutton(win, text='Show 0', variable=show_m1, command=refresh_display)
        s0.grid(row=16, column=2, columnspan=3)
        
    if patternMode == False:
        if l0:
            l0.destroy()
        if l1:
            l1.destroy()
        if l2:
            l2.destroy()
        if l3:
            l3.destroy()
        l0 = tk.Label(win, text='0 - 1')
        l0.grid(row=3, column=10, columnspan=2)
        l1 = tk.Label(win, text='2 - 3')
        l1.grid(row=3, column=12, columnspan=2)
        l2 = tk.Label(win, text='4 - 5')
        l2.grid(row=10, column=10, columnspan=2)
        l3 = tk.Label(win, text='6 - 7')
        l3.grid(row=10, column=12, columnspan=2)
    else:
        if l0:
            l0.destroy() 
        l0 = tk.Label(win, text='Pattern 0\nX: 0 Y: 0')
        l0.grid(row=12, column=12, columnspan=2)#, columnspan=2, rowspan=2)
        if l1:
            l1.destroy()
        l1 = tk.Label(win, text="Table 1 / 3")
        l1.grid(row=13, column=12, columnspan=2)
        if l2:
            l2.destroy()
        if l3:
            l3.destroy() 

    if patternMode == False:
        smallpixels1 = []
        smallpixels2 = []
        smallpixels3 = []
        smallpixels4 = []
        i = 0
        while i < 16:
            j = 0 
            while j < 16:
                smallpixels1.append(iconCanvas.create_rectangle((j*smalsize)+2, (i*smalsize)+2, ((j+1)*smalsize)+2, ((i+1)*smalsize)+2, fill='grey', outline=""))
                smallpixels2.append(iconCanvas.create_rectangle((j*smalsize)+66, (i*smalsize)+2, ((j+1)*smalsize)+66, ((i+1)*smalsize)+2, fill='grey', outline=""))
                smallpixels3.append(iconCanvas.create_rectangle((j*smalsize)+2, (i*smalsize)+66, ((j+1)*smalsize)+2, ((i+1)*smalsize)+66, fill='grey', outline=""))
                smallpixels4.append(iconCanvas.create_rectangle((j*smalsize)+66, (i*smalsize)+66, ((j+1)*smalsize)+66, ((i+1)*smalsize)+66, fill='grey', outline=""))
                j += 1
            i += 1

    smallpatternpx = []
    i = 0
    while i < (8*4):
        t = []
        smallpatternpx.append(t)
        i+=1

    if patternMode == True:
        i = 0
        while i < 4:
            j = 0
            while j < 8:
                y = 0
                while y < spriteSize:
                    x = 0
                    while x < spriteSize:
                        x1 = (j * (smalsize*spriteSize)) + (x*smalsize) + 2
                        x2 = (j * (smalsize*spriteSize)) + (x*smalsize) + smalsize + 2
                        y1 = (i * (smalsize*spriteSize)) + (y*smalsize) + 2
                        y2 = (i * (smalsize*spriteSize)) + (y*smalsize) + smalsize + 2
                        smallpatternpx[(i*8)+j].append(iconCanvas.create_rectangle(x1, y1, x2, y2, fill='grey', outline=""))
                        x+=1
                    y+=1
                j += 1
            i += 1

    if patternMode == False:
        iconCanvas.create_line(64+2, 0+2, 64+2, 128+2, fill='black')
        iconCanvas.create_line(0+2, 64+2, 128+2, 64+2, fill='black')
        draw_sprite_selector(0)
        refresh_display(True)
    if patternMode == True:
        iconCanvas.create_line(64+2, 0+2, 64+2, 128+2, fill='grey')
        iconCanvas.create_line(0+2, 64+2, 256+2, 64+2, fill='grey')
        iconCanvas.create_line(32+2, 0+2, 32+2, 128+2, fill='grey')
        iconCanvas.create_line(96+2, 0+2, 96+2, 128+2, fill='grey')
        iconCanvas.create_line(0+2, 32+2, 256+2, 32+2, fill='grey')
        iconCanvas.create_line(0+2, 96+2, 256+2, 96+2, fill='grey')
        iconCanvas.create_line(128+2, 0+2, 128+2, 128+2, fill='grey')
        iconCanvas.create_line(192+2, 0+2, 192+2, 128+2, fill='grey')
        iconCanvas.create_line(160+2, 0+2, 160+2, 128+2, fill='grey')
        iconCanvas.create_line(224+2, 0+2, 224+2, 128+2, fill='grey')
        update_pattern_icons()
        refresh_display(True)
    if bl:
        bl.destroy()
    if br:
        br.destroy()
    if bu:
        bu.destroy()
        bd.destroy()
        buu.destroy()
        bdd.destroy()
    if sr:
        sr.destroy()
        su.destroy()
        sl.destroy()
        sd.destroy()
    if patternMode == False:
        bl = tk.Button(win, text="←", command=page_back)
        bl.grid(row=11, column=11, columnspan=1)
        br = tk.Button(win, text="→", command=page_forward)
        br.grid(row=11, column=12, columnspan=1)
    else:
        bl = tk.Button(win, text="←", command=pattern_move_back)
        bl.grid(row=11, column=12, columnspan=1)
        br = tk.Button(win, text="→", command=pattern_move_fwd)
        br.grid(row=11, column=13, columnspan=1)
        bu = tk.Button(win, text="↑", command=pattern_move_up) 
        bu.grid(row=11, column=10)
        buu = tk.Button(win, text='⇈', command=pattern_page_up)
        buu.grid(row=11, column=11)
        bd = tk.Button(win, text="↓", command=pattern_move_down)
        bd.grid(row=12, column=10)
        bdd = tk.Button(win, text='⇊', command=pattern_page_down)
        bdd.grid(row=12, column=11)
    sr = tk.Button(win, text='⇒', command=shift_right)
    sr.grid(row=14, column=8, columnspan=2)
    sl = tk.Button(win, text='⇐', command=shift_left)
    sl.grid(row=14, column=6, columnspan=2)
    su = tk.Button(win, text='⇑', command=shift_up)
    su.grid(row=14, column=1, columnspan=2)
    sd = tk.Button(win, text='⇓', command=shift_down)
    sd.grid(row=14, column=3, columnspan=2)
    global filename 
    global asmfile 
    if loading==False:
        filename = ''
        asmfile = ''
    # Bind events
    drawCanvas.bind("<Button-1>", color_pixel)
    drawCanvas.bind("<B1-Motion>", color_pixel)
    drawCanvas.bind("<Button-3>", erase_pixel)
    drawCanvas.bind("<B3-Motion>", erase_pixel)
    drawCanvas.bind("<ButtonRelease-1>", set_undo_release)
    drawCanvas.bind("<ButtonRelease-3>", set_undo_release)
    
    if patternMode == True:
        fileMenu.entryconfigure(2, command=save_normal_pattern)
        fileMenu.entryconfigure(3, label='Save As .M2P...', command=save_pattern_as)
        fileMenu.entryconfigure(7, label='Export z80 pattern data...', command=export_asm_pattern)
    else: 
        fileMenu.entryconfigure(2, command=save_normal_sprite)
        fileMenu.entryconfigure(3, label='Save As .M2S...', command=save_sprite_as)
        fileMenu.entryconfigure(7, label='Export z80 sprite data...', command=export_asm_data)
    
    palette_display[1].clicked(0)

    app.bind("<Key>", keyboard_monitor)
    
    return

initialize_new(False)
# Run the app
app.resizable(False, False)
app.protocol("WM_DELETE_WINDOW", client_exit)
app.mainloop()
