'''
Created on 27/05/2011

@author: mikel
'''
from _spotify import toplistbrowse as _toplistbrowse

from spotify.utils.decorators import synchronized

from spotify.utils.iterators import CallbackIterator

from spotify import artist, album, track



def encode_region(country_code):
    uc = country_code.upper()
    if len(uc) != 2:
        raise "The country code must be two chars long"
    else:
        return ord(uc[0]) << 8 | ord(uc[1])



class ToplistType:
    Artists = 0
    Albums = 1
    Tracks = 2



class ToplistRegion:
    Everywhere = 0
    User = 1



class ProxyToplistbrowseCallbacks:
    __toplistbrowse = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, toplistbrowse, callbacks):
        self.__toplistbrowse = toplistbrowse
        self.__callbacks = callbacks
        self.__c_callback = _toplistbrowse.toplistbrowse_complete_cb(
            self.toplistbrowse_complete
        )
    
    
    def toplistbrowse_complete(self, toplisbrowse_struct, userdata):
        self.__callbacks.toplistbrowse_complete(self.__toplistbrowse)
    
    
    def get_c_callback(self):
        return self.__c_callback



class ToplistbrowseCallbacks:
    def toplistbrowse_complete(self, toplisbrowse):
        pass



class Toplistbrowse:
    __proxy_callbacks = None
    __toplistbrowse_struct = None
    
    
    @synchronized
    def __init__(self, session, type, region, username=None, callbacks=None):
        if callbacks is not None:
            self.__proxy_callbacks = ProxyToplistbrowseCallbacks(
                self, callbacks
            )
            c_callback = self.__proxy_callbacks.get_c_callback()
        else:
            c_callback = None
        
        self.__toplistbrowse_struct = _toplistbrowse.create(
            session.get_struct(), type, region, username, c_callback, None
        )
    
    
    @synchronized
    def is_loaded(self):
        return _toplistbrowse.is_loaded(self.__toplistbrowse_struct)
    
    
    @synchronized
    def error(self):
        return _toplistbrowse.error(self.__toplistbrowse_struct)
    
    
    @synchronized
    def add_ref(self):
        _toplistbrowse.add_ref(self.__toplistbrowse_struct)
    
    
    @synchronized
    def release(self):
        _toplistbrowse.release(self.__toplistbrowse_struct)
    
    
    @synchronized
    def num_artists(self):
        return _toplistbrowse.num_artists(self.__toplistbrowse_struct)
    
    
    @synchronized
    def artist(self, index):
        return artist.Artist(
            _toplistbrowse.artist(self.__toplistbrowse_struct, index)
        )
    
    
    def artists(self):
        return CallbackIterator(self.num_artists, self.artist)
    
    
    @synchronized
    def num_albums(self):
        return _toplistbrowse.num_albums(self.__toplistbrowse_struct)
    
    
    @synchronized
    def album(self, index):
        return album.Album(
            _toplistbrowse.album(self.__toplistbrowse_struct, index)
        )
    
    
    def albums(self):
        return CallbackIterator(self.num_albums, self.album)
    
    
    @synchronized
    def num_tracks(self):
        return _toplistbrowse.num_tracks(self.__toplistbrowse_struct)
    
    
    @synchronized
    def track(self, index):
        return track.Track(
            _toplistbrowse.track(self.__toplistbrowse_struct, index)
        )
    
    
    def tracks(self):
        return CallbackIterator(self.num_tracks, self.track)
