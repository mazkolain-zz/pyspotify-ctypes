'''
Created on 30/04/2011

@author: mikel
'''
from _spotify import album as _album

from spotify.utils.decorators import synchronized

from spotify import artist

import binascii



class AlbumType:
    Album = 0
    Single = 1
    Compilation = 2
    Unknown = 3



class Album:
    __album_struct = None
    
    
    def __init__(self, album_struct):
        self.__album_struct = album_struct
    
    
    @synchronized
    def is_loaded(self):
        return _album.is_loaded(self.__album_struct)
    
    
    @synchronized
    def is_available(self):
        return _album.is_available(self.__album_struct)
    
    
    @synchronized
    def artist(self):
        return artist.Artist(_album.artist(self.__album_struct))
    
    
    @synchronized
    def cover(self):
        res = _album.cover(self.__album_struct).contents
        if res is not None:
            return binascii.b2a_hex(res.value)
    
    
    @synchronized
    def name(self):
        return _album.name(self.__album_struct)
    
    
    @synchronized
    def year(self):
        return _album.year(self.__album_struct)
    
    
    @synchronized
    def type(self):
        return _album.type(self.__album_struct)
    
    
    @synchronized
    def add_ref(self):
        _album.add_ref(self.__album_struct)
    
    
    @synchronized
    def release(self):
        _album.release(self.__album_struct)
