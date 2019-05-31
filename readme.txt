MSX2 Tools
Release Notes:
Spr 1.33/Scr 1.22/Bmp 1.0: Initial public release.


Whussis?
MSX2 Tools is a set of open-source graphical tools for use specifically with the 9938 VDP, built entirely with the native Python 3 libraries. The Spriter and Screener tool were made with G3 (SCREEN 4) with Mode-2 sprites in mind, but can easily be adapted for use with G2 (SCREEN 3) and Mode-1 sprites.

They can be used as-is with a single Python script file if you have Python installed (probably the best method), or by downloading the binaries and running them as executables. As long as you have Python 3.7 or above installed, they should work as-is without issue. 

MSX2 Spriter
Tool for creating sprites AND background/text patterns

MSX2 Screener
Tool for creating screen maps used in SCREEN2/3 graphic modes utilizing patterns made using the Spriter tool

MSX2 Bitmapper
Tool for creating G4-G7 (SCREEN 5-8) bitmaps


Other Notes
The code is extremely ugly. I am not a professional coder by any means and this is mostly for personal use. I'm releasing it publically so maybe someone else will get some use out of it.

IT'S SLOW! I use Tkinter rectangles to represent pixels, which means there are sometimes several thousand canvas updates happening. Hopefully it remains manageable even on slower systems. I've done quite a bit of optimizing, so right now the only noticable thing is importing and undo on the screener tool (which has a loading notification).

The icons for the toolbar were actually made using the tool, and inverting the byte order for X11-method bitmaps.

Feel free to contribute, clean up, or give me a shout-out :)

(c)2019 Ben Ferguson
Made with assistance from jlbeard83
All tools created in Python3

-------------------------------------------------

MSX2 Spriter v1.33
Features
-Support for a full 32-mask, dual-layered sprite set at once
-Single/double mask view toggle
-Automatic color correction and OR coloring for sprite masks; automatic color correction for patterns
-Transparency color selection
-Color picker, fill tool 
-Cut, copy, paste of masks
-100-step undo and redo
-Horizontal and vertical flip
-Four directional shift
-Bitwise invert (0>1 and vice versa)
-Native compressed file format
-Export to z80 assembly code AND bytes-only
-Palette import and export
-Pattern support for full 768 tiles
-Optional triplicate for pattern export

Usage
The palette at the top of the screen is the default MSX2 palette. To modify these colors, simply select the color, input new RGB values in the edit boxes (values of 0-7), and select Apply. The Reset button will change the selected color back to the MSX2 system default. You can also drag and drop palette entries to rearrange them. This will automatically swap their associated colors for all current sprites.

Note that the first color (color 0) is transparent for sprites. Its value can be changed, but for practical purposes this is cosmetic.

Instructions:
-The left mouse button draws the selected color, and the right mouse button erases (draws transparent).
-MSX2 Spriter will automatically color-correct. This means the image will always be MSX2 compliant, but colors might change when you don't expect them to. Check below for sprite mode limitations.
-Note that TWO sprite masks are selected at a time, and all sprites are currently limited to 16x16 mode. 'Mask' in this context refers to one of the two 16x16 pixel blocks that make up a combined sprite.
-Only one mask can be drawn on at a time. Use the radio button beneath the draw area to swap between the two currently displayed masks.
-Use the checkbox buttons to toggle visibility of the two currently displayed masks.
-Holding the Shift key temporarily toggles to the color picker (eyedropper).
-Click the small sprite display to swap between the two masks currently being edited.
-Click the arrows to swap between pages (there are four, to constitute a full MSX2 mode-2 sprite set).
-The arrows underneath the draw area allow you to shift in all four directions. This does not add to the undo queue, since this is very easy to fix yourself with a click.
-The toolbar at the top of the screen represents, in order: Save, Pixel, Pick color, Fill, Cut, Copy, Paste, Undo, Redo, Flip Horiz., Flip Vertical, Invert. These options are all in the Edit menu as well (Save is in File).
-To use a palette from another M2S or M2P file in your current file, choose 'Import palette from...' option from the File menu.

Save, Load, and Export
The tool uses a text-based format that just stores the raw data as *.m2s (MSX2 Spriter format), which is then zipped. These files also retain palette data and saving and loading should be fully functional.

To use the sprites in assembly language programs, use Export z80 sprite data... (or raw bytes) from the Export menu. It will export assembler data byte format which should be compatible with almost all z80-language compilers, e.g.

DB $00, $00, $00, $02, $06, $04, $0a, $1f

The color data is included as bytes above the sprite mask data so an entire set can be loaded into MSX2 memory all in one go.

(The exporter will only export masks and pattern tables that are NOT empty, but these are annotated in the z80 export. Raw bytes export will export the entire sequence, including blank masks, up until the last non-empty mask.)

To export the universal palette, use the Export z80 palette data... (or raw bytes) option. As above, it will export assembler data byte format in sequence to be loaded into register #16.

As of 1.1, you can also create pattern sets for backgrounds!

To switch to pattern mode, select New pattern file from the File menu. 

Instructions for Pattern mode:
-As above, the left mouse button draws a color, the right mouse button draws transparent.
-Also as with sprite mode, the patterns are always MSX2 color-compliant. Check below for pattern mode limitations.
-One pattern is one 8x8 pixel block. There are 3 tables of 256 (32x8) patterns, but only one 8x4 section of the entire 32x24 (768) editable segment is visible at once.
-Use the arrow buttons to scroll the visible patterns up, down, left and right.
-As above, click the pattern you wish to edit. Only one pattern can be edited at a time.
-When exporting patterns as z80 data, two files will be exported - filename.z80 and filename_colors.z80. The _colors file must be loaded at a different area of memory, so it is exported seperately. Text inside of the files reminds you that the default VDP locations for pattern generator is $0000 and colors is $2000. The files themselves are also annotated per-row so you know which tile goes where.

MSX2 Mode-2 Sprite Limitations
Keep in mind the following restrictions:

Each individual mask can only have one color per row, but a total of 16 colors (one for each row, including transparent).
When two masks are overlaid, if the higher-order mask has bit 6 of its color bytes set, the overlapping pixels have their palette values OR-ed (e.g. palette number 1 overlaid with palette number 2 will produce palette number 3 (0001 | 0010 = 0011). MSX2 Spriter does this automatically for higher-order masks (every odd). Refer to this link for more information:
https://www.msx.org/wiki/The_OR_Color
In sprite mode 2, 8 sprite masks can be displayed on a single scanline, which means with overlaid sprites that restriction is reduced to an effective 4.
MSX2 GRAPHIC3 Pattern Limitations
GRAPHIC3 background patterns are surprisingly lenient:

Each pattern can have 16 colors (the entire palette, transparent included).
Only two colors can co-exist on the same pixel row - this includes transparent (color 0).
Each third of the screen needs its own pattern table.

-----------------------------------------------

MSX2 Screener v1.22
Features
-Native compressed format
-Export in z80 code and raw bytes
-Support for hot-swapping pattern files
-100-step undo and redo
-Selection and cut/copy/paste
-Automatic tile swapping when drawing each pattern region

Usage (Screener tool):
As above, copy or download msx2screener.py locally to your computer. To make use of the screener tool, you need a pattern (M2P) file created with the Spriter tool. You execute it with:

$ python3 ./msx2screener.py


Instructions for Screener tool:
-You need to load in an M2P pattern file from the Spriter tool before painting a screen. (Sorry, no support for standard images yet!)
-Screen patterns are limited to one-third sections of the screen. Patterns 0-255 are for the top third, 256-511 for the middle, and 512-767 for the bottom.
-Click any of the patterns on each of the pattern windows to select a 'paintbrush' for that section of the screen. After doing this, painting is natural and fluid - you can drag your mouse between the screen's third-sections and continue painting with the selected neighboring pattern.
-Right click to set that tile to whatever is set to tile '0' in that section. 
-When creating a new screen file, all tiles will be filled in by default with tile '0'. It is recommended this tile is fully transparent (color 0).
-You can freely change screen files and pattern files. Import a new M2P to change the current screen's pattern graphics, or load/create a new M2C and the tool will ask if you want to change your current pattern set.
-Exporting is nice and easy - 768 bytes, one per tile, each valued 0-255. Formatting is the same as described above.

-----------------------------------------------

MSX2 Bitmapper v1.0
Features
-Support for all four 9938 VDP bitmap modes - G4-G7 (aka SCREEN 5-8)
-Support for both vertical resolutions - 192 and 212 (displayed by setting bit 7 in R#9)
-Support for interlaced bitmaps @ 384 and 424 px resolutions (bits 2 and 3 ste to 1 in R#9)
-Proper color/palette configuration for all modes
-Easy pop-up palette swapping (and palette z80 export)
-(Only slightly buggy) window scaling
-1x, 2x, 4x, 8x pixel zoom
-Box selection and cut/copy/paste
-1-9 px brush size
-Square and diamond shape brushes
-Line, circle, and square shape drawing
-Flood-fill and color swap
-100-step undo and redo
-File formats: native compressed (gzip), export support for both z80 assembler and raw bytes 


How to use

On start, the app will load a G4 mode bitmap with 192 vertical resolution. In order, the icons in the toolbar are:
Save, Draw, Line, Circle, Square, (brush size), Fill, Select, Cut, Copy, Paste, Undo, Redo, Scale window, and four zoom levels.

To change a color in the palette, right click the color, and select the new palette color. In all but G7 modes, you have access to the full 512 color MSX2 palette, and that palette value will automatically swapped if already painted to the canvas. In G7 mode, blues are halved, and colors will not be swapped on the canvas.

In most draw modes, right click and drag will move the canvas if at a zoom level higher than 1x. Left click will draw (or fill), and when in shape mode, left click and drag will expand the shape.
Keyboard shortcuts are:
Ctrl+S: Save
Ctrl+Z: Undo
Ctrl+Y: Redo
(Available in selection mode):
Ctrl+X: Cut 
Ctrl+C: Copy 
Ctrl+V: Paste 

When in selection mode, drag to box-select the desired area, then use cut or copy. A single click elsehwere on the canvas will automatically show the pastable area (a drag will create a new selection but will otherwise have no affect on the clipboard).
Fill mode is slow! It's generally faster, if you are swapping an entire color, to simply do this on the palette. Fill is animated so you can see your progress, as is Undo. 

The window will default to 2x pixel size (minimum). Depending on the resolution of your monitor, clicking the scale button will increase the pixel size by 1 until filling your screen, then clicking it again will reset it to 2x. This has been tested at 720p and 1080p, but you might see artifacts or weird empty space at 1440p and above. The pixel grid is also generally only viewable at 4x 8x zoom, but this depends on your screen resolution/scale as well.


Exports in z80 are formatted as:
DB $00, $00, $00...
This should be a universal format compatible with all compilers. If your compiler doesn't like $-notation, you can always use the raw bytes export. 
Note that raw byte export for interlaced mode exports both bitmap tables as one file. If this is unacceptable, you can easily split them using the z80 export, or by simply chopping the file in half. 


Other Notes
-It's very slow! Interlaced images, being double the amount of pixels, can have a very low framerate on refresh. Windows 10 with integrated graphics in particular has trouble with the Tkinter library, but on Linux/Mac and a graphics-accelerated PC this should be much less noticable. Zoomed-in displays fewer canvas objects as well, which should be faster overall.
-Fill and undo is animated so it feels less laggy.
-If you want to view the .m2b files in raw, simply add a .zip extension and extract what's inside.