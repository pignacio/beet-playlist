from argparse import ArgumentParser
import logging
import os
import sys
import subprocess

PLAYLISTS_DIR = "/home/ignacio/Music/.playlists"
PLAYLISTS_DATA_FILE = ".playlists_data"

def _get_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("-n" , "--new",
                        action='store_true', default=False,
                        help='Adds a new playlist')
    parser.add_argument("-l" , "--list",
                        action='store_true', default=False,
                        help='Lists current playlists')
    parser.add_argument("-a" , "--add",
                        action='store_true', default=False,
                        help='Adds track to a playlist')
    parser.add_argument("-p" , "--play",
                        action='store_true', default=False,
                        help='Plays a playlist')
    parser.add_argument('playlist', nargs="?", default=None,
                        help='playlist to act on')
    parser.add_argument('query', nargs="*",
                        help='query to act on')
    return parser

def _init_playlists_dir():
    if not os.path.isdir(PLAYLISTS_DIR):
        os.makedirs(PLAYLISTS_DIR)

def _get_playlist_dir(playlist):
    return os.path.join(PLAYLISTS_DIR, playlist)

def _get_playlist_contents(playlist):
    return sorted(os.listdir(_get_playlist_dir(playlist)))

def _is_playlist(playlist):
    return os.path.isdir(os.path.join(PLAYLISTS_DIR, playlist))

def _check_playlist(playlist):
    if playlist is None:
        logging.error("Must supply a playlist name")
        sys.exit(1)
    elif not _is_playlist(playlist):
        logging.error("Invalid playlist '%s'", playlist)
        sys.exit(1)

def new(playlist):
    print "new(%s)" % playlist
    if playlist is None:
        logging.error("Must supply a playlist name")
        sys.exit(1)
    elif _is_playlist(playlist):
        logging.error("Playlist '%s' already exsts", playlist)
        sys.exit(1)
    else:
        os.makedirs(os.path.join(PLAYLISTS_DIR, playlist))

def list_(playlist):
    print "list(%s)" % playlist
    if playlist is None:
        for playlist in sorted(os.listdir(PLAYLISTS_DIR)):
            if playlist != PLAYLISTS_DATA_FILE:
                print "%s - %d tracks" % (playlist, len(_get_playlist_contents(playlist)))
    else:
        _check_playlist(playlist)
        print "Playlist '%s' - %d tracks" % (playlist, len(_get_playlist_contents(playlist)))
        for track in _get_playlist_contents(playlist):
            print " - %s" % track

def add(playlist, query):
    print "add(%s), query: '%s'" % (playlist, query)
    _check_playlist(playlist)
    format = '$artist\t$album\t$title\t$path'
    proc = subprocess.Popen(['beet', 'list', '-f', format] + query, stdout=subprocess.PIPE)
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
    size = len(_get_playlist_contents(playlist))
    fname_bits = ["%06d" % (size + 1), artist, album, title]
    fname = "-".join(fname_bit.replace(" ", "_") for fname_bit in fname_bits)
    dest = os.path.join(_get_playlist_dir(playlist), fname)
    os.link(path, dest)


def play(playlist):
    print "play(%s)" % playlist
    _check_playlist(playlist)
    playlist_dir = _get_playlist_dir(playlist)
    contents = [os.path.join(playlist_dir, track) for track in _get_playlist_contents(playlist)]
    subprocess.call(["mplayer"] + contents)


def main():
    parser = _get_arg_parser()
    options = parser.parse_args()
    if not any([options.new, options.list, options.add, options.play]):
        print >> sys.stderr, "No action supplied"
        parser.print_help()
        sys.exit(1)

    _init_playlists_dir()

    if options.new:
        new(options.playlist)
    elif options.list:
        list_(options.playlist)
    elif options.add:
        add(options.playlist, options.query)
    elif options.play:
        play(options.playlist)

if __name__ == "__main__":
    main()
