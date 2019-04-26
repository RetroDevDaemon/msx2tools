#########################################################
# MSX2 Spriter
#
# (c) 2019 Ben Ferguson
#
# Use Python 3! (Coded in 3.7.1)
# 
# v1.0: First pass
#
# Assembles z80 byte data for GRAPHIC3 (screen 4)
#  / sprite mode 2 graphics for use with compilers.
# Easy point-and-click interface.
# 
##########################################################

# Imports 
import tkinter as tk
import sys 
import math 

# MSX2 default 16-color palette, in integer strings
defaultIntegerPalette = [
    '000', '000', '161', '373',
    '117', '237', '511', '267',
    '711', '733', '661', '664',
    '141', '625', '555', '777'
]
intpal = defaultIntegerPalette.copy()
# Each above integer must be divided by 7 then converted to hex.
displayPalette = []

# TK Setup
app = tk.Tk()
app.title('MSX2 Spriter')

# First, convert the integer palette to hexadecimal palette.    
def convert_int_pal_to_hex(integerPalette):
    global displayPalette
    displayPalette = None
    displayPalette = []
    i = 0
    while i < 16:
        if i == 0:
            displayPalette.append('grey')
        else:
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
# Run the pal conversion once
convert_int_pal_to_hex(intpal)

# Set up the default window frame
win = tk.Frame(master=app, width=800, height=600)
win.grid(row=16, columnspan=16)

# some globals
numSel = 0
currentColor = 'trans'
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
        return 'grey'
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
palette_display = []
i = 0
while i < 16:
    palette_display.append(PaletteButton(win, width=scale, height=scale, background=displayPalette[i]))
    palette_display[i].grid(row=1, column=i+1)
    palette_display[i].setVal(intpal[i])
    if i == 0:
        palette_display[i].myVal = 'trans'
    i += 1

# Refreshes the palette colors
def updatePaletteDisplay():
    i = 0
    global palette_display
    global displayPalette
    while i < 16:
        palette_display[i].configure(background=displayPalette[i])
        palette_display[i].setVal(intpal[i])
        if i == 0:
            palette_display[i].myVal = 'trans'
        i += 1
    return 

# Updates the current palette to the inputted values
def applyColorToSel():
    # 1) ensure input values are between 0-7 
    global currentColor
    oldcol = single_intcol_to_hex(currentColor)
    if oldcol != 'grey':
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
    return


# Changes all color of type x to type y 
def find_and_replace_pixels(oldcolor, newcolor):
    for n in pixels:
        if drawCanvas.itemcget(n, 'fill') == oldcolor:
            drawCanvas.itemconfig(n, fill=newcolor)
    return

# Changes the palette back to the default and re-paints image
def resetSelectedColor():
    global currentColor
    oldcol = single_intcol_to_hex(currentColor)
    if oldcol != 'grey':
        intpal[numSel] = defaultIntegerPalette[numSel]
        convert_int_pal_to_hex(intpal)
        currentColor = intpal[numSel]
        paintcol = single_intcol_to_hex(currentColor)
        updatePaletteDisplay()
        find_and_replace_pixels(oldcol, paintcol)
    refresh_display(True)
    return

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
    while i < 16:
        # TODO update 'grey' to transparent variable
        if mask.get() == 1:
            if pixels_mask1[(row*16)+i] != 0: 
                pixels_mask1[(row*16)+i] = currentPalNo
        if mask.get() == 2:
            if pixels_mask2[(row*16)+i] != 0:
                pixels_mask2[(row*16)+i] = currentPalNo    
        i += 1
    return

# Actually paints the pixel and changes the pal number in the mask array
def color_pixel(ob):
    x_px = math.floor(ob.x/pixelSize) 
    y_px = math.floor(ob.y/pixelSize)
    if ob.x < 0 or ob.x >= (spriteSize*pixelSize) or ob.y < 0 or ob.y >= (spriteSize*pixelSize):
        return 
    if mask.get() == 1:
        pixels_mask1[(y_px*spriteSize)+x_px] = currentPalNo
    if mask.get() == 2:
        pixels_mask2[(y_px*spriteSize)+x_px] = currentPalNo
    # TODO update this to trans
    if currentColor != 'trans':
        repaint_row(y_px)
    maskdata[page_ofs + (icon_selected*2)] = pixels_mask1.copy()
    maskdata[page_ofs + (icon_selected*2)+1] = pixels_mask2.copy()
    refresh_display(False)
    return

def erase_pixel(ob):
    global currentColor
    global currentPalNo 
    oldp = currentPalNo
    oldc = currentColor + '.'
    currentColor = 'trans'
    currentPalNo = 0
    color_pixel(ob)
    #print(oldc)
    currentPalNo = oldp
    currentColor = oldc[:-1]
    return 

pixelSize = 16
spriteSize = 16

# Both layers enabled?
def update_orlayer():
    orpixels = pixels_mask1.copy()
    i = 0
    while i < (spriteSize*spriteSize):
        if orpixels[i] != 0 and pixels_mask2[i] != 0:
            orpixels[i] = orpixels[i] | pixels_mask2[i] 
        elif orpixels[i] == 0 and pixels_mask2[i] != 0:
            orpixels[i] = pixels_mask2[i] 
        topaint = 'grey'
        cur_px = orpixels[i]
        if palette_display[cur_px].myVal != 'trans':
            intval = palette_display[cur_px].myVal
            topaint = single_intcol_to_hex(intval)
        drawCanvas.itemconfig(pixels[i], fill=topaint)
        i += 1
    return

# Just layer 2 enabled
def update_layermask_2():
    i = 0
    global pixels_mask2
    global palette_display
    while i < (spriteSize * spriteSize):
        topaint = 'grey'
        cur_px = pixels_mask2[i]
        if palette_display[cur_px].myVal != 'trans':
            intval = palette_display[cur_px].myVal
            topaint = single_intcol_to_hex(intval)
        drawCanvas.itemconfig(pixels[i], fill=topaint)
        i += 1
    return 

# Just layer 1 enabled
def update_layermask_1():
    i = 0
    global pixels_mask1
    global palette_display
    while i < (spriteSize * spriteSize):
        topaint = 'grey'
        cur_px = pixels_mask1[i]
        if palette_display[cur_px].myVal != 'trans':
            intval = palette_display[cur_px].myVal
            topaint = single_intcol_to_hex(intval)
        drawCanvas.itemconfig(pixels[i], fill=topaint)
        i += 1
    return 

# Add sub-canvas for drawing, and palette value arrays
drawCanvas = tk.Canvas(win, background='white', width=pixelSize*spriteSize, height=pixelSize*spriteSize)
drawCanvas.grid(row=3, column=0, columnspan=10, rowspan=10)
# populate with pixel grid
pixels = []
# the mask arrays are actual PALETTE values 0-15.
pixels_mask1 = []
pixels_mask2 = []
i = 0
while i < spriteSize:
    j = 0
    while j < spriteSize:
        #create_rectangle's
        pixels.append(drawCanvas.create_rectangle(j*pixelSize, i*pixelSize, (j+1)*pixelSize, (i+1)*pixelSize, outline='black', fill='grey'))
        pixels_mask1.append(0)
        pixels_mask2.append(0)
        j += 1
    i += 1
 #

# Bind events
drawCanvas.bind("<Button-1>", color_pixel)
drawCanvas.bind("<B1-Motion>", color_pixel)
drawCanvas.bind("<Button-3>", erase_pixel)
drawCanvas.bind("<B3-Motion>", erase_pixel)

# Radial bools have to be defined as tk variables
show_m1 = tk.BooleanVar()
show_m1.set(True)
show_m2 = tk.BooleanVar()
show_m2.set(True)

# Universally updates all 256 pixels
def refresh_display(allicons=False):
    transparent = 'grey'
    i = 0
    while i < (spriteSize*spriteSize):
        drawCanvas.itemconfig(pixels[i], fill=transparent)
        i += 1
    if show_m1.get() == True and show_m2.get() == True:
        update_orlayer()
    elif show_m1.get() == True and show_m2.get() == False:
        update_layermask_1()
    elif show_m2.get() == True and show_m1.get() == False:
        update_layermask_2()
    if allicons == False:
        global icon_selected
        update_icon_window(icon_selected)
    else:
        i = 0
        while i < 4:
            update_icon_window(i)
            i += 1
 #

# add radials to swap between mask 1 and mask 2
r1 = tk.Radiobutton(win, text='Mask 1', variable=mask, value=2, command=refresh_display)
r1.grid(row=14, column=4, columnspan=3)
r0 = tk.Radiobutton(win, text='Mask 0', variable=mask, value=1, command=refresh_display)
r0.grid(row=14, column=1, columnspan=3)
s1 = tk.Checkbutton(win, text='Show 1', variable=show_m2, command=refresh_display)
s1.grid(row=15, column=4, columnspan=3)
s0 = tk.Checkbutton(win, text='Show 0', variable=show_m1, command=refresh_display)
s0.grid(row=15, column=1, columnspan=3)

# TODO s:

icon_selected = 0

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
#=maskdata[32][256]
page_ofs = 0
def select_from_icon(obj):
    global page_ofs
    global icon_selected
    global pixels_mask1
    global pixels_mask2
    # first, copy current pixel mask into maskdata[].
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
    refresh_display(False)
    return 

iconCanvas = tk.Canvas(win,background='grey',width=128+2,height=128+2)
l0 = tk.Label(win, text='0 - 1')
l0.grid(row=3, column=10, columnspan=2)
l1 = tk.Label(win, text='2 - 3')
l1.grid(row=3, column=12, columnspan=2)
iconCanvas.grid(row=3, column=10, columnspan=4, rowspan=8)
l2 = tk.Label(win, text='4 - 5')
l2.grid(row=10, column=10, columnspan=2)
l3 = tk.Label(win, text='6 - 7')
l3.grid(row=10, column=12, columnspan=2)
iconCanvas.bind("<Button-1>", select_from_icon)

def update_label_txt():
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
    return 

smallpixels1 = []
smallpixels2 = []
smallpixels3 = []
smallpixels4 = []
smalsize = 4
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
iconCanvas.create_line(64+2, 0+2, 64+2, 128+2)
iconCanvas.create_line(0+2, 64+2, 128+2, 64+2)


def update_icon_window(win_no):
    # Both layers!
    global icon_selected
    global page_ofs 
    orpixels = maskdata[(win_no*2)+page_ofs].copy() 
    or2pixels = maskdata[(win_no*2)+page_ofs+1].copy()
    i = 0
    while i < (spriteSize*spriteSize):
        if orpixels[i] != 0 and or2pixels[i] != 0:
            orpixels[i] = orpixels[i] | or2pixels[i] 
        elif orpixels[i] == 0 and or2pixels[i] != 0:
            orpixels[i] = or2pixels[i] 
        topaint = 'grey'
        cur_px = orpixels[i]
        if palette_display[cur_px].myVal != 'trans':
            intval = palette_display[cur_px].myVal
            topaint = single_intcol_to_hex(intval)
        if win_no == 0:
            iconCanvas.itemconfig(smallpixels1[i], fill=topaint)
        elif win_no == 1:
            iconCanvas.itemconfig(smallpixels2[i], fill=topaint)
        elif win_no == 2:
            iconCanvas.itemconfig(smallpixels3[i], fill=topaint)
        elif win_no == 3:
            iconCanvas.itemconfig(smallpixels4[i], fill=topaint)
        i += 1
    return
    
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
    return 
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
    return 
tk.Button(win, text="<", command=page_back).grid(row=11, column=11, columnspan=1)
tk.Button(win, text=">", command=page_forward).grid(row=11, column=12, columnspan=1)

# 3. export and import palette and sprites as DBs
from tkinter import filedialog
filename = ''

def save_as():
    global filename 
    filename = tk.filedialog.asksaveasfilename(title='Save MSX2 Spriter file', filetypes=( ('MSX2 Spriter file', '*.m2s'),('All files', '*.*') ))
    if filename == '':
        return 
    savem2s()
    return
def load_as():
    global filename 
    filename = tk.filedialog.askopenfilename(title='Load MSX2 Spriter file', filetypes=( ('MSX2 Spriter file', '*.m2s'),('All files', '*.*') ))
    if filename == '':
        return 
    loadm2s()
    return 

## Z80 ASSEMBLY EXPORT - THE GOOD SHIT ##    
asmfile = ''
def export_asm_data():
    global asmfile 
    asmfile = tk.filedialog.asksaveasfilename(title='Save MSX2 sprite assembly data', filetypes=( ('Z80 assembly data', '*.z80'),('All files', '*.*') ))
    if asmfile == '':
        return 
    outdata = []
    outdata.append("; Made with MSX2 Spriter")
    # Gotta do palette shit first 
    i = 0
    while i < 32:
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
                    outb = '{:02x}'.format(md)
                x += 1
            y += 1
            if outb == '':
                curline.append(' $00,')
            else:
                curline.append(' ${},'.format(outb))
        #print(curline)
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
                    outb = '{:02x}'.format(md)
                x += 1
            y += 1
            if outb == '':
                curline.append(' $00,')
            else:
                curline.append(' ${},'.format(outb))
        #print(curline)
        curline = ''.join(curline)[:-1]
        outdata.append(curline)

        i += 1
    # NOW do sprite stuff
    i = 0
    while i < 32:
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
        #print(curline)
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
        #print(curline)
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
        #print(curline)
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
        #print(curline)
        outdata.append(curline)
        i += 1
    #print(outdata)
    f = open(asmfile, 'w')
    for s in outdata:
        f.write(s)
        f.write('\n')
    f.close()
    #
    return 
def import_data():
    return 


tk.Button(win, text='Save file...', command=save_as).grid(row=6, column=14, columnspan=3)
tk.Button(win, text='Load file...', command=load_as).grid(row=7, column=14, columnspan=3)
tk.Button(win, text='Export as...', command=export_asm_data).grid(row=8, column=14, columnspan=3)
#tk.Button(win, text='Import data', command=import_data).grid(row=9, column=14, columnspan=3)

def loadm2s():
    f = open(filename, 'r')
    data = f.readline()
    # reset palette data
    global palette_display
    global currentColor
    palette_vals = data.split(',')
    i = 0
    while i < 16:
        palette_display[i].myVal = palette_vals[i]
        currentColor = i 
        i += 1
    resetPalette(palette_vals)
    currentColor = 'trans'
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
    return 

def resetPalette(newpal):
    global intpal 
    intpal = newpal 
    convert_int_pal_to_hex(intpal)
    updatePaletteDisplay()
    return 

def savem2s():
    p = []
    for n in palette_display:
        p.append(n.myVal)
    f = open(filename, 'w')
    for item in p: 
        f.write('%s,' % item)
    for n in maskdata:
        f.write('\n')
        for item in n:
            f.write('%s,'%item)
    f.close()
    return

# Run the app
app.mainloop()