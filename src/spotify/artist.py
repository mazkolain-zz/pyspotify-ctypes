'''
Created on 30/04/2011

@author: mikel
'''
from _spotify import artist as _artist

from spotify.utils.decorators import synchronized



class Artist:
    __artist_struct = None
    
    
    def __init__(self, artist_struct):
        self.__artist_struct = artist_struct

    
    @synchronized
    def name(self):
        return _artist.name(self.__artist_struct)
    
    
    @synchronized
    def is_loaded(self):
        return _artist.is_loaded(self.__artist_struct)
    
    
    @synchronized
    def add_ref(self):
        _artist.add_ref(self.__artist_struct)
    
    
    @synchronized
    def release(self):
        _artist.release(self.__artist_struct)
