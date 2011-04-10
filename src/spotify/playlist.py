'''
Created on 10/04/2011

@author: mikel
'''
class Playlist:
    _session = None
    _playlist = None
    
    def __init__(self, session, playlist):
        self._session = session
        self._playlist = playlist