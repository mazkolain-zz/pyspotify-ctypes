'''
Created on 30/04/2011

@author: mikel
'''
from _spotify import album as _album, artist as _artist

from spotify.utils.decorators import synchronized, extract_args

from spotify import artist

import binascii

from utils.finalize import track_for_finalization



class AlbumType:
    Album = 0
    Single = 1
    Compilation = 2
    Unknown = 3



@extract_args
@synchronized
def _finalize_album(album_interface, album_struct):
    album_interface.release(album_struct)
    print "album __del__ called"



class Album:
    __album_struct = None
    __album_interface = None
    
    
    def __init__(self, album_struct):
        self.__album_struct = album_struct
        self.__album_interface = _album.AlbumInterface()
        
        #Register finalizers
        args = (self.__album_interface, self.__album_struct)
        track_for_finalization(self, args, _finalize_album)
    
    
    @synchronized
    def is_loaded(self):
        return self.__album_interface.is_loaded(self.__album_struct)
    
    
    @synchronized
    def is_available(self):
        return self.__album_interface.is_available(self.__album_struct)
    
    
    @synchronized
    def artist(self):
        #Increment the refcount so it doesn't get stolen from us
        artist_struct = self.__album_interface.artist(self.__album_struct)
        
        if artist_struct is not None:
            ai = _artist.ArtistInterface()
            ai.add_ref(artist_struct)
            return artist.Artist(artist_struct)
    
    
    @synchronized
    def cover(self):
        res = self.__album_interface.cover(self.__album_struct)
        if res:
            return binascii.b2a_hex(buffer(res.contents))
    
    
    @synchronized
    def name(self):
        return self.__album_interface.name(self.__album_struct)
    
    
    @synchronized
    def year(self):
        return self.__album_interface.year(self.__album_struct)
    
    
    @synchronized
    def type(self):
        return self.__album_interface.type(self.__album_struct)
    
    
    def get_struct(self):
        return self.__album_struct
