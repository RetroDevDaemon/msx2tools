# MSX2 Bitmapper v1.1

## Release notes
1.1<br>
-Added pattern-mode export for GRAPHIC-1 and GRAPHIC-2 modes<br>
-Added color map reduction for pattern mode compatibility<br>
-Added selection-only export for all graphic modes<br>

## Features
-Support for all four 9938 VDP bitmap modes - G4-G7 (aka SCREEN 5-8)<br>
-Support for both vertical resolutions - 192 and 212 (displayed by setting bit 7 in R#9)<br>
-Support for interlaced bitmaps @ 384 and 424 px resolutions (bits 2 and 3 ste to 1 in R#9)<br>
-Proper color/palette configuration for all modes<br>
-Easy pop-up palette swapping (and palette z80 export)<br>
-(Only slightly buggy) window scaling<br>
-1x, 2x, 4x, 8x pixel zoom<br>
-Box selection and cut/copy/paste<br>
-1-9 px brush size<br>
-Square and diamond shape brushes<br>
-Line, circle, and square shape and filled-shape drawing<br>
-Flood-fill and color swap<br>
-100-step undo and redo<br>
-File formats: native compressed (gzip), export support for both z80 assembler and raw bytes
<br>
<br>
## How to use
![ss4](m2s8.png)<br>
On start, the app will load a G4 mode bitmap with 192 vertical resolution. In order, the icons in the toolbar are:<br>
Save, Draw, Line, Circle, Square, (brush size), Fill, Select, Cut, Copy, Paste, Undo, Redo, Scale window, and four zoom levels.<br><br>
To change a color in the palette, right click the color, and select the new palette color. In all but G7 modes, you have access to the full 512 color MSX2 palette, and that palette value will automatically swapped if already painted to the canvas. In G7 mode, blues are halved, and colors will not be swapped on the canvas.<br><br>
In pixel draw and line draw mode, right click and drag will move the canvas if at a zoom level higher than 1x. Left click will draw (or fill), and when in shape mode, left click and drag will expand the shape. When drawing a square or circle, you can use RMB instead to create a filled version. These are also slow, but animate their progress if particularly large.<br>
Keyboard shortcuts are:<br>
Ctrl+S: Save<br>
Ctrl+Z: Undo<br>
Ctrl+Y: Redo<br>
(Available in selection mode):<br>
Ctrl+X: Cut <br>
Ctrl+C: Copy <br>
Ctrl+V: Paste <br>
<br>
When in selection mode, drag to box-select the desired area, then use cut or copy. A single click elsehwere on the canvas will automatically show the pastable area (a drag will create a new selection but will otherwise have no affect on the clipboard).<br>
When in selection mode you can also use <b>selection export</b>. This will export the raw bytes only of whatever is currently selected in any graphic mode. This is useful if your game uses a lot of bitmaps of varying sizes.<br>
<b>Fill mode</b> is slow! It's generally faster, if you are swapping an entire color, to simply do this on the palette. Fill is animated so you can see your progress, as is Undo. <br>
<b>Pattern export</b> is also possible. At the moment this only works on GRAPHIC-4 bitmaps. This exports the entire image into a series of 768 patterns, either in raw byte form or in M2P form for use with the Spriter tool. Doing this will automatically perform <b>color map reduction</b>, which reduces the color map to G1 and G2 compatible pattern colors. This may cause artificing if your bitmap uses lots of color in detail, but generally works pretty well. This can also be done manually in mode G6. Data from G6 can either copied to a new G4 mode image or exported by selection.
<br>
<br>
The window will default to 2x pixel size (minimum). Depending on the resolution of your monitor, clicking the scale button will increase the pixel size by 1 until filling your screen, then clicking it again will reset it to 2x. This has been tested at 720p and 1080p, but you might see artifacts or weird empty space at 1440p and above. The pixel grid is also generally only viewable at 4x 8x zoom, but this depends on your screen resolution/scale as well.<br><br>

Exports in z80 are formatted as:<br>
` DB  $00, $00, $00...`<br>
This should be a universal format compatible with all compilers. If your compiler doesn't like $-notation, you can always use the raw bytes export. <br>
<b>Note that raw byte export for interlaced mode exports both bitmap tables as one file.</b> If this is unacceptable, you can easily split them using the z80 export, or by simply chopping the file in half.
<br><br>
## Other Notes
-It's very slow! Interlaced images, being double the amount of pixels, can have a very low framerate on refresh. Windows 10 with integrated graphics in particular has trouble with the Tkinter library, but on Linux/Mac and a graphics-accelerated PC this should be much less noticable. Zoomed-in displays fewer canvas objects as well, which should be faster overall.<br>
-Fill and undo is animated so it feels less laggy.<br>
-If you want to view the .m2b files in raw, simply add a .zip extension and extract what's inside.<br>
