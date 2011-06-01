'''
Created on 21/05/2011

@author: mikel
'''

from _spotify import artistbrowse as _artistbrowse

from spotify.utils.decorators import synchronized

from spotify.utils.iterators import CallbackIterator

from spotify import artist, album, track



class ProxyArtistbrowseCallbacks:
    __artistbrowse = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, artistbrowse, callbacks):
        self.__artistbrowse = artistbrowse
        self.__callbacks = callbacks
        self.__c_callback = _artistbrowse.artistbrowse_complete_cb(
            self.artistbrowse_complete
        )
    
    
    def artistbrowse_complete(self, artistbrowse_struct, userdata):
        self.__callbacks.artistbrowse_complete(self.__artistbrowse)
    
    
    def get_c_callback(self):
        return self.__c_callback



class ArtistbrowseCallbacks:
    def artistbrowse_complete(self, artistbrowse):
        pass



class Artistbrowse:
    #The same as on albumbrowse, should honor OOR?
    __artist = None
    __artistbrowse_struct = None
    __proxy_callbacks = None
    
    
    @synchronized
    def __init__(self, session, artist, callbacks):
        self.__artist = artist
        self.__proxy_callbacks = ProxyArtistbrowseCallbacks(self, callbacks)
        self.__artistbrowse_struct = _artistbrowse.create(
            session.get_struct(), artist.get_struct(),
            self.__proxy_callbacks.get_c_callback(), None
        )
    
    
    @synchronized
    def is_loaded(self):
        return _artistbrowse.is_loaded(self.__artistbrowse_struct)
    
    
    @synchronized
    def error(self):
        return _artistbrowse.error(self.__artistbrowse_struct)
    
    
    def artist(self):
        return self.__artist
    
    
    @synchronized
    def num_portraits(self):
        return _artistbrowse.num_portraits(self.__artistbrowse_struct)
    
    
    @synchronized
    def portrait(self, index):
        return _artistbrowse.portrait(self.__artistbrowse_struct)
    
    
    def portraits(self):
        return CallbackIterator(self.num_portraits, self.portrait)
    
    
    @synchronized
    def num_tracks(self):
        return _artistbrowse.num_tracks(self.__artistbrowse_struct)
    
    
    @synchronized
    def track(self, index):
        return track.Track(
            _artistbrowse.track(self.__artistbrowse_struct, index)
        )
    
    
    def tracks(self):
        return CallbackIterator(self.num_tracks, self.track)
    
    
    @synchronized
    def num_albums(self):
        return _artistbrowse.num_albums(self.__artistbrowse_struct)
    
    
    @synchronized
    def album(self, index):
        return album.Album(
            _artistbrowse.album(self.__artistbrowse_struct, index)
        )
    
    
    def albums(self):
        return CallbackIterator(self.num_albums, self.album)
    
    
    @synchronized
    def num_similar_artists(self):
        return _artistbrowse.num_similar_artists(self.__artistbrowse_struct)
    
    
    @synchronized
    def similar_artist(self, index):
        return artist.Artist(
            _artistbrowse.similar_artist(self.__artistbrowse_struct, index)
        )
    
    
    def similar_artists(self):
        return CallbackIterator(self.num_similar_artists, self.similar_artists)
    
    
    @synchronized
    def biography(self):
        return _artistbrowse.biography(self.__artistbrowse_struct)
    
    
    @synchronized
    def add_ref(self):
        _artistbrowse.add_ref(self.__artistbrowse_struct)
    
    
    @synchronized
    def release(self):
        _artistbrowse.release(self.__artistbrowse_struct)
    
    
    def __del__(self):
        self.release()
