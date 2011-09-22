'''
Created on 30/04/2011

@author: mikel
'''
from _spotify import album as _album, artist as _artist

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
    __album_interface = None
    
    
    def __init__(self, album_struct):
        self.__album_struct = album_struct
        self.__album_interface = _album.AlbumInterface()
    
    
    @synchronized
    def is_loaded(self):
        return self.__album_interface.is_loaded(self.__album_struct)
    
    
    @synchronized
    def is_available(self):
        return self.__album_interface.is_available(self.__album_struct)
    
    
    @synchronized
    def artist(self):
        artist_struct = self.__album_interface.artist(self.__album_struct)
        
        #This reference is borrowed, preincrement it
        ai = _artist.ArtistInterface()
        ai.add_ref(artist_struct)
        
        return artist.Artist(artist_struct)
    
    
    @synchronized
    def cover(self):
        res = self.__album_interface.cover(self.__album_struct).contents
        if res is not None:
            return binascii.b2a_hex(buffer(res))
    
    
    @synchronized
    def name(self):
        return self.__album_interface.name(self.__album_struct)
    
    
    @synchronized
    def year(self):
        return self.__album_interface.year(self.__album_struct)
    
    
    @synchronized
    def type(self):
        return self.__album_interface.type(self.__album_struct)
    
    
    @synchronized
    def add_ref(self):
        self.__album_interface.add_ref(self.__album_struct)
    
    
    @synchronized
    def __del__(self):
        self.__album_interface.release(self.__album_struct)
    
    
    def get_struct(self):
        return self.__album_struct
