'''
Created on Mar 16, 2014

@author: ignacio
'''
from common import check_playlist, get_playlist_contents, \
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
    print "Adding %s tracks to %s" % (len(tracks), playlist)
    for track in tracks:
        print "Adding: %s" % track
        size = len(get_playlist_contents(playlist))
        fname_bits = ["%06d" % (size + 1), track.artist, track.album, track.title]
        fname = "-".join(fname_bit.replace(" ", "_") for fname_bit in fname_bits)
        dest = os.path.join(get_playlist_dir(playlist), fname)
        os.link(track.path, dest)

def _parse_and_check(str_value, limit):
    int_value = int(str_value)
    if 0 <= int_value < limit:
        return int_value
    raise ValueError("%s is out of range (max:%s)" % (int_value, limit - 1))

def _parse_range(rang, limit):
    if "-" in rang:
        start, end = [_parse_and_check(x, limit) for x in rang.split("-", 1)]
        return range(start, end + 1)
    else:
        return [_parse_and_check(rang, limit)]


def _parse_indexes(selection, limit):
    if selection in ['a', 'A']:
        return range(limit)
    else:
        ranges = selection.split(",")
        res = []
        for rang in ranges:
            try:
                res += _parse_range(rang, limit)
            except Exception:
                logging.exception("Problems parsing '%s'", rang)
                return None
    return res

def _get_add_candidates(tracks):
    if len(tracks) == 1:
        return tracks
    for i, track in enumerate(tracks):
        print "%3s - %s" % (i, track)
    print "Query matched %d tracks" % len(tracks)
    print """Select which tracks to add.
Some valid examples: ['1','2-3','2,3,6-10,4']
a/A adds all tracks."""
    selection = raw_input("Which tracks should I add?: ")
    indexes = _parse_indexes(selection, len(tracks))
    return [tracks[i] for i in indexes]

def _confirm(msg):
    while True:
        resp = raw_input("%s (y/n): " % msg)
        if resp in ['y', 'Y']:
            return True
        elif resp in ['n', 'N']:
            return False
        print "Invalid response: '%s'. Try again..." % resp

def _confirm_add(candidates):
    print "Current selection is:"
    for candidate in candidates:
        print " - %s" % (candidate)
    return _confirm("Are you sure you want to add this?")

def _confirm_restart():
    return _confirm("Do you want to go back to the track selection?")

def _interactive_select(tracks):
    while True:
        candidates = _get_add_candidates(tracks)
        if _confirm_add(candidates):
            return candidates
        elif len(tracks) == 1:
            return []
        if not _confirm_restart():
            return []

def add(playlist, query):
    print "add(%s), query: '%s'" % (playlist, query)
    check_playlist(playlist)

    tracks = _run_beet_query(query)

    if len(tracks) == 0:
        logging.error("No tracks matched")
        sys.exit(1)
    else:
        tracks_to_add = _interactive_select(tracks)

    _add(playlist, tracks_to_add)
