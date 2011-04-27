'''
Created on 07/11/2010

@author: mikel
'''
from _spotify import track as _track

from spotify.utils.decorators import synchronized



class Track:
    __session = None
    __track_struct = None
    
    
    def __init__(self, session, track_struct):
        self.__session = session
        self.__track_struct = track_struct
        self.add_ref()
    
    
    @synchronized
    def is_loaded(self):
        return _track.is_loaded(self.__track_struct)
    
    
    @synchronized
    def name(self):
        return _track.name(self.__track_struct)
    
    
    @synchronized
    def add_ref(self):
        return _track.add_ref(self.__track_struct)
    
    
    @synchronized
    def release(self):
        return _track.release(self.__track_struct)
    
    
    def get_struct(self):
        return self.__track_struct
    
    
    def __del__(self):
        self.release()
