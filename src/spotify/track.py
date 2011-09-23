'''
Created on 07/11/2010

@author: mikel
'''
import ctypes

from _spotify import track as _track

from spotify import artist, album

from spotify.utils.decorators import synchronized

from spotify.utils.iterators import CallbackIterator



@synchronized
def set_starred(session, tracks, star):
    arr = (ctypes.c_void_p * len(tracks))()
    ti = _track.TrackInterface()
    
    for index, item in enumerate(tracks):
        arr[index] = item.get_struct()
    
    ti.set_starred(
        session.get_struct(), ctypes.byref(arr), len(tracks), star
    )



class Track:
    __track_struct = None
    __track_interface = None
    
    
    def __init__(self, track_struct):
        self.__track_struct = track_struct
        self.__track_interface = _track.TrackInterface()
        self.add_ref()
    
    
    @synchronized
    def is_loaded(self):
        return self.__track_interface.is_loaded(self.__track_struct)
    
    
    @synchronized
    def error(self):
        return self.__track_interface.error(self.__track_struct)
    
    
    @synchronized
    def is_available(self, session):
        return self.__track_interface.is_available(session.get_struct(), self.get_struct())
    
    
    @synchronized
    def is_local(self, session):
        return self.__track_interface.is_local(session.get_struct(), self.get_struct())
    
    
    @synchronized
    def is_autolinked(self, session):
        return self.__track_interface.is_autolinked(session.get_struct(), self.get_struct())
    
    
    @synchronized
    def is_starred(self, session):
        return self.__track_interface.is_starred(session.get_struct(), self.get_struct())
    
    
    @synchronized
    def num_artists(self):
        return self.__track_interface.num_artists(self.__track_struct)
    
    
    @synchronized
    def artist(self, index):
        return artist.Artist(self.__track_interface.artist(self.__track_struct, index))
    
    
    def artists(self):
        return CallbackIterator(self.num_artists, self.artist)
    
    
    @synchronized
    def album(self):
        return album.Album(self.__track_interface.album(self.__track_struct))
    
    
    @synchronized
    def name(self):
        return self.__track_interface.name(self.__track_struct)
    
    
    @synchronized
    def duration(self):
        return self.__track_interface.duration(self.__track_struct)
    
    
    @synchronized
    def popularity(self):
        return self.__track_interface.popularity(self.__track_struct)
    
    
    @synchronized
    def disc(self):
        return self.__track_interface.disc(self.__track_struct)
    
    
    @synchronized
    def index(self):
        return self.__track_interface.index(self.__track_struct)
    
    
    @synchronized
    def __del__(self):
        self.__track_interface.release(self.__track_struct)
    
    
    def get_struct(self):
        return self.__track_struct
