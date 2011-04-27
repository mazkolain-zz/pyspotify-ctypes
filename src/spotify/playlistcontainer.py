'''
Created on 10/04/2011

@author: mikel
'''
import ctypes

from spotify import DuplicateCallbackError, UnknownCallbackError

from _spotify import playlistcontainer as _playlistcontainer

from spotify.utils.decorators import synchronized

import playlist


class ProxyPlaylistContainerCallbacks:
    _container = None
    _callbacks = None
    
    
    def __init__(self, container, callbacks):
        self._container = container
        self._callbacks = callbacks
    
    
    def _playlist_added(self, c_container, c_playlist, position, data):
        self._callbacks.playlist_added(
            self._container, self._container.playlist(position), position
        )
    
    
    def _playlist_removed(self, c_container, c_playlist, position, data):
        self._callbacks.playlist_removed(
            self._container, self._container.playlist(position), position
        )
    
    
    def _playlist_moved(self, c_container, c_playlist, position, new_position, data):
        self._callbacks.playlist_moved(
            self._container, self._container.playlist(position),
            position, new_position
        )
    
    
    def _container_loaded(self, container, data):
        #Also set the container's flag
        self._container.set_loaded(True)
        self._callbacks.container_loaded(self._container)
        
    
    def get_callback_struct(self):
        return _playlistcontainer.callbacks(
            _playlistcontainer.cb_playlist_added(self._playlist_added),
            _playlistcontainer.cb_playlist_removed(self._playlist_removed),
            _playlistcontainer.cb_playlist_moved(self._playlist_moved),
            _playlistcontainer.cb_container_loaded(self._container_loaded),
        )



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
    
    #Keep references to callbacks structs an the like
    _callbacks = None
    
    #To store generated playlist instances
    _playlist_objects = None
    
    #Is loaded check, not provided by libspotify
    _is_loaded = None
    
    
    @synchronized
    def __init__(self, session, container):
        self._session = session
        self._container = container
        self._playlist_objects = {}
        self._callbacks = {}
        self._is_loaded = False
        _playlistcontainer.add_ref(self._container)
    
    
    def set_loaded(self, status):
        self._is_loaded = status
    
    
    def is_loaded(self):
        return self._is_loaded
    
    
    @synchronized
    def add_callbacks(self, callbacks):
        cb_id = id(callbacks)
        if cb_id in self._callbacks:
            raise DuplicateCallbackError()
        
        else:
            proxy = ProxyPlaylistContainerCallbacks(self, callbacks)
            struct = proxy.get_callback_struct()
            ptr = ctypes.pointer(struct)
            
            self._callbacks[cb_id] = {
                "struct": struct,
                "ptr": ptr,
                "callbacks": callbacks,
            }
            
            _playlistcontainer.add_callbacks(
                self._container, ptr, None
            )
    
    
    @synchronized
    def remove_callbacks(self, callbacks):
        cb_id = id(callbacks)
        if cb_id not in self._callbacks:
            raise UnknownCallbackError()
        
        else:
            ptr = self._callbacks[cb_id]["ptr"]
            _playlistcontainer.remove_callbacks(
                self._container, ptr, None
            )
            del self._callbacks[cb_id]
    
    
    def remove_all_callbacks(self):
        for item in self._callbacks:
            self.remove_callbacks(item["callbacks"])
    
    
    @synchronized
    def num_playlists(self):
        return _playlistcontainer.num_playlists(self._container)
    
    
    @synchronized
    def _get_playlist_object(self, pos):
        if pos not in self._playlist_objects:
            self._playlist_objects[pos] = playlist.Playlist(
                self._session, _playlistcontainer.playlist(self._container, pos)
            )
        
        return self._playlist_objects[pos]
    
    
    def playlist(self, pos):
        return self._get_playlist_object(pos)
    
    
    def __iter__(self):
        return PlaylistContainerIterator(self)
    
    
    def __len__(self):
        return self.num_playlists()
    
    
    def get_struct(self):
        return self._container
    
    
    def __del__(self):
        self.remove_all_callbacks()
        _playlistcontainer.release(self._container)
    
    
    
