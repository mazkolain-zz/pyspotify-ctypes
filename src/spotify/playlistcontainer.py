'''
Created on 10/04/2011

@author: mikel
'''
import ctypes

from _spotify import playlistcontainer as _playlistcontainer

import playlist


class PlaylistContainerCallbacks:
    def playlist_added(self, container, playlist, position):
        pass
    
    def playlist_removed(self, container, playlist, position):
        pass
    
    def playlist_moved(self, container, playlist, position, new_position):
        pass
    
    def container_loaded(self, container):
        pass


class PlaylistContainerIterator:
    _container = None
    _pos = None
    
    def __init__(self, container):
        self._container = container
        self._pos = 0
    
    def __iter__(self):
        return self
    
    def next(self):
        if self._pos < self._container.num_playlists():
            playlist = self._container.playlist(self._pos)
            self._pos += 1
            return playlist
        else:
            raise StopIteration
        

class PlaylistContainer:
    _session = None
    _container = None
    
    _manager = None
    
    #Just a shortcut callback to avoid subclassing PlaylistContainerCallbacks
    _onload_callback = None
    
    #Avoid garbage collection
    _callbacks = None

    def __init__(self, session, container, onload=None):
        self._session = session
        self._container = container
        _playlistcontainer.add_ref(self._container)
        self._onload_callback = onload
        
        #Register callbacks as soon as possible
        self._callbacks = _playlistcontainer.callbacks(
            _playlistcontainer.cb_playlist_added(self._playlist_added),
            _playlistcontainer.cb_playlist_removed(self._playlist_removed),
            _playlistcontainer.cb_playlist_moved(self._playlist_moved),
            _playlistcontainer.cb_container_loaded(self._container_loaded),
        )
        _playlistcontainer.add_callbacks(
            self._container,
            ctypes.pointer(self._callbacks),
            ctypes.c_void_p()
        )
    
    
    def add_callbacks(self, manager):
        self._manager = manager
        
    
    def num_playlists(self):
        return _playlistcontainer.num_playlists(self._container)
    
    
    def playlist(self, pos):
        return playlist.Playlist(
            self._session, _playlistcontainer.playlist(self._container, pos)
        )
    
    
    def __iter__(self):
        return PlaylistContainerIterator(self)
    
    
    def __len__(self):
        return self.num_playlists()
    
    
    def __del__(self):
        _playlistcontainer.release(self._container)
    
    
    #Callback proxies
    def _playlist_added(self, container, playlist_p, position, data):
        po = playlist.Playlist(self._session, playlist_p)
        if self._manager != None:
            self._manager.playlist_added(
                self, po, position
            )
    
    
    def _playlist_removed(self, container, playlist_p, position, data):
        po = playlist.Playlist(self._session, playlist_p)
        if self._manager != None:
            self._manager.playlist_removed(
                self, po, position
            )
    
    
    def _playlist_moved(self, container, playlist_p, position, new_position, data):
        po = playlist.Playlist(self._session, playlist_p)
        if self._manager != None:
            self._manager.playlist_moved(
                self, po, position, new_position
            )
    
    
    def _container_loaded(self, container, data):
        #Try with the shortcut callback
        if self._onload_callback != None:
            self._onload_callback(self)
        
        #With the manager one
        if self._manager != None:
            self._manager.container_loaded(self)
