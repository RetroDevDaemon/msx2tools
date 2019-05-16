# MSX2 Spriter v1.28 / Screener v1.2

Python3 tool for creating/exporting dual-masked mode 2 (GRAPHIC3/screen4) sprites, patterns, and screen layouts.


### Release notes:

1.28: Added icon toolbar to both tools, box select to screen tool, and horizontal/vertical flip for sprite tool.<br>
1.27: Added import of palettes from other M2S/M2P files.<br>
1.26: Added UDLR shifting of sprites and patterns. (This does NOT add to the undo queue, since it's easy to undo yourself). <br>
1.25: Added 100-step undo/redo and various bug fixes <br>
1.22: Keyboard shortcuts for copy/paste sprites, fix for transparency color change<br>
1.21: Added transparency selection/display to sprite mode, added copy/paste mask data<br>
1.2: Added Screener tool, fixed various bugs, added visible selector<br>
1.1: Added PATTERN mode! <br>
1.02: Moved file options to menu bar, added New file functionality<br>
1.01: Fixed issue with high-order mask not having CC bit set. (Apologies!)<br>
1.00: Initial release.


## Usage (Spriter tool):
You must have a fairly recent verson of Python installed in order to use this app. It was developed on Python 3.7.1 but should run on any Python installation that has Tkinter included (which is most of the recent ones). It does not use any additional libraries. It has been fully tested on both Windows 10 and Ubuntu Linux.

To start it, download (or copy) msx2spriter.py to any folder on a computer with Python installed and run:

`$ python3 ./msx2spriter.py`

The following window will open:

![ss1](m2s6.png)

The palette at the top of the screen is the default MSX2 palette. To modify these colors, simply select the color, input new RGB values in the edit boxes (values of 0-7), and select **Apply**. The **Reset** button will change the selected color back to the MSX2 system default.

_Note that the first color (color 0) is transparent for sprites. Its value can be changed, but for practical purposes this is cosmetic._

Instructions:<br>
-The left mouse button draws the selected color, and the right mouse button erases (draws transparent).<br>
-_MSX2 Spriter will automatically color-correct._ This means the image will always be MSX2 compliant, but colors might change when you don't expect them to. Check below for sprite mode limitations.<br>
-**Note that TWO sprite masks are selected at a time, and all sprites are currently limited to 16x16 mode**. 'Mask' in this context refers to one of the two 16x16 pixel blocks that make up a combined sprite.<br>
-Only one mask can be drawn on at a time. Use the radio button beneath the draw area to swap between the two currently displayed masks.<br>
-Use the checkbox buttons to toggle visibility of the two currently displayed masks.<br>
-Click the small sprite display to swap between the two masks currently being edited.<br>
-Click the arrows to swap between pages (there are four, to constitute a full MSX2 mode-2 sprite set).<br>
-The arrows underneath the draw area allow you to shift in all four directions.<br>
-The toolbar at the top of the screen represents, in order: Save, Pixel (draw mode cannot be changed at this time), Cut, Copy, Paste, Undo, Redo, Flip Horiz. and Flip Vertical. These options are all in the Edit menu as well (Save is in File).<br>
-To use a palette from another M2S or M2P file in your current file, choose 'Import palette from...' option from the File menu.<br>

### Save, Load, and Export

The tool uses a text-based format that just stores the raw data as __\*.m2s__ (MSX2 Spriter format). These files also retain palette data and saving and loading should be fully functional.

To use the sprites in assembly language programs, use **Export z80 sprite data...** from the File menu. It will export assembler data byte format which should be compatible with almost all z80-language compilers, e.g.

 `DB  $00, $00, $00, $02, $06, $04, $0a, $1f`

The color data is included as bytes above the sprite mask data so an entire set can be loaded into MSX2 memory all in one go. 

(Note that as of v1.0 the exporter will export all 32 masks and color data. You'll have to cherry pick them if you only want to include some of them.)

To export the universal palette, use the **Export z80 palette data...** option. As above, it will export assembler data byte format in sequence to be loaded into register #16. 

As of 1.1, you can also create pattern sets for backgrounds!

To switch to pattern mode, select **New pattern file** from the File menu. You will be greeted with a screen similar to the following:

![ss2](m2s7.png)

Instructions for **Pattern mode**:<br>
-As above, the left mouse button draws a color, the right mouse button draws transparent.<br>
-Also as with sprite mode, the patterns are always MSX2 color-compliant. Check below for pattern mode limitations.<br>
-One pattern is one 8x8 pixel block. There are 3 tables of 256 (32x8) patterns, but only one 8x4 section of the entire 32x24 (768) editable segment is visible at once.<br>
-Use the arrow buttons to scroll the visible patterns up, down, left and right.<br>
-As above, click the pattern you wish to edit. Only one pattern can be edited at a time.<br>
-When exporting patterns as z80 data, **two** files will be exported - filename.z80 and filename_colors.z80. The _colors file must be loaded at a different area of memory, so it is exported seperately. Text inside of the files reminds you that the default VDP locations for pattern generator is $0000 and colors is $2000. The files themselves are also tagged per-row so you know which tile goes where.<br>

If you are using this with a compiler such as sjasm, you might want to include a line such as the following at the top of the exported .z80 file and compile it to be included as a raw binary:

` output sprites.bin`


## Usage (Screener tool):
As above, copy or download `msx2screener.py` locally to your computer. To make use of the screener tool, you need a pattern (M2P) file created with the Spriter tool. You execute it with:<br>

`$ python3 ./msx2screener.py`<br>

The window looks like this:<br>

![ss2](m2s5.png)


Instructions for **Screener tool**:<br>
-You need to load in an M2P pattern file from the Spriter tool before painting a screen. (Sorry, no support for standard images yet!)<br>
-Screen patterns are limited to one-third sections of the screen. Patterns 0-255 are for the top third, 256-511 for the middle, and 512-767 for the bottom.<br>
-Click any of the patterns on each of the pattern windows to select a 'paintbrush' for that section of the screen. After doing this, painting is natural and fluid - you can drag your mouse between the screen's third-sections and continue painting with the selected neighboring pattern.<br>
-Right click to set that tile to whatever is set to tile '0' in that section. <br>
-When creating a new screen file, all tiles will be filled in by default with tile '0'. It is recommended this tile is fully transparent (color 0).<br>
-You can freely change screen files and pattern files. Import a new M2P to change the current screen's pattern graphics, or load/create a new M2C and the tool will ask if you want to change your current pattern set.<br>
-Exporting is nice and easy - 768 bytes, one per tile, each valued 0-255. Formatting is the same as described above.<br>


### MSX2 Mode-2 Sprite Limitations

Keep in mind the following restrictions:
1. Each _individual mask_ can only have one color per row, but a total of 16 colors (one for each row, including transparent).<br>
2. When two masks are overlaid, if the higher-order mask has bit 6 of its color bytes set, the overlapping pixels have their palette values OR-ed (e.g. palette number 1 overlaid with palette number 2 will produce palette number 3 (0001 | 0010 = 0011). MSX2 Spriter does this automatically for higher-order masks (every odd). Refer to this link for more information:<br>
https://www.msx.org/wiki/The_OR_Color<br>
3. In sprite mode 2, 8 sprite masks can be displayed on a single scanline, which means with overlaid sprites that restriction is reduced to an effective 4.


### MSX2 GRAPHIC3 Pattern Limitations

GRAPHIC3 background patterns are surprisingly lenient:<br>
1. Each pattern can have 16 colors (the entire palette, transparent included).<br>
2. Only two colors can co-exist on the same pixel row - this includes transparent (color 0).<br>
3. Each third of the screen needs its own pattern table.


### Other Notes

The code is extremely ugly. I am not a professional coder by any means and this is mostly for personal use. I'm releasing it publically so maybe someone else will get some use out of it. 

IT'S SLOW! I use Tkinter rectangles to represent pixels, which means there are sometimes several thousand canvas updates happening. Hopefully it remains manageable even on slower systems. I've done quite a bit of optimizing, so right now the only noticable thing is importing and undo on the screener tool (which has a loading notification).

The icons for the toolbar were actually made using the tool, and inverting the byte order for X11-method bitmaps.

More QoL features coming soon!

Feel free to contribute, clean up, or give me a shout-out :)
