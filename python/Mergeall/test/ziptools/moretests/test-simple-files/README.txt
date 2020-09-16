Demo zipping individual files instead of folders, with and without 
Unix "*" filename expansion.  How tested:

/.../ziptools/moretests/test-simple-files$ py3 ../../zip-create.py all1.zip a.py b.py c.py d.py -skipcruft
Zipping ['a.py', 'b.py', 'c.py', 'd.py'] to all1.zip
Cruft patterns: {'skip': ['.*', '[dD]esktop.ini', 'Thumbs.db', '~*', '$*', '*.py[co]'], 'keep': ['.htaccess']}
Adding  file  a.py
Adding  file  b.py
Adding  file  c.py
Adding  file  d.py

/.../ziptools/moretests/test-simple-files$ py3 ../../zip-create.py all2.zip *.py -skipcruft
Zipping ['a.py', 'b.py', 'c.py', 'd.py'] to all2.zip
Cruft patterns: {'skip': ['.*', '[dD]esktop.ini', 'Thumbs.db', '~*', '$*', '*.py[co]'], 'keep': ['.htaccess']}
Adding  file  a.py
Adding  file  b.py
Adding  file  c.py
Adding  file  d.py

/.../ziptools/moretests/test-simple-files$ py3 ../../zip-extract.py all1.zip all1-extract 
Unzipping from all1.zip to all1-extract
Extracted a.py
		=> all1-extract/a.py
Extracted b.py
		=> all1-extract/b.py
Extracted c.py
		=> all1-extract/c.py
Extracted d.py
		=> all1-extract/d.py

/.../ziptools/moretests/test-simple-files$ py3 ../../zip-extract.py all2.zip all2-extract 
Unzipping from all2.zip to all2-extract
Extracted a.py
		=> all2-extract/a.py
Extracted b.py
		=> all2-extract/b.py
Extracted c.py
		=> all2-extract/c.py
Extracted d.py
		=> all2-extract/d.py

/.../ziptools/moretests/test-simple-files$ ls all1-extract/
a.py	b.py	c.py	d.py
/.../ziptools/moretests/test-simple-files$ ls all2-extract/
a.py	b.py	c.py	d.py
