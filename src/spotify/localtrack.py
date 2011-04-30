'''
Created on 30/04/2011

@author: mikel
'''
from _spotify import localtrack as _localtrack

from spotify import track


def create(artist, title, album, length):
    return track.Track(
        _localtrack.create(artist, title, album, length)
    )
