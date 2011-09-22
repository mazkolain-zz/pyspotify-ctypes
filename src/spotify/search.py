'''
Created on 25/05/2011

@author: mazkolain
'''
from _spotify import search as _search

from spotify import track, album, artist

from spotify.utils.decorators import synchronized

from spotify.utils.iterators import CallbackIterator

import weakref



class ProxySearchCallbacks:
    __search = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, search, callbacks):
        self.__search = weakref.proxy(search)
        self.__callbacks = callbacks
        self.__c_callback = _search.search_complete_cb(self.search_complete)
        
        
    def search_complete(self, search_struct, userdata):
        self.__callbacks.search_complete(self.__search)
    
    
    def get_c_callback(self):
        return self.__c_callback



class SearchCallbacks:
    def search_complete(self, result):
        pass



class Search:
    #Not private, so RadioSearchh can see it
    _search_struct = None
    __search_interface = None
    __proxy_callbacks = None
    
    
    @synchronized
    def __init__(self, session, query, track_offset=0, track_count=0, album_offset=0, album_count=0, artist_offset=0, artist_count=0, callbacks=None):
        self.__proxy_callbacks = ProxySearchCallbacks(self, callbacks)
        self.__search_interface = _search.SearchInterface()
        self._search_struct = self.__search_interface.create(
            session.get_struct(), query,
            track_offset, track_count,
            album_offset, album_count,
            artist_offset, artist_count,
            self.__proxy_callbacks.get_c_callback(),
            None
        )
        
    
    
    @synchronized
    def is_loaded(self):
        return self.__search_interface.is_loaded(self._search_struct)
    
    
    @synchronized
    def error(self):
        return self.__search_interface.error(self._search_struct)
    
    
    @synchronized
    def num_tracks(self):
        return self.__search_interface.num_tracks(self._search_struct)
    
    
    @synchronized
    def track(self, index):
        return track.Track(self.__search_interface.track(self._search_struct, index))
    
    
    def tracks(self):
        return CallbackIterator(self.num_tracks, self.track)
    
    
    @synchronized
    def num_albums(self):
        return self.__search_interface.num_albums(self._search_struct)
    
    
    @synchronized
    def album(self, index):
        return album.Album(self.__search_interface.album(self._search_struct, index))
    
    
    def albums(self):
        return CallbackIterator(self.num_albums, self.album)
    
    
    @synchronized
    def num_artists(self):
        return self.__search_interface.num_artists(self._search_struct)
    
    
    @synchronized
    def artist(self, index):
        return artist.Artist(self.__search_interface.artist(self._search_struct, index))
    
    
    def artists(self):
        return CallbackIterator(self.num_artists, self.artist)
    
    
    @synchronized
    def query(self):
        return self.__search_interface.query(self._search_struct)
    
    
    @synchronized
    def did_you_mean(self):
        return self.__search_interface.did_you_mean(self._search_struct)
    
    
    @synchronized
    def total_tracks(self):
        return self.__search_interface.total_tracks(self._search_struct)
    
    
    @synchronized
    def total_albums(self):
        return self.__search_interface.total_albums(self._search_struct)
    
    
    @synchronized
    def total_artists(self):
        return self.__search_interface.total_artists(self._search_struct)
    
    
    @synchronized
    def __del__(self):
        print "search __del__ called"
        self.__search_interface.release(self._search_struct)
