"""
=================================================================
Test font support (and lack thereof) in Pydroid 3's tkinter.
Families courier, helvetica, and times (and their synonyms)
work, others trigger a hard/silent crash, and italic and bold
styles are ignored for courier in both tuples and strings.
Change settings below and run in the Pydroid 3 app to test.

Update: Pydroid 3's 30 release fixed the font crash by simply
forcing any unknown font family to be helvetica.  All other 
limitations of its font support remain as described above.  
=================================================================
"""
 
from tkinter import *
root = Tk()

text = Text(root, height=2)
text.pack()
text.config(font=('helvetica', 12, 'italic bold'))    # +times, courier
text.insert('0.1', 'qwerty-1')                        # arial==helvetica
                                                      # courier: no italic/bold
text = Text(root, height=2)
text.pack()
text.config(font='courier 12 italic bold')            # change me to test
text.insert('0.1', 'qwerty-2')

root.mainloop()
