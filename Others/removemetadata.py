# -*- coding: utf-8 -*-
import os
import sys
import codecs
from mutagen.mp3 import MP3

"""
python -m pip install mutagen

Removes metadata from MP3 files in the directory from which it was run.
Credits to ccpizza from activestate.com for making this in Python 2,
I simply converted it to work with Python 3.
"""

TEXT_ENCODING = 'utf8'

# get workdir from first arg or use current dir
if (len(sys.argv) > 1):
    fpath = sys.argv[1]
else:
    fpath = os.path.abspath(os.path.dirname(sys.argv[0]))

for fn in os.listdir(fpath):

    fname = os.path.join(fpath, fn)
    if fname.lower().endswith('.mp3'):
        print(fn)
        mp3 = MP3(fname)
        try:
            mp3.delete()
            mp3.save()
            print('ok!')
        except:
            print('no ID3 tag')
print('Done')
