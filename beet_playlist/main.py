#!/usr/bin/env python
# encoding: utf-8
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

from argparse import ArgumentParser
import logging
import os
import sys

from .beets_api import run_beet_query
from .common import get_config, HISTORY_LIMIT
from . import add, common

_SHUFFLE_TOKEN = "<SHUFFLED>"


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
    parser.add_argument('--history', action='store_true', default=False,
                        help='Shows last played queries')
    common.add_play_arguments(parser)
    parser.set_defaults(func=play_beets_query)


def play_beets_query(query, shuffle=False, history=False, repeat=False):
    if history and not query:
        _show_history()
    else:
        if history:
            try:
                query, shuffle = _fetch_history_query(query[0], shuffle)
            except ValueError:
                _show_history()
                raise
        tracks = run_beet_query(query)
        if not tracks:
            logging.warn("Query '%s' matched no tracks!", query)
            return
        logging.info("Got %s tracks from query '%s'", len(tracks), query)
        for track in tracks:
            logging.info(" - %s", track.path)
        _push_to_history(query, shuffle)
        common.mplayer([t.path for t in tracks], shuffle=shuffle,
                       repeat=repeat)


def _push_to_history(query, shuffle):
    config = get_config()
    if shuffle:
        query = query + [_SHUFFLE_TOKEN]
    history = [query] + [q for q in config.history if q != query]
    config.history = history[:HISTORY_LIMIT]
    config.save()
    config = get_config()


def _fetch_history_query(query, shuffle):
    try:
        history_num = int(query)
    except ValueError:
        raise ValueError("Invalid int for history lookup: '{}'".format(query))

    try:
        history_query = get_config().history[history_num - 1]
    except IndexError:
        raise ValueError("Invalid history index: '{}'".format(history_num))

    history_shuffle = (history_query[-1] == _SHUFFLE_TOKEN)
    if history_shuffle:
        history_query = [q for q in history_query if q != _SHUFFLE_TOKEN]
    return history_query, shuffle or history_shuffle


def _show_history():
    print("History:")
    for index, query in enumerate(get_config().history):
        print(" {} - {}".format(index + 1, query))

if __name__ == "__main__":
    main()
