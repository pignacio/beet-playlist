'''
Created on Mar 16, 2014

@author: ignacio
'''
import logging
import os
import subprocess

PLAYLISTS_DIR = "/home/ignacio/Music/.playlists"
PLAYLISTS_DATA_FILE = ".playlists_data"


class Playlist():
    def __init__(self, playlist):
        if playlist is None:
            raise ValueError("Must supply a playlist")
        if not self.exists(playlist):
            raise ValueError("'{}' is not a valid playlist".format(playlist))
        self._path = self._get_playlist_dir(playlist)
        self._name = playlist

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def contents(self):
        return sorted(os.listdir(self._path))

    def play(self):
        contents = [os.path.join(self.path, c) for c in self.contents()]
        subprocess.call(["mplayer"] + contents)

    @classmethod
    def _get_playlist_dir(cls, playlist):
        return os.path.join(PLAYLISTS_DIR, playlist)

    @classmethod
    def exists(cls, playlist):
        return os.path.isdir(cls._get_playlist_dir(playlist))

    @classmethod
    def create(cls, playlist):
        logging.info("Creating new playlist '%s'", playlist)
        if playlist is None:
            raise ValueError("Must supply a playlist")
        elif cls.exists(playlist):
            raise ValueError("Playlist '{}' already exsts".format(playlist))
        else:
            os.makedirs(cls._get_playlist_dir(playlist))
            logging.info("Created playlist '%s'", playlist)

    @classmethod
    def list(cls):
        return [cls(playlist) for playlist in sorted(os.listdir(PLAYLISTS_DIR)) if playlist != PLAYLISTS_DATA_FILE]

def list_playlists(playlist):
    if playlist is None:
        for playlist in Playlist.list():
            print "%s - %d tracks" % (playlist.name, len(playlist.contents()))
    else:
        contents = playlist.contents()
        print "Playlist '%s' - %d tracks" % (playlist.name, len(contents))
        for track in contents:
            print " - %s" % track

def add_parsers(subparsers):
    add_new_parser(subparsers)
    add_list_parser(subparsers)
    add_play_parser(subparsers)

def add_new_parser(subparsers):
    parser = subparsers.add_parser("new")
    parser.add_argument("playlist", action='store',
                        help='Crate a new playlist')
    parser.set_defaults(func=Playlist.create)

def add_list_parser(subparsers):
    parser = subparsers.add_parser("list")
    parser.add_argument("playlist", action='store', type=Playlist, default=None,
                        nargs='?', help='List all or given playlist')
    parser.set_defaults(func=list_playlists)

def add_play_parser(subparsers):
    parser = subparsers.add_parser("play")
    parser.add_argument("playlist", action='store', type=Playlist, default=None,
                        help='Play given playtlist')
    parser.set_defaults(func=lambda playlist: Playlist.play(playlist))

