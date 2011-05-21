'''
Created on 20/05/2011

@author: mikel
'''
from _spotify import albumbrowse as _albumbrowse

from spotify.utils.decorators import synchronized

from spotify import album, artist, track


class Albumtype:
    Album = 0
    Single = 1
    Compilation = 2
    Unknown = 3



class ProxyAlbumbrowseCallbacks:
    __albumbrowse = None
    __callbacks = None
    __c_callback = None
    
    
    def __init__(self, albumbrowse, callbacks):
        self.__albumbrowse = albumbrowse
        self.__callbacks = callbacks
        self.__c_callback = _albumbrowse.callback(self.albumbrowse_complete)
    
    
    def albumbrowse_complete(self, albumbrowse_struct, userdata):
        self.__callbacks.albumbrowse_complete(self.__albumbrowse)
    
    
    def get_c_callback(self):
        return self.__c_callback



class AlbumbrowseCallbacks:
    def albumbrowse_complete(self, albumbrowse):
        pass



class Albumbrowse:
    #Should we honor OOR?
    __album = None
    __albumbrowse_struct = None
    __proxy_callbacks = None
    
    
    @synchronized
    def __init__(self, session, album, callbacks):
        self.__album = album
        self.__proxy_callbacks = ProxyAlbumbrowseCallbacks(self, callbacks)
        self.__albumbrowse_struct = _albumbrowse.create(
            session.get_struct(), album.get_struct(),
            self.__proxy_callbacks.get_c_callback(), None
        )
    
    
    @synchronized
    def is_loaded(self):
        return _albumbrowse.is_loaded(self.__albumbrowse_struct)
    
    
    @synchronized
    def error(self):
        return _albumbrowse.is_loaded(self.__albumbrowse_struct)
    
    
    def album(self):
        return self.__album
    
    
    @synchronized
    def artist(self):
        return artist.Artist(_albumbrowse.artist(self.__albumbrowse_struct))
    
    
    @synchronized
    def num_copyrights(self):
        return _albumbrowse.num_copyrights(self.__albumbrowse_struct)
    
    
    @synchronized
    def copyright(self, index):
        return _albumbrowse.copyright(self.__albumbrowse_struct, index)
    
    
    @synchronized
    def num_tracks(self):
        return _albumbrowse.num_tracks(self.__albumbrowse_struct)
    
    
    @synchronized
    def track(self, index):
        return track.Track(
            _albumbrowse.track(self.__albumbrowse_struct, index)
        )
    
    
    @synchronized
    def review(self):
        return _albumbrowse.review(self.__albumbrowse_struct)
    
    
    @synchronized
    def add_ref(self):
        _albumbrowse.add_ref(self.__albumbrowse_struct)
    
    
    @synchronized
    def release(self):
        _albumbrowse.release(self.__albumbrowse_struct)
    
    
    def __del__(self):
        self.release()
