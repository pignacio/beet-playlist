#!/usr/bin/env python
# encoding: utf-8
'''
Created on May 4, 2014

@author: ignacio
'''
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)
import subprocess


class BeetTrack(object):
    def __init__(self, artist, album, title, path):
        self.artist = artist
        self.album = album
        self.title = title
        self.path = path

    def __str__(self):
        return " - ".join([self.artist, self.album, self.title])


def run_beet_query(query):
    beet_format = '$artist\t$album\t$title\t$path'
    proc = subprocess.Popen(['beet', 'list', '-f', beet_format] + query,
                            stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    proc.wait()
    return [BeetTrack(*line.rstrip('\n').split("\t")) for line in lines]
