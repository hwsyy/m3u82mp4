#!/usr/bin/python
import shutil
import os
import sys
import glob
from distutils.spawn import find_executable


if find_executable('ffmpeg') is None:
    print 'This script requires ffmpeg to encode your m3u8 to mp4. Please go away, install ffmpeg and try again.'
    sys.exit()

try:
    m3u8path = sys.argv[1]
except IndexError:
    print 'Please provide the path to your m3u8 files.'
    sys.exit()

try:
    outputfile = sys.argv[2]
except IndexError:
    print 'Please provide the path to your output file.'
    sys.exit()

try:
    os.chdir(m3u8path)
    playlists = glob.glob('*.m3u8')
    if len(playlists) > 1:
        print 'More than one .m3u8 playlist file in this directory.'
        sys.exit()
except OSError:
    print 'The given m3u8 path doesn\'t exist.'
    sys.exit()

playlist = playlists[0]
f = open(playlist, 'r')

f.seek(0)
fdata = f.readlines()

with open(outputfile, 'wb') as outfile:
    for filename in fdata:
        fn = filename.rstrip()
        if fn[-3:] == '.ts':
            #print filename
            try:
                filepath = os.path.join(os.getcwd(), fn)
                with open(filepath, 'rb') as readfile:
                    shutil.copyfileobj(readfile, outfile)
            except IOError:
                pass

# ffmpeg -i movie.ts -c:v libx264 -c:a aac The_Mandalorian_S01E01.mp4
