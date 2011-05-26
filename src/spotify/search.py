'''
Created on 25/05/2011

@author: mazkolain
'''
from _spotify import search as _search

from spotify import track, album, artist

from spotify.utils.decorators import synchronized



class ProxySearchCallbacks:
    __search = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, search, callbacks):
        self.__search = search
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
    __search_struct = None
    __proxy_callbacks = None
    
    
    @synchronized
    def __init__(self, session, query, track_offset=0, track_count=0, album_offset=0, album_count=0, artist_offset=0, artist_count=0, callbacks=None):
        self.__proxy_callbacks = ProxySearchCallbacks(self, callbacks)
        self.__search_struct = _search.create(
            session.get_struct(), query,
            track_offset, track_count,
            album_offset, album_count,
            artist_offset, artist_count,
            self.__proxy_callbacks.get_c_callback(),
            None
        )
    
    
    @synchronized
    def is_loaded(self):
        return _search.is_loaded(self.__search_struct)
    
    
    @synchronized
    def error(self):
        return _search.error(self.__search_struct)
    
    
    @synchronized
    def num_tracks(self):
        return _search.num_tracks(self.__search_struct)
    
    
    @synchronized
    def track(self, index):
        return track.Track(_search.track(self.__search_struct, index))
    
    
    @synchronized
    def num_albums(self):
        return _search.num_albums(self.__search_struct)
    
    
    @synchronized
    def album(self, index):
        return album.Album(_search.album(self.__search_struct, index))
    
    
    @synchronized
    def num_artists(self):
        return _search.num_artists(self.__search_struct)
    
    
    @synchronized
    def artist(self, index):
        return artist.Artist(_search.artist(self.__search_struct, index))
    
    
    @synchronized
    def query(self):
        return _search.query(self.__search_struct)
    
    
    @synchronized
    def did_you_mean(self):
        return _search.did_you_mean(self.__search_struct)
    
    
    @synchronized
    def total_tracks(self):
        return _search.total_tracks(self.__search_struct)
    
    
    @synchronized
    def total_albums(self):
        return _search.total_albums(self.__search_struct)
    
    
    @synchronized
    def total_artists(self):
        return _search.total_artists(self.__search_struct)
    
    
    @synchronized
    def add_ref(self):
        _search.add_ref(self.__search_struct)
    
    
    @synchronized
    def release(self):
        _search.release(self.__search_struct)
    
    
    @synchronized
    def __del__(self):
        self.release()
