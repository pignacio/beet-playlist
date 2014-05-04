from argparse import ArgumentParser
import common
import add
import logging
import os
import sys

def _get_arg_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')
    common.add_parsers(subparsers)
    add.add_parser(subparsers)
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
        raise Exception("Missing 'func' attribute. Maybe subparser '{}' didnt correctly set_defaults()?".format(subparser))
    _init_playlists_dir()
    func(**options.__dict__)


if __name__ == "__main__":
    main()
