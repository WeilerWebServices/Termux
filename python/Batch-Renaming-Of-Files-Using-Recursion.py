#!python

# Batch Renaming Of Files Using Recursion

import os

def renameFiles(path, basefilename, depth=99):
    # Once we hit depth, just return (base case)
    if depth < 0: return

    # Make sure that a path was supplied and it is not a symbolic link
    if os.path.isdir(path) and not os.path.islink(path):
        ind = 1

        # Loop through each file in the start directory and create a fullpath
        for file in os.listdir(path):
            fullpath = path + os.path.sep + file

            # Again we don't want to follow symbolic links
            if not os.path.islink(fullpath):

                # If it is a directory, recursively call this function 
                # giving that path and reducing the depth.
                if os.path.isdir(fullpath):
                    renameFiles(fullpath, basefilename, depth - 1)
                else:
                    # Find the extension (if available) and rebuild file name 
                    # using the directory, new base filename, index and the old extension.
                    extension = os.path.splitext(fullpath)[1]
                    os.rename(fullpath, os.path.dirname(fullpath) + os.path.sep + basefilename + "_" + str(ind) + extension)
                    ind += 1
    return
