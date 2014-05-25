'''
Created on Mar 16, 2014

@author: ignacio
'''
import logging
import os
import subprocess


DATA_DIR = os.path.join(os.path.expanduser("~"), ".beet-playlist")
DATA_FILE = os.path.join(DATA_DIR, ".playlists_data")
PLAYLISTS_DIR = os.path.join(DATA_DIR, ".playlists")


class Playlist(object):

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

    def play(self, shuffle=False):
        paths = [os.path.join(self.path, c) for c in self.contents()]
        if paths:
            mplayer(paths, shuffle=shuffle)
        else:
            logging.warn("Playlist {} is empty. Not playing".format(self.name))

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
        return [cls(playlist)
                for playlist in sorted(os.listdir(PLAYLISTS_DIR))]


def list_playlists(playlist):
    if playlist is None:
        for playlist in Playlist.list():
            print "%s - %d tracks" % (playlist.name, len(playlist.contents()))
    else:
        contents = playlist.contents()
        print "Playlist '%s' - %d tracks" % (playlist.name, len(contents))
        for track in contents:
            print " - %s" % track


def _get_playlist_subparser(subparsers, name, **kwargs):
    parser = subparsers.add_parser(name)
    parser.add_argument("playlist", action='store', type=Playlist,
                        default=None, **kwargs)
    return parser


def add_parsers(subparsers):
    _add_new_parser(subparsers)
    _add_list_parser(subparsers)
    _add_play_parser(subparsers)
    _add_rm_parser(subparsers)


def _add_new_parser(subparsers):
    parser = subparsers.add_parser("new")
    parser.add_argument("playlist", action='store',
                        help='Crate a new playlist')
    parser.set_defaults(func=Playlist.create)


def _add_list_parser(subparsers):
    parser = _get_playlist_subparser(subparsers, "list", nargs='?',
                                     help='List this playlist contents')
    parser.set_defaults(func=list_playlists)


def _add_play_parser(subparsers):
    parser = _get_playlist_subparser(subparsers, "play",
                                     help='PLaylist to play')
    parser.add_argument("--shuffle", action='store_true', default=False,
                        help='Shuffle the playlist')
    parser.set_defaults(func=_play)


def _add_rm_parser(subparsers):
    parser = _get_playlist_subparser(subparsers, "rm",
                                     help='Playlist to remove')
    parser.set_defaults(func=_rm_playlist)


def _play(playlist, shuffle):
    playlist.play(shuffle=shuffle)


def _rm_playlist(playlist):
    logging.info("Removing playlist '%s'", playlist.name)
    os.removedirs(playlist.path)
    logging.info("Removed")


def mplayer(paths, shuffle=False):
    if not paths:
        raise ValueError("No paths supplied to mplayer")
    command = ['mplayer']
    if shuffle:
        command.append("--shuffle")
    command.extend(paths)
    subprocess.call(command)
