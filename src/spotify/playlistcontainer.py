'''
Created on 10/04/2011

@author: mikel
'''
import ctypes

from spotify import DuplicateCallbackError, UnknownCallbackError, handle_sp_error, user

from _spotify import playlistcontainer as _playlistcontainer

from spotify.utils.decorators import synchronized

from spotify.utils.iterators import CallbackIterator

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
        


class PlaylistContainer:
    __container_struct = None
    
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
    def __init__(self, container_struct):
        self.__container_struct = container_struct
        self._playlist_objects = {}
        self._callbacks = {}
        self._is_loaded = False
        _playlistcontainer.add_ref(self.__container_struct)
    
    
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
                self.__container_struct, ptr, None
            )
    
    
    @synchronized
    def remove_callbacks(self, callbacks):
        cb_id = id(callbacks)
        if cb_id not in self._callbacks:
            raise UnknownCallbackError()
        
        else:
            ptr = self._callbacks[cb_id]["ptr"]
            _playlistcontainer.remove_callbacks(
                self.__container_struct, ptr, None
            )
            del self._callbacks[cb_id]
    
    
    def remove_all_callbacks(self):
        for item in self._callbacks:
            self.remove_callbacks(item["callbacks"])
    
    
    @synchronized
    def num_playlists(self):
        return _playlistcontainer.num_playlists(self.__container_struct)
    
    
    @synchronized
    def _get_playlist_object(self, pos):
        if pos not in self._playlist_objects:
            self._playlist_objects[pos] = playlist.Playlist(
                _playlistcontainer.playlist(self.__container_struct, pos)
            )
        
        return self._playlist_objects[pos]
    
    
    def playlist(self, pos):
        return self._get_playlist_object(pos)
    
    
    def playlists(self):
        return CallbackIterator(self.num_playlists, self.playlist)
    
    
    @synchronized
    def playlist_type(self, index):
        return _playlistcontainer.playlist_type(self.__container_struct, index)
    
    
    @synchronized
    def playlist_folder_name(self, index):
        buf = (ctypes.c_char() * 255)()
        handle_sp_error(
            _playlistcontainer.playlist_folder_name(
                self.__container_struct, index, ctypes.byref(buf), 255
            )
        )
        return buf.value
    
    
    @synchronized
    def playlist_folder_id(self, index):
        return _playlistcontainer.playlist_folder_id(
            self.__container_struct, index
        )
    
    
    @synchronized
    def add_new_playlist(self, name):
        return playlist.Playlist(
            _playlistcontainer.add_new_playlist(self.__container_struct, name)
        )
    
    
    @synchronized
    def add_playlist(self, link):
        return playlist.Playlist(
            _playlistcontainer.add_playlist(
                self.__container_struct, link.get_struct()
            )
        )
    
    
    @synchronized
    def remove_playlist(self, index):
        #FIXME: Should refresh index in _playlist_objects
        handle_sp_error(
            _playlistcontainer.remove_playlist(
                self.__container_struct, index
            )
        )
    
    
    @synchronized
    def move_playlist(self, index, new_position, dry_run):
        handle_sp_error(
            _playlistcontainer.move_playlist(
                self.__container_struct, new_position, dry_run
            )
        )
    
    
    @synchronized
    def add_folder(self, index, name):
        handle_sp_error(
            _playlistcontainer.add_folder(
                self.__container_struct, index, name
            )
        )
    
    
    @synchronized
    def owner(self):
        return user.User(
            _playlistcontainer.owner(self.__container_struct)
        )
        
    
    @synchronized
    def add_ref(self):
        _playlistcontainer.add_ref()
    
    
    @synchronized
    def release(self):
        _playlistcontainer.release()
    
    
    def __len__(self):
        return self.num_playlists()
    
    
    def get_struct(self):
        return self.__container_struct
    
    
    def __del__(self):
        self.remove_all_callbacks()
        _playlistcontainer.release(self.__container_struct)
