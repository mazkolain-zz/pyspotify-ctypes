'''
Created on 30/04/2011

@author: mikel
'''
from _spotify import artist as _artist

from spotify.utils.decorators import synchronized, extract_args

import binascii

from utils.finalize import track_for_finalization



@extract_args
@synchronized
def _finalize_artist(artist_interface, artist_struct):
    artist_interface.release(artist_struct)
    print "artist __del__ called"



class Artist:
    __artist_struct = None
    __artist_interface = None
    
    
    def __init__(self, artist_struct):
        self.__artist_struct = artist_struct
        self.__artist_interface = _artist.ArtistInterface()
        
        #register finalizers
        args = (self.__artist_interface, self.__artist_struct)
        track_for_finalization(self, args, _finalize_artist)

    
    @synchronized
    def name(self):
        return self.__artist_interface.name(self.__artist_struct)
    
    
    @synchronized
    def is_loaded(self):
        return self.__artist_interface.is_loaded(self.__artist_struct)
    
    
    @synchronized
    def portrait(self):
        res = self.__artist_interface.portrait(self.__artist_struct)
        if res:
            return binascii.b2a_hex(buffer(res.contents))
    
    
    def get_struct(self):
        return self.__artist_struct
