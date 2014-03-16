'''
Created on Mar 16, 2014

@author: ignacio
'''
import sys
import logging
import os

PLAYLISTS_DIR = "/home/ignacio/Music/.playlists"
PLAYLISTS_DATA_FILE = ".playlists_data"

def get_playlist_dir(playlist):
    return os.path.join(PLAYLISTS_DIR, playlist)

def get_playlist_contents(playlist):
    return sorted(os.listdir(get_playlist_dir(playlist)))

def is_playlist(playlist):
    return os.path.isdir(os.path.join(PLAYLISTS_DIR, playlist))

def check_playlist(playlist):
    if playlist is None:
        logging.error("Must supply a playlist name")
        sys.exit(1)
    elif not is_playlist(playlist):
        logging.error("Invalid playlist '%s'", playlist)
        sys.exit(1)
