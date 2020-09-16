#!/bin/bash
#==========================================================================
# An example script for populating a new drive (edit me).
#
# Usage: /Admin-Mergeall/extreme256-1/START-MAY-9-to-11-17/HOW.sh [1|2|3]
#
# First: copy mac metadata from Gadgets/mac (automate me)
#
# To watch:
# ctrl-z 
# bg
# tail -f  ~/Desktop/EXT256-1--COPY.txt
#==========================================================================

python3 /MY-STUFF/Code/mergeall/cpall.py    /MY-STUFF /Volumes/EXT256-$1/MY-STUFF -skipcruft -vv >     ~/Desktop/EXT256-$1--COPY.txt
python3 /MY-STUFF/Code/mergeall/mergeall.py /MY-STUFF /Volumes/EXT256-$1/MY-STUFF -report -skipcruft > ~/Desktop/EXT256-$1--mergeall.txt
python3 /MY-STUFF/Code/mergeall/diffall.py  /MY-STUFF /Volumes/EXT256-$1/MY-STUFF -skipcruft >         ~/Desktop/EXT256-$1--diffall.txt

python3 /MY-STUFF/Code/mergeall/cpall.py    /my-OTHER-STUFF /Volumes/EXT256-$1/my-OTHER-STUFF -skipcruft -vv >     ~/Desktop/EXT256-$1--COPY-OTHER.txt
python3 /MY-STUFF/Code/mergeall/mergeall.py /my-OTHER-STUFF /Volumes/EXT256-$1/my-OTHER-STUFF -report -skipcruft > ~/Desktop/EXT256-$1--mergeall-OTHER.txt
python3 /MY-STUFF/Code/mergeall/diffall.py  /my-OTHER-STUFF /Volumes/EXT256-$1/my-OTHER-STUFF -skipcruft >         ~/Desktop/EXT256-$1--diffall-OTHER.txt
