#!/usr/local/bin/python
"""
################################################################################
PyCalc 4.0: a Python/tkinter calculator program and GUI component.

[SA] 4.0, Sep-2017: standalone release of PyCalc, PyClock, PyPhoto, PyToe.
Copyright: 1996-2019 M.Lutz, from book "Programming Python, 4th Edition".
License:   provided freely, but with no warranties of any kind.
Homepage:  http://learning-python.com/pygadgets.html.

#-------------------------------------------------------------------------------
# ANDROID VERSION, March-April 2019
# Per http://learning-python.com/using-tkinter-programs-on-android.html#PyGadgets.
# Replace original file with this custom version on your Android device (only).
# Search for "# ANDROID" for all changes, or date for these recent changes:
#
# [Apr1919] Open "hist" a bit wider for usability: small phones have room.
#
# [Apr1219] Reduce the initial size of the "hist" history display for better 
#           fit (though accommodating both phone orientations is impossible).
#           Do similar for "cmd" popups: shrink, use a smaller font to allow
#           more content, redo build code to clip Run button last if resized.
#           Also gets new "OK" button and size of helpmessage.py dialogs.
# 
# [Apr0419] Enable enter/return in keyboards too (but shifted operator keys fail
#           with no known workaround; tap/click GUI buttons for operator keys).
#           Also keep half of history on "clear" trims (not Android specific).
#
# [Apr0219] Enable backspace in on-screen keyboards too (but enter doesn't work).
#           Also fix traceback on rare empty+"eval" made more likely by new "back".
#
# [Mar3119] "back" backspace button, fix stuck-on buttons, history color/font.
#           All undated Android changes ahead were made in this release.
#-------------------------------------------------------------------------------

Evaluates expressions as they are entered per operator precedence, 
catching GUI button clicks and keyboard keys for expression entry. 

Versions:

4.0 (2017, standalone rlease [SA])
-automatic comma separators in main display
-enhanced help display
-Mac OS port
-new configs model: file or args, more options
-extra operators via new 'more' button frame
-x! factorial, -x, int(x), and 'e' extra ops
-x^y power operator with same precedence as * and /
-statistics module functions import

3.0+ (2010, PP4E, version number retained):
-port to run under Python 3.X (only)
-drop 'L' keypress (the long type is now dead in earnest)

3.0 changes (2005, PP3E):
-use 'readonly' entry state, not 'disabled', else field is greyed
 out (fix for 2.3 Tkinter change);
-avoid extended display precision for floats by using str(), instead
 of `x`/repr() (fix for Python change);
-apply font to input field to make it larger;
-use justify=right for input field so it displays on right, not left;
-add 'E+' and 'E-' buttons (and 'E' keypress) for float exponents;
 'E' keypress must generally be followed digits, not + or - optr key;
-remove 'L' button (but still allow 'L' keypress): superfluous now,
 because Python auto converts up if too big ('L' forced this in past);
-use smaller font size overall;
-auto scroll to the end in the history window

2.0 (1999, PP2E) evaluated expression parts as entered, added integrated 
command-line popups, a recent calculations history display popup, fonts
and colors configuration, help and about popups, preimported math/random
constants, and more;

1.0 (1996, PP1E) was a very simplistic calculator GUI that just built up 
Python expressions and passed them to eval() as a whole;

Misc. notes:
done 4.0: add a commas-insertion mode (see StringVarCommas);
done 4.0: allow '**' as an operator key (added as "^" key)
todo: allow '+' and 'J' inputs for complex Numbers
todo: use new decimal type for fixed precision floats; as is, can 
use 'cmd' popup windows to input and evaluate things like complex, but 
can't be input via main window; 
caveat: PyCalc's precision, accuracy, and some of its behaviour, is 
currently bound by result of the built-in str() call;
################################################################################
"""

import sys
from tkinter import *                                            # widgets, consts
from PP4E.Gui.Tools.guimixin import GuiMixin                     # quit method
from PP4E.Gui.Tools.widgets import label, entry, button, frame   # widget builders

debugme = True
def trace(*args):
    if debugme: print(args)

# [SA] port to Mac OS
RunningOnMac = 1#sys.platform.startswith('darwin')     # all Mac OS (X)

# [SA]: set window icons on Windows and Linux
from windowicons import trySetWindowIcon

# ANDROID - stuck-on buttons fix, etc.
RunningOnAndroid = True


################################################################################
# The main class - handles user interface.
# An extended Frame, on new Toplevel, or embedded in another container widget.
################################################################################

class CalcGui(GuiMixin, Frame):

    Operators = "+-*/^="                             # button lists, [SA] +^ 
    Operands  = ["abcd", "0123", "4567", "89()"]     # customizable here

    # [SA] additions, from book's subclasses
    Extras = [(' x! ',  'factorial(%s)'),
              ('-x ',   '-(%s)'),
              ('x^2',   '(%s)**2'),
              ('1/x',   '1.0/(%s)'),
              ('sqrt',  'sqrt(%s)'),
              ('int',   'int(%s)')]

    def __init__(self, parent=None, configs=object()):
        Frame.__init__(self, parent)                 # None=default Tk root
        self.pack(expand=YES, fill=BOTH)             # all parts expandable
        self.eval = Evaluator()                      # embed a stack handler
        self.text = StringVarCommas()                # extended linked variable
        self.text.set("0")
        self.erase = 1                               # clear "0" text next
        self.makeWidgets(configs)                    # build the GUI itself
        if not parent or not isinstance(parent, Frame):
            self.master.title('PyCalc 4.0')          # title iff owns window
            self.master.iconname("PyCalc")           # ditto for key bindings
            self.master.bind('<KeyPress>', self.onKeyboard)
            self.entry.config(state='readonly')      # 3.0: not 'disabled'=grey
        else:
            self.entry.config(state='normal')
            self.entry.focus()
        self.root = parent

    def makeWidgets(self, configs): 
        """
        build the GUI (N frames plus text-entry), register events:
        """
        font = configs.Font                          # font, color configurable
        bg, fg = configs.BgColor, configs.FgColor

        self.entry = entry(self, TOP, self.text)
        self.entry.config(font=font)                 # 3.0: make display larger
        self.entry.config(justify=RIGHT)             # 3.0: on right, not left
       #self.entry.pack(expand=NO, fill=X)           # [SA] grow vertically too

        for row in self.Operands:
            frm = frame(self, TOP)
            for char in row:
                if RunningOnMac or RunningOnAndroid:   # ANDROID - else bg botched temp
                    # [SA] emulate colored buttons
                    l = label(frm, LEFT, char,
                           fg=fg, bg=bg, font=font)
                    l.bind('<Button-1>', lambda e, op=char: self.onOperand(op))
                else:
                    button(frm, LEFT, char, lambda op=char: self.onOperand(op),
                           fg=fg, bg=bg, font=font)

        frm = frame(self, TOP)
        for char in self.Operators:
            if RunningOnMac or RunningOnAndroid:       # ANDROID - else bg botched temp
                # [SA] emulate colored buttons
                l = label(frm, LEFT, char,
                       fg=bg, bg=fg, font=font)
                l.bind('<Button-1>', lambda e, op=char: self.onOperator(op))

            else:
                button(frm, LEFT, char, lambda op=char: self.onOperator(op),
                       fg=bg, bg=fg, font=font)

        frm = frame(self, TOP)
        button(frm, LEFT, 'dot ', lambda: self.onOperand('.'))
        button(frm, LEFT, ' E+ ', lambda: self.text.set(self.text.get()+'E+'))
        button(frm, LEFT, ' E- ', lambda: self.text.set(self.text.get()+'E-'))
        button(frm, LEFT, 'cmd ', lambda: self.onMakeCmdline(configs))
        button(frm, LEFT, 'help', self.help)
        button(frm, LEFT, 'quit', self.quit)       # from guimixin

        frm = frame(self, BOTTOM)
        button(frm, LEFT, 'eval ', self.onEval)
        button(frm, LEFT, 'hist ', lambda: self.onHist(configs))
        button(frm, LEFT, 'more ', self.onMore)

        # ANDROID - add backspace button for touch, if no keyboard
        button(frm, LEFT, 'back ', lambda: self.onKeyboard(type('dummy', (), dict(char='\b'))))
                            # or=> lambda: self.event_generate('<BackSpace>'))
        button(frm, LEFT, 'clear', self.onClear)

        # [SA] make+hide additions
        morefrm = frame(self, TOP)
        for (lab, expr) in self.Extras:
            button(morefrm, LEFT, lab, (lambda expr=expr: self.onExtra(expr)))
        button(morefrm, LEFT, 'pi', lambda: self.onLiteral('pi'))
        button(morefrm, LEFT, 'e',  lambda: self.onLiteral('e'))
        morefrm.pack_forget()
        self.morefrm, self.moretgl = morefrm, 0

        # [SA] bind Delete for erase on Macs (\b isn't auto)
        #
        # ANDROID [Apr0219] - ditto, though you need an on-demand keyboard, 
        # and this isn't very useful because the enter/return key doesn't 
        # work (its <KeyPress> sends "" for all on-screen keyboards tested);
        # all keys work fine and as expected in "cmd" command-line popups;
        #
        # ANDROID [Apr0419] - fix return key by extra handler, but operator 
        # keys still don't work: in Pydroid 3 they don't set .char, .keysym
        # is unusable (see ahead), and this is not worth further work when  
        # "cmd" works fully and the GUI's buttons can be tapped or clicked;
        # binding to <plus> and <asterisk> here doesn't help (but why?-TBD);
        # note that tkinter fires <Return> xor <KeyPress> (preferring first);
        #
        if RunningOnMac or RunningOnAndroid:
            class Dummy1: char = '\b'
            self.master.bind('<BackSpace>', lambda e: self.onKeyboard(Dummy1))
        if RunningOnAndroid:
            class Dummy2: char = '\r'    # or use type() or instances
            self.master.bind('<Return>', lambda e:self.onKeyboard(Dummy2))       

    def onMore(self):
        """
        [SA] show/hide extra-row additions
        """
        self.moretgl += 1
        if self.moretgl % 2:
            self.morefrm.pack(expand=YES, fill=BOTH)
        else:
            self.morefrm.pack_forget()

    def onClear(self):
        """
        clear calculator state 
        """
        self.eval.clear()
        self.text.set('0')
        self.erase = 1

    def onEval(self):
        """
        run eval operation: eval all still-open exprs
        """
        self.eval.shiftOpnd(self.text.get())     # last or only opnd
        self.eval.closeall()                     # apply all optrs left
        self.text.set(self.eval.popOpnd())       # need to pop: optr next?
        self.erase = 1

    def onOperand(self, char):
        """
        handle an operand button or keypress
        """
        if char == '(':
            self.eval.open()
            self.text.set('(')                      # clear text next
            self.erase = 1
        elif char == ')':
            self.eval.shiftOpnd(self.text.get())    # last or only nested opnd
            self.eval.close()                       # pop here too: optr next?
            self.text.set(self.eval.popOpnd())
            self.erase = 1
        else:
            if self.erase:
                self.text.set(char)                     # clears last value
            else:
                self.text.set(self.text.get() + char)   # else append to opnd
            self.erase = 0
        self.update()

    def onOperator(self, char):
        """
        handle an operator button or keypress
        """
        self.eval.shiftOpnd(self.text.get())    # push opnd on left
        self.eval.shiftOptr(char)               # eval exprs to left?
        self.text.set(self.eval.topOpnd())      # push optr, show opnd|result
        self.erase = 1   
        self.update()                       # erased on next opnd|'('

    def onExtra(self, expr):
        """
        [SA] addition: run extra-row expr with value substitution
        """
        try:
            self.text.set(self.eval.runstring(expr % self.text.get()))
        except:
            self.text.set('ERROR')

    def onLiteral(self, literal):
        """
        [SA] addition: run extra-row literal expr
        """
        self.text.set(self.eval.runstring(literal))  # e.g., 'pi', 'e'

    def onMakeCmdline(self, configs):
        """
        new non-modal top-level window for arbitrary Python code
        """
        new = Toplevel()                            # new top-level window
        new.title('PyCalc Command Line')
        trySetWindowIcon(new, 'icons', 'pygadgets') # [SA] for win+lin

        frm = frame(new, TOP)                       # only the Entry expands
        label(frm, LEFT, '>>>').pack(expand=NO)

        # ANDROID [Apr1219]: make+pack button first so clipped last if resized
        onButton = (lambda: self.onCmdline(var, ent))
        onReturn = (lambda event: self.onCmdline(var, ent))
        button(frm, RIGHT, 'Run', onButton).pack(expand=NO)

        # ANDROID [Apr1219]: use smaller font to shrink and allow more content on phones
        cmdfont = 'courier 8 normal'                # was configs.Font (= main buttons)
        var = StringVar()                           # [SA] no commas here
        ent = entry(frm, LEFT, var, width=30)       # ANDROID [Apr1219] smaller, was 40
        ent.config(font=cmdfont)                    # [SA] now configurable
        ent.bind('<Return>', onReturn)
        var.set(self.text.get())
        ent.focus()   # [SA] on this entry and window

    def onCmdline(self, var, ent): 
        """
        evaluate cmdline pop-up input
        """
        try:
            value = self.eval.runstring(var.get())
            var.set('OKAY')
            if value != None:                 # run in eval namespace dict
                self.text.set(value)          # expression or statement
                self.erase = 1
                var.set('OKAY => '+ value)
        except:                               # result in calc field
            var.set('ERROR')                  # status in pop-up field
        ent.icursor(END)                      # insert point after text
        ent.select_range(0, END)              # select msg so next key deletes

    def onKeyboard(self, event):
        """
        on keyboard press event, pretend button was pressed,
        or handle extras - backspace (not delete), ?=help;
        """
        #        
        # ANDROID [Apr0219-Apr0419] - in Pydroid 3's tkinter:
        # -on backspace, event .char='' and .keysym='BackSpace'
        # -on return,    event .char='' and .keysym='Return'
        # this differs from expected behavior; addressed with 
        # '<Return>' and '<BackSpace>' handler binds elsewhere;
        #
        # ANDROID [Apr0419] _shifted_ operator keys (e.g. '+')
        # .char is '' too, but .keysym is not usable - tkinter
        # sends two separate events: Shift_L/R + the *unshifted*
        # key (though using "cmd" popups seems to oddly fix this);
        # punt: this seems a tkinter bug - use "cmd" or buttons;
        #
        tracekb = False  #True
        if RunningOnAndroid and tracekb: 
            print('char=%r, keysym=%r' % 
              tuple(getattr(event, attr, 'none') for attr in ('char', 'keysym')))
       
        pressed = event.char 
        if pressed != '':
            if pressed in self.Operators:
                self.onOperator(pressed)
            else:
                for row in self.Operands:
                    if pressed in row:
                        self.onOperand(pressed)
                        break
                else:                                          # 4E: drop 'Ll'
                    if pressed == '.':
                        self.onOperand(pressed)                # can start opnd
                    if pressed in 'Ee':  # 2e10, no +/-
                        self.text.set(self.text.get()+pressed) # can't: no erase
                    elif pressed == '\r':
                        self.onEval()                          # enter key=eval
                    elif pressed == ' ':
                        self.onClear()                         # spacebar=clear
                    elif pressed == '\b':
                        self.text.set(self.text.get()[:-1])    # backspace or "back"
                    elif pressed == '?':                       # [SA] +Mac delete
                        self.help()

    def onHist(self, configs):
        """
        show recent calcs log popup
        """
        from tkinter.scrolledtext import ScrolledText     # or PP4E.Gui.Tour

        new = Toplevel()                                  # make new window
        new.title('PyCalc History')
        trySetWindowIcon(new, 'icons', 'pygadgets')       # [SA] for win+lin

        # new window goes away on ok press or enter key
        ok = Button(new, text=' OK ', command=new.destroy)
        ok.pack(pady=1, side=BOTTOM)                      # pack first=clip last
        new.bind("<Return>", (lambda event: new.destroy()))

        text = ScrolledText(new, bg='beige')              # add Text + scrollbar
        bg, font = configs.HistBgColor, configs.HistFont  # [SA] now configurable
        text.config(bg=bg, font=font)
        text.insert('0.0', self.eval.getHist())           # get Evaluator text
        text.see(END)                                     # 3.0: scroll to end
        text.pack(expand=YES, fill=BOTH)

        # ANDROID [Apr1219] - start smaller for fit on phones, user can resize;
        # hist font preset in __main__ is larger than help font in helpmessage.py,
        # and smaller than "cmd" popup font above, but all are tailored for fit;
        # ANDROID [Apr1919] - open "hist" 45 wide, not 40, for ease (there's room);
        #
        text.config(width=45, height=20)    # chars, lines (more or less: see Tk)

        # go modal until window destroyed
        ok.focus_set()                      # make new window modal:
        new.grab_set()                      # get keyboard focus, grab app
        new.wait_window()                   # don't return till new.destroy

    def help(self):
        """
        [SA] fully redesigned, and helpmessage replaces self.infobox();
        called for 'help' button click, '?' keyboard press, Mac menus;
        """
        from helpmessage import showhelp
        showhelp(self.root, 'PyCalc', self.HelpText, forcetext=False,
                 setwinicon=lambda win:
                        trySetWindowIcon(win, 'icons', 'pygadgets'))
        #if self.root: self.root.focus_force()   # now done in helpmessage

    HelpText = ('PyCalc 4.0\n'
                '\n'
                'A Python/tkinter calculator GUI.\n'
                'For Mac OS, Windows, Linux, and Android.\n'
                'From the book Programming Python.\n'
                'Author and © M. Lutz 1996-2019.\n'
                '\n'
                'Use button clicks or keyboard presses to '
                'input numbers and operators, or type '
                'Python expression code in a "cmd" popup.\n'
                '\n'
                'Keyboard usage: spacebar="clear", enter="eval", '
                '.="dot", ?="help", backspace or delete=erase 1 character.  '
                'Comma separators are inserted automatically for '
                'display as numbers are entered and shown.\n'
                '\n'
                'Tips:\n'
                '▶ "=" assigns variables '
                '(e.g., ab=99, ab+1)\n'
                '▶ "eval" evaluates pending expressions\n'
                '▶ "more" shows/hides extra keys\n'
                # ANDROID
                '▶ "back" is backspace for main display\n'
                '▶ "hist" displays recent calculations\n'
                '▶ "^" is x^y power (Python\'s "**")\n'
                '▶ "int" and "* 1." convert to int and float\n'
                '\n'
                'The "cmd" dialog supports entry of additional '
                'ops, including all functions in Python\'s math, '
                'random, statistics, and builtins modules.  E.g., '
                'sin(x), log(x, b), random(), mean([]), max(x, y), set().\n'
                '\n'
                # ANDROID
                'Android users: the "back" key is backspace '
                'for touch.  Keyboards are limited: use the '
                '"cmd" command-line popup for general entry.\n'
                '\n'
                'Version history (see source for changes):\n'
                '● 4.0: Jan 2019, Android release\n'
                '● 4.0: Sep 2017, standalone release\n'
                '● 3.1: May 2010, Programming Python 4E\n'
                '● 3.0 2005 3E, 2.0 1999 2E, 1.0 1996 1E\n'
                '\n'
                'For downloads and more apps, visit:\n'
                'http://learning-python.com/programs.html'
               )


################################################################################
# The expression evaluator class.
# Embedded in and used by a CalcGui instance, to perform calculations.
################################################################################

class Evaluator:
    def __init__(self):
        self.names = {}                              # a names-space for my vars
        self.opnd, self.optr = [], []                # two empty stacks
        self.hist = []                               # my prev calcs history log

        # preimport math modules into calc's namespace for "cmd"
        # namespaces are disjoint: set(dir(math)) & set(dir(other))
        
        self.runstring("from math import *")         # sin(x), log(x, b), pi, e
        self.runstring("from random import *")       # plus builtins: max(), abs()
        try:
            # [SA] new in py 3.4, ignore if absent
            self.runstring("from statistics import *")   # mean(), median(), etc
        except:
            print('Note: PyCalc cannot load statistics module in your Python;')
            print('upgrade to Python 3.4 or later to use its tools in PyCalc.')

    def clear(self):
        self.opnd, self.optr = [], []           # leave names intact
        if len(self.hist) > 128:                # don't let hist get too big
            # 
            # ANDROID [Apr0419] - keep latest half of history (all platforms)
            # self.hist = ['clear']
            #
            self.hist = self.hist[-64:] + ['--clear and trim--']
        else:
            self.hist.append('--clear--')

    def popOpnd(self):
        value = self.opnd[-1]                   # pop/return top|last opnd
        self.opnd[-1:] = []                     # to display and shift next
        return value                            # or x.pop(), or del x[-1]

    def topOpnd(self):
        return self.opnd[-1]                    # top operand (end of list)

    def open(self):
        self.optr.append('(')                   # treat '(' like an operator

    def close(self):                            # on ')' pop downto highest '('
        self.shiftOptr(')')                     # ok if empty: stays empty
        self.optr[-2:] = []                     # pop, or added again by optr

    def closeall(self):
        while self.optr:                        # force rest on 'eval'
            self.reduce()                       # last may be a var name
        try:
            self.opnd[0] = self.runstring(self.opnd[0])
            #
            # ANDROID [Apr0219] - fix a rare special case: an immediate backspace 
            # or new "back" button followed by "eval" can cause an empty string to 
            # succeed as a statement and return+push None, which breaks commify();
            # other "back" empty-string cases all fail normally as "*ERROR*" opnds;
            # this can occur in pre-Android PyCalc too but is likelier with "back";
            #
            assert self.opnd[0] != None
        except:
            self.opnd[0] = '*ERROR*'            # pop else added again next:

    afterMe = {'^': ['+', '-', '(', '='],       # [SA] add power operator
               '*': ['+', '-', '(', '='],       # class member
               '/': ['+', '-', '(', '='],       # optrs to not pop for key
               '+': ['(', '='],                 # if prior optr is this: push
               '-': ['(', '='],                 # else: pop/eval prior optr
               ')': ['(', '='],                 # all left-associative as is
               '=': ['('] }

    def shiftOpnd(self, newopnd):               # push opnd at optr, ')', eval
        self.opnd.append(newopnd)

    def shiftOptr(self, newoptr):               # apply ops with <= priority
        while (self.optr and
               self.optr[-1] not in self.afterMe[newoptr]):
            self.reduce()
        self.optr.append(newoptr)               # push this op above result
                                                # optrs assume next opnd erases
    def reduce(self):
        trace(self.optr, self.opnd)
        try:                                    # collapse the top expr
            operator       = self.optr[-1]      # pop top optr (at end)
            [left, right]  = self.opnd[-2:]     # pop top 2 opnds (at end)
            self.optr[-1:] = []                 # delete slice in-place
            self.opnd[-2:] = []
            result = self.runstring(left + operator + right)
            if result == None:
                result = left                   # assignment? key var name
            self.opnd.append(result)            # push result string back
        except:
            self.opnd.append('*ERROR*')         # stack/number/name error

    def runstring(self, rawcode):
        code = rawcode.replace('^', '**')                     # [SA] xlate power
        try:                                                  # 3.0: not `x`/repr
            result = str(eval(code, self.names, self.names))  # try expr: string
            self.hist.append(rawcode + ' => ' + result)       # add to hist log
        except:
            exec(code, self.names, self.names)                # try stmt: None
            self.hist.append(rawcode)
            result = None
        return result

    def getHist(self):
        return '\n'.join(self.hist)


################################################################################
# [SA] StringVar wrapper class.
# Used to manage thousands-separator commas display with minimal changes.
################################################################################

class StringVarCommas(StringVar):
    """
    in the main number-display area (only: not cmd): auto insert commas as 
    numbers are entered, and remove them when fetched for the evaluator;
    this also removes commas on backspace erases by a get+set combination;
    literal comma presses are simply ignored (TBD: use them as a toggle?);

    some lex errors are caught here (e.g., '1E2.'), but others pass here 
    and fail later in the evaluator (e.g., '1..2', '..1', '1EE2', '.'), 
    due in part to split(x, 1): removing the 1 would make more fail here;
    """

    # extend StringVar interface

    def get(self):
        text = StringVar.get(self)         # get display text 
        return self.decommify(text)        # strip commas

    def set(self, text):
        text = self.commify(text)          # add commas
        StringVar.set(self, text)          # set display text


    # add text processing methods

    def decommify(self, text):
        return text.replace(',', '')

    def commify(self, text):
        text = self.decommify(text)
       #text = '{:,}'.format(num)          # requires an eval()

        # strip sign if added by -X key
        if text.startswith('-'):
            sign, text = '-' , text[1:]
        else:
            sign = ''

        # add commas to whole-number part
        try:
            if text.isdigit():                                  # all digits: 'xxx'
                return sign + '{:,}'.format(int(text))          # add ',' and sign 

            elif '.' in text:                                   # also for '.' or '..'
                whole, rest = text.split('.', 1)                # 'x.y' 'x.' '.y' 'x.yEz'
                if whole:                                       # nov17: '.any' => '.any'
                    whole = '{:,}'.format(int(whole))           # (whole or '0') adds '0'
                return sign + whole + '.' + rest                # covers '0.1e2', '.1e-2'

            elif 'E' in text.upper() and 'ERROR' not in text:
                whole, exp = text.upper().split('E', 1)         #  no '.' but whole base
                whole = '{:,}'.format(int(whole))               # 'xe+z', 'xe-z', 'xez'
                return sign + whole + 'E' + exp

            else:
                return text                                     # other: allow 'abcd'

        except:
            return 'ERROR'   # anything not recognized: avoid uncaught exception in GUI


################################################################################
# Main logic - when run standalone.
# Get optional configs via command-line args, make and start a CalcGui object.
#
# ANDROID - the config file is launcher-only, and Pydroid 3 doesn't do cmd-line 
# arguments, so configuration options are currently limited to defaults below.
################################################################################

if __name__ == '__main__':
    from getConfigs import getConfigs      # [SA] new common gadgets utility

    defaults = dict(InitialSize=None,      # None=let tkinter decide
                    BgColor='wheat',       # main-display options
                    FgColor='black', 
                    Font=('courier', 14, 'bold'),  # or 'family...' str arg
                    
                    # ANDROID - bg was beige, but clashes with main window default
                    # ANDROID - font was None, but default 5-pt font is very small
                    #
                    HistBgColor='ivory',
                    HistFont='courier 6 normal')

    configs = getConfigs('PyCalc', defaults)       # load from file or args

    root = Tk()                                    # non-default top-level window
    if configs.InitialSize:
        root.geometry(configs.InitialSize)         # 'Wxh' size string
    trySetWindowIcon(root, 'icons', 'pygadgets')   # [SA] for win+lin
    calc = CalcGui(root, configs)                  # build gui on root

    if RunningOnMac:
        # Mac requires menus, deiconifies, focus

        # [SA] on Mac, customize app-wide automatic top-of-display menu
        from guimaker_pp4e import fixAppleMenuBar
        fixAppleMenuBar(window=root,
                        appname='PyCalc',
                        helpaction=calc.help,      # bound method (has self)
                        aboutaction=None,
                        quitaction=calc.quit)      # app-wide quit: ask

        # [SA] reopen auto on dock/app click and fix tk focus loss on deiconify
        def onReopen():
            root.lift()
            root.update()
            temp = Toplevel()
            temp.lower()
            temp.destroy()
        root.createcommand('::tk::mac::ReopenApplication', onReopen)

    root.mainloop()
