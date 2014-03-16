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

class BeetTrack():
    def __init__(self, artist, album, title, path):
        self.artist = artist
        self.album = album
        self.title = title
        self.path = path

    def __str__(self):
        return " - ".join([self.artist, self.album, self.title])


def _run_beet_query(query):
    beet_format = '$artist\t$album\t$title\t$path'
    proc = subprocess.Popen(['beet', 'list', '-f', beet_format] + query, stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    proc.wait()
    return [BeetTrack(*line.rstrip('\n').split("\t")) for line in lines]

def _add(playlist, tracks):
    for track in tracks:
        print "Adding: %s" % track
        size = len(get_playlist_contents(playlist))
        fname_bits = ["%06d" % (size + 1), track.artist, track.album, track.title]
        fname = "-".join(fname_bit.replace(" ", "_") for fname_bit in fname_bits)
        dest = os.path.join(get_playlist_dir(playlist), fname)
        os.link(track.path, dest)

def add(playlist, query):
    print "add(%s), query: '%s'" % (playlist, query)
    check_playlist(playlist)

    tracks = _run_beet_query(query)

    if len(tracks) == 0:
        logging.error("No tracks matched")
        sys.exit(1)
    elif len(tracks) > 1:
        for track in tracks:
            print track
        logging.error("More than one track matched")
        sys.exit(1)
    else:
        tracks_to_add = tracks

    _add(playlist, tracks_to_add)
