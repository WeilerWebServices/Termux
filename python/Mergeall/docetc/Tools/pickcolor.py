#!/usr/bin/python
"""
===============================================================================
pickcolor.py - utility script for frigcal (and others)

Select a color, display it on a button, and show its #RRGGBB hex-string value
for copy/paste into frigcal config files, [tT]kinter keywords, or webpage tags.
Use Ctrl-C/Ctrl-V to copy/paste (command-C/V on Macs) and resize the GUI's 
window for a larger view of the selected color.  Borrowed from the book 
"Programming Python, 4th Edition", with a slightly extended GUI here.

Update June 2017: this now both:

- Displays the color and RGB string of a color chosen in a GUI dialog
- Displays the color of an RGB string entered in the entry field

The latter is new: to enter an RGB string and see its color, enclose the 
string in single quotes anywhere in the entry field at the bottom of the 
display, and press Enter/return (e.g., .... '#d5f9ff'....).  Any text 
surrounding the quoted string is ignored (and Tk allows some mistakes).

About the split:
"'xx'".split("'")       => ['', 'xx', '']
"aaa'xx'".split("'")    => ['aaa', 'xx', '']
"'xx'bbb".split("'")    => ['', 'xx', 'bbb']
"aaa'xx'bbb".split("'") => ['aaa', 'xx', 'bbb']
===============================================================================
"""

import sys
if sys.version[0] == '2':                   # for Python 3.X or 2.X
    from Tkinter import *
    from tkColorChooser import askcolor
    from tkMessageBox import showinfo
elif sys.version[0] == '3':
    from tkinter import *
    from tkinter.colorchooser import askcolor
    from tkinter.messagebox import showinfo

def selectedColor():
    # dialog -> display
    (triple, hexstr) = askcolor()
    if hexstr:
        print(hexstr)
        push.config(bg=hexstr)
        show.set("#RRGGBB string = '" + hexstr + "'")

def enteredColor(tkevent):
    # input -> display
    text = show.get()
    try:
        hexstr = text.split("'")[1]
        print(hexstr)
        push.config(bg=hexstr)
        show.set("#RRGGBB string = '" + hexstr + "'")
    except:     
        message=('Sorry - cannot set color from input.  '
                 'Make sure it is entered using format \'#RRGGBB\' '
                 'in the input field.  Include the quotes and #, ' 
                 'and use hex digits (0..F) for R, G, and B.')
        showinfo(parent=root, title='pickcolor - bad RGB', message=message)

root = Tk()
root.title('pickcolor')

if sys.platform.startswith('darwin'):
    # Mac OS X Tk doesn't do bg color on buttons
    push = Label(root, text='Press to Select Color')
    push.bind('<Button-1>', lambda event: selectedColor())
else: 
    # but Windows and Linux do
    push = Button(root, text='Press to Select Color', command=selectedColor)

push.config(height=5, width=30, font=('times', 20, 'bold'))
push.pack(expand=YES, fill=BOTH)

show = StringVar()
show.set('\'#RRGGBB\' hex string shown or input here')
entry = Entry(root, textvariable=show, justify=CENTER, font='bold')
entry.pack(fill=X)
entry.bind('<Return>', enteredColor)

root.mainloop()
