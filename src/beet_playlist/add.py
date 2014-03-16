'''
Created on Mar 16, 2014

@author: ignacio
'''
from beet_playlist.common import check_playlist, get_playlist_contents, \
    get_playlist_dir
import logging
import os
import subprocess
import sys

def add(playlist, query):
    print "add(%s), query: '%s'" % (playlist, query)
    check_playlist(playlist)
    beet_format = '$artist\t$album\t$title\t$path'
    proc = subprocess.Popen(['beet', 'list', '-f', beet_format] + query, stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    proc.wait()
    if len(lines) == 0:
        logging.error("No tracks matched")
        sys.exit(1)
    elif len(lines) > 1:
        for line in lines:
            print line.rstrip("\n")
        logging.error("More than one track matched")
        sys.exit(1)

    artist, album, title, path = lines[0].rstrip("\n").split("\t")
    print "Matched: %s - %s - %s" % (artist, album, title)
    size = len(get_playlist_contents(playlist))
    fname_bits = ["%06d" % (size + 1), artist, album, title]
    fname = "-".join(fname_bit.replace(" ", "_") for fname_bit in fname_bits)
    dest = os.path.join(get_playlist_dir(playlist), fname)
    os.link(path, dest)
