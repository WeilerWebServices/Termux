#!/usr/bin/python3
"""
====================================================================================
A simple, customizable, and attachable scrolled listbox component, adopted from
the book _Programming Python, 4th Edition_.

# ANDROID version, Jan 2019 (see "# ANDROID" for changes)

Modified here to support: (1) separate label/action tables (and thus allow
duplicate labels); (2) single and double left-click modes; and (3) right-click
events and actions that use the selected or nearest item.  Left and right click
handlers also receive the click's tk event object for pixel position, if needed.

Inputs: labels is [strings], both actions are [one-argument-callables].  In the
listbox, left and right clicks run actions in leftactions and rightactions,
respectively, which correspond to clicked labels by position.  See comments
ahead for more on left-click and right-item modes.  The caller must sanitize
non-BMP Unicode characters in labels for Tk versions through 8.6 if required.
====================================================================================
"""

import sys
from tkinter import *

class ScrolledList(Frame):

    #----------------------------------------------------------------------
    # activate item's left-click callback via single or double left-click;
    # a single-click in left-double mode just highlights the item, which
    # may seem pointless, but might be used for right-click item choice;
    # note: a click in left-single mode still highlights the item (per tk
    # built-in code), which may matter only if the listbox is persistent;
    #----------------------------------------------------------------------
    
    leftclickmode = 'single'     # or 'double' (single requires right nearest)

    #---------------------------------------------------------------------- 
    # right-click item choice: selected item, or item nearest to click;
    # Selected assumes item selected by left-single and requires left-double
    # mode, but may use either nearest or selected in left-double mode;
    # right-clicks never highlight the item, per tk's standard behavior;
    #----------------------------------------------------------------------

    rightclickitem = 'nearest'   # or 'selected' (selected requires left double)


    def __init__(self, labels, leftactions, rightactions, parent=None, side=TOP):
        # sanity checks
        assert len(labels) == len(leftactions)
        assert len(labels) == len(rightactions)

        # these settings can be overridden in subclasses
        assert self.leftclickmode  in ('single',  'double')
        assert self.rightclickitem in ('nearest', 'selected')

        # invalid case: single + selected        
        if self.leftclickmode == 'single':
            assert self.rightclickitem == 'nearest'        # but double => nearest or selected
        if self.rightclickitem == 'selected':
            assert self.leftclickmode == 'double'          # but nearest => double or single

        # build the widget
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH, side=side)        # make me expandable
        self.makeWidgets(labels)                           # caller: self.config(bg=x, bd=y,...)
        self.leftactions  = leftactions                    # caller: self.listbox.config/itemconfig()
        self.rightactions = rightactions


    def handleListLeft(self, tkevent):
        """
        on list single- or double-left-click
        single mode: use item nearest to click
        double mode: use item selected (single left-click just selects an item)
        """
        if self.leftclickmode == 'single':                 # activate item nearest click:
            index = self.listbox.nearest(tkevent.y)        # index of nearest item (rel to widget)
        elif self.leftclickmode == 'double':               # activate item selected by single-left:
            index = self.listbox.curselection()            # get selected item index
            index = int(index[0])                          # index= (digitstring,) tuple, 0..N-1
        else:
            assert False, 'invalid leftclickmode setting'
        self.leftactions[index](tkevent)                   # call corresponding action with event

      
    def handleListRight(self, tkevent):
        """
        on list single-right-click
        use item nearest to click, or formerly selected by left-click
        """
        if self.rightclickitem == 'nearest':               # activate item nearest click:
            index = self.listbox.nearest(tkevent.y)        # index of nearest item (rel to widget)
        elif self.rightclickitem == 'selected':            # activate item selected by single-left:
            index = self.listbox.curselection()            # get selected item index
            index = int(index[0])                          # index= (digitstring,) tuple, 0..N-1
        else:
            assert False, 'invalid rightclickitem setting'
        self.rightactions[index](tkevent)                  # call corresponding action with event


    def makeWidgets(self, labels):
        """
        build the GUI: listbox, scroll, callbacks;
        always uses default single selection and resize modes,
        as in: list.config(selectmode=SINGLE, setgrid=1)
        """     
        # crosslink listbox, vertical scrollbar
        sbar = Scrollbar(self)
        lbox = Listbox(self, relief=SUNKEN)
        sbar.config(command=lbox.yview)                    # xlink sbar and list
        lbox.config(yscrollcommand=sbar.set)               # move one moves other
        sbar.pack(side=RIGHT, fill=Y)                      # pack first=clip last
        lbox.pack(side=LEFT, expand=YES, fill=BOTH)        # list clipped first

        # fill listbox with labels
        for (pos, label) in enumerate(labels):             # add to listbox
            lbox.insert(pos, label)                        # or insert(END,label)

        # set left/right click handlers
        if self.leftclickmode == 'single':                 # set left-click event handler
            lbox.bind('<Button-1>', self.handleListLeft)   # single-left activates item
        else:
            lbox.bind('<Double-1>', self.handleListLeft)   # single-left only selects item
        lbox.bind('<Button-3>', self.handleListRight)      # set right-click event handler

        # [2.0] on Mac OS X, also allow Control-click as an equivalent for right-click,
        # and support Mac mice that trigger Button-2 on right button click (on Macs,
        # right=Button-2 and middle=Button-3; it's the opposite on Windows and Linux!)
        
        # ANDROID - +True: enables rightclick = drive-by swipe (else can't copy hidden events)
        if True or sys.platform == 'darwin':
            lbox.bind('<Control-Button-1>', self.handleListRight)
            lbox.bind('<Button-2>', self.handleListRight)           

        self.listbox = lbox


if __name__ == '__main__':
    # run to test
    labels = ('spam', 'toast', 'spam', 'eggs')                 # duplicates: map by index
    lactions = [lambda e, i=i: print(i) for i in range(4)]     # print(0), print(1), ... (last i!)
    ractions = [lambda e, i=i: print(i) for i in range(4, 8)]  # print(4)...print(7)  
    ScrolledList(labels, lactions, ractions).mainloop()
