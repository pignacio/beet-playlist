from argparse import ArgumentParser
import common
import add
import logging
import os
import sys
from beets_api import run_beet_query


def _get_arg_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')
    common.add_parsers(subparsers)
    add.add_parser(subparsers)
    add_parsers(subparsers)
    return parser


def _init_playlists_dir():
    if not os.path.isdir(common.PLAYLISTS_DIR):
        os.makedirs(common.PLAYLISTS_DIR)


def _extract_from_options(key, options):
    res = getattr(options, key)
    delattr(options, key)
    return res


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = _get_arg_parser()
    options = parser.parse_args()

    subparser = _extract_from_options("subparser", options)

    try:
        func = _extract_from_options("func", options)
    except AttributeError:
        raise Exception("Missing 'func' attribute. Maybe subparser '{}' didnt "
                        "correctly set_defaults()?".format(subparser))
    _init_playlists_dir()
    func(**options.__dict__)


def add_parsers(subparsers):
    parser = subparsers.add_parser("play_query")
    parser.add_argument('query', nargs="*",
                        help='beets query to play')
    parser.add_argument('--shuffle', action='store_true', default=False,
                        help='')
    parser.set_defaults(func=play_beets_query)


def play_beets_query(query, shuffle=False):
    tracks = run_beet_query(query)
    if not tracks:
        logging.warn("Query '{}' matched no tracks!".format(query))
        return
    logging.info("Got %s tracks from query '%s'", len(tracks), query)
    for track in tracks:
        logging.info(" - %s", track.path)
    common.mplayer([t.path for t in tracks], shuffle=shuffle)

if __name__ == "__main__":
    main()
