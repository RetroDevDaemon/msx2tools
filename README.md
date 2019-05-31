# MSX2 Tools

## Release Notes:
Spr 1.33/Scr 1.22/Bmp 1.0: Initial public release.<br>
<br>
## Whussis?
MSX2 Tools is a set of open-source graphical tools for use specifically with the 9938 VDP, built entirely with the native Python 3 libraries. The Spriter and Screener tool were made with G3 (SCREEN 4) with Mode-2 sprites in mind, but can easily be adapted for use with G2 (SCREEN 3) and Mode-1 sprites.<br>
<br>
They can be used as-is with a single Python script file if you have Python installed (probably the best method), or by downloading the binaries and running them as executables. As long as you have Python 3.7 or above installed, they should work as-is without issue. 
<br>
### [MSX2 Spriter Manual](./spriter-manual.md)
Tool for creating sprites AND background/text patterns
### [MSX2 Screener Manual](./screener-manual.md)
Tool for creating screen maps used in SCREEN2/3 graphic modes utilizing patterns made using the Spriter tool
### [MSX2 Bitmapper Manual](./bitmapper-manual.md)
Tool for creating G4-G7 (SCREEN 5-8) bitmaps

<br><br>
Follow the links above for all the details.<br>

### Other Notes

The code is extremely ugly. I am not a professional coder by any means and this is mostly for personal use. I'm releasing it publically so maybe someone else will get some use out of it. 

IT'S SLOW! I use Tkinter rectangles to represent pixels, which means there are sometimes several thousand canvas updates happening. Hopefully it remains manageable even on slower systems. I've done quite a bit of optimizing, so right now the only noticable thing is importing and undo on the screener tool (which has a loading notification).

The icons for the toolbar were actually made using the tool, and inverting the byte order for X11-method bitmaps.

Feel free to contribute, clean up, or give me a shout-out :)<br>
<br>
(c)2019 Ben Ferguson<br>
Made with assistance from jlbeard83<br>
All tools created in Python3 
