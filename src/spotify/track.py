'''
Created on 07/11/2010

@author: mikel
'''
import ctypes

from _spotify import track as _track

from spotify import artist, album

from spotify.utils.decorators import synchronized



@synchronized
def is_available(session, track):
    return _track.is_available(session.get_struct(), track.get_struct())


@synchronized
def is_local(session, track):
    return _track.is_local(session.get_struct(), track.get_struct())


@synchronized
def is_autolinked(session, track):
    return _track.is_autolinked(session.get_struct(), track.get_struct())


@synchronized
def is_starred(session, track):
    return _track.is_starred(session.get_struct(), track.get_struct())


@synchronized
def set_starred(session, tracks, star):
    arr = (ctypes.c_void_p * len(tracks))()
    
    for index, item in enumerate(tracks):
        arr[index] = item.get_struct()
    
    _track.set_starred(
        session.get_struct(), ctypes.byref(arr), len(tracks), star
    )



class Track:
    __track_struct = None
    
    
    def __init__(self, track_struct):
        self.__track_struct = track_struct
        self.add_ref()
    
    
    @synchronized
    def is_loaded(self):
        return _track.is_loaded(self.__track_struct)
    
    
    @synchronized
    def error(self):
        return _track.error(self.__track_struct)
    
    
    @synchronized
    def num_artists(self):
        return _track.num_artists(self.__track_struct)
    
    
    @synchronized
    def artist(self, index):
        return artist.Artist(_track.artist(self.__track_struct, index))
    
    
    @synchronized
    def album(self):
        return album.Album(_track.album(self.__track_struct))
    
    
    @synchronized
    def name(self):
        return _track.name(self.__track_struct)
    
    
    @synchronized
    def duration(self):
        return _track.duration(self.__track_struct)
    
    
    @synchronized
    def popularity(self):
        return _track.popularity(self.__track_struct)
    
    
    @synchronized
    def disc(self):
        return _track.disc(self.__track_struct)
    
    
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
