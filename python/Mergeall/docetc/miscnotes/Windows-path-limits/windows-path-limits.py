#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
Isolate and verify the actual path-length limits on Windows.
See the corresponding output text file here for results.

Note that all paths here use _characters_, not bytes, strongly
sugggesting that length limits are not subject to any expansions
required for Unicode encodings.

Also note that relative path limits are _less_ than those of abs
paths, but correspond exactly to the lenth of their abs paths
forms (i.e., the lengths of the rel path + the CWD prefix).  To
check lengths against the limits, code must use absolute paths.
--------------------------------------------------------------------------------
"""

import os, shutil
PREFIX = '\\\\?\\'


def TEST(root, rel=False):

    def prefix(path):
        if not rel:
            return PREFIX + path
        else:
            return PREFIX + os.path.abspath(path)
        
    #------------------------------------------------------------------------------
    # DIRS
    #------------------------------------------------------------------------------

    print()
    print('MAKE DIRS')
    path = root
    while True:
        try:
            path += 'x'            # up to 255 for component > 247 dirpath limit
            os.mkdir(path)
        except:
            print(' os.mkdir failed at len=%d chars' % len(path))
            print('\tadding len=', end='')
            for i in range(15):
                print('%d ' % len(path), end='')
                os.mkdir(prefix(path))            # add longer paths for more 
                path += 'x'
            print()
            break

    print('ACCESS DIRS')
    for func in(os.path.isdir, os.listdir, os.lstat):
        path = root
        while True:
            try:
                path += 'x'
                res = func(path)
                if res == False and func is os.path.isdir:    # False on fail
                    raise OSError
            except:
                print(' %s failed at len=%d chars' %
                      (getattr(func, '__name__', func), len(path)))
                break

    print('ACCESS DIRS WITH PREFIX')
    for func in(os.path.isdir, os.listdir, os.lstat):
        path = root
        while True:
            try:
                path += 'x'
                res = func(prefix(path))
                if res == False and func is os.path.isdir:
                    raise OSError
            except:
                print(' %s failed at len=%d chars' %
                      (getattr(func, '__name__', func), len(path)))
                break

    #------------------------------------------------------------------------------
    # FILES
    #------------------------------------------------------------------------------

    print()
    print('MAKE FILES')
    path = root
    while True:
        try:
            path += 'f' 
            f = open(path, 'w')
            f.write('spam')
            f.close()
        except:
            print(' open failed at len=%d chars' % len(path))
            print('\tadding len=', end='')
            for i in range(15):
                print('%d ' % len(path), end='')
                f = open(prefix(path), 'w')
                f.write('spam')
                f.close()  
                path += 'f'
            print()
            break

    print('ACCESS FILES')
    for func in(open, os.path.isfile, os.lstat):
        path = root
        while True:
            try:
                path += 'f'
                res = func(path)
                if res == False and func is os.path.isfile:    # False on fail
                    raise OSError
            except:
                print(' %s failed at len=%d chars' %
                      (getattr(func, '__name__', func), len(path)))
                break

    print('ACCESS FILES WITH PREFIX')
    for func in(open, os.path.isfile, os.lstat):
        path = root
        while True:
            try:
                path += 'f'
                res = func(prefix(path))
                if res == False and func is os.path.isfile:    # False on fail
                    raise OSError
            except:
                print(' %s failed at len=%d chars' %
                      (getattr(func, '__name__', func), len(path)))
                break


#------------------------------------------------------------------------------
# TEST ABSOLUTE PATHS (NOT REL)
#------------------------------------------------------------------------------

print()
print('ABSOLUTE PATHS', '*'*60)
root = 'C:\\Users\\mark\\Desktop\\dirlentest\\'   # 33 chars here
if os.path.exists(root):
    shutil.rmtree('\\\\?\\' + root)               # clean up prior run's dirs
os.mkdir(root)
print('root prefix len=%d' % len(root))
TEST(root, rel=False)


#------------------------------------------------------------------------------
# REDO ALL WITH RELATIVE PATH (NOT ABS)
#------------------------------------------------------------------------------

print()
print('RELATIVE PATHS', '*'*60)
runin = 'C:\\Users\\mark\\Desktop'
os.chdir(runin)
root = 'dirlentest\\'
if os.path.exists(root):
    shutil.rmtree('\\\\?\\' + os.path.abspath(root))    # clean up prior run
os.mkdir(root)
print('cwd len=%d (%d with \\)' % (len(runin), len(runin)+1))
print('root prefix len=%d' % len(root))
TEST(root, rel=True)



