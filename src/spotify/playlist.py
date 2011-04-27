'''
Created on 10/04/2011

@author: mikel
'''
import ctypes

from spotify import user, DuplicateCallbackError, UnknownCallbackError

from _spotify import playlist as _playlist

from spotify import track

from spotify.utils.decorators import synchronized



class ProxyPlaylistCallbacks:
    _c_session = None
    _playlist = None
    _callbacks = None
    
    def __init__(self, c_session, playlist, callbacks):
        self._c_session = c_session
        self._playlist = playlist
        self._callbacks = callbacks
    
    #Callback proxies
    def _tracks_added(self, playlist, tracks, num_tracks, position, userdata):
        self._callbacks.tracks_added(self._playlist, tracks, position)
    
    def _tracks_removed(self, playlist, tracks, num_tracks, userdata):
        self._callbacks.tracks_removed(self._playlist, tracks)
    
    def _tracks_moved(self, playlist, tracks, num_tracks, new_position, userdata):
        self._callbacks.tracks_moved(self._playlist, tracks, new_position)
    
    def _playlist_renamed(self, playlist, userdata):
        self._callbacks.playlist_renamed(self._playlist)
    
    def _playlist_state_changed(self, playlist, userdata):
        #print "_playlist_state_changed"
        self._callbacks.playlist_state_changed(self._playlist)
    
    def _playlist_update_in_progress(self, playlist, done, userdata):
        self._callbacks.playlist_update_in_progress(
            self._playlist, done
        )
    
    def _playlist_metadata_updated(self, playlist, userdata):
        self._callbacks.playlist_metadata_updated(self._playlist)
    
    def _track_created_changed(self, playlist, position, c_user, when, userdata):
        self._callbacks.track_created_changed(
            self._playlist, position, user.User(self._c_session, c_user), when
        )
    
    def _track_seen_changed(self, playlist, position, seen, userdata):
        self._callbacks.track_seen_changed(self._playlist, position, seen)
    
    def _description_changed(self, playlist, desc, userdata):
        self._callbacks.description_changed(self._playlist, desc)
    
    def _image_changed(self, playlist, image, userdata):
        self._callbacks.image_changed(self._playlist, image)
    
    def _track_message_changed(self, playlist, position, message, userdata):
        self._callbacks.track_message_changed(
            self._playlist, position, message
        )
    
    def _subscribers_changed(self, playlist, userdata):
        self._callbacks.subscribers_changed(
            self._playlist
        )
    
    #Build up the struct
    def get_callback_struct(self):
        return _playlist.callbacks(
            _playlist.cb_tracks_added(self._tracks_added),
            _playlist.cb_tracks_removed(self._tracks_removed),
            _playlist.cb_tracks_moved(self._tracks_moved),
            _playlist.cb_playlist_renamed(self._playlist_renamed),
            _playlist.cb_playlist_state_changed(self._playlist_state_changed),
            _playlist.cb_playlist_update_in_progress(self._playlist_update_in_progress),
            _playlist.cb_playlist_metadata_updated(self._playlist_metadata_updated),
            _playlist.cb_track_created_changed(self._track_created_changed),
            _playlist.cb_track_seen_changed(self._track_seen_changed),
            _playlist.cb_description_changed(self._description_changed),
            _playlist.cb_image_changed(self._image_changed),
            _playlist.cb_track_message_changed(self._track_message_changed),
            _playlist.cb_subscribers_changed(self._subscribers_changed),
        )


class PlaylistCallbacks:
    def tracks_added(self, playlist, tracks, position):
        pass
    
    def tracks_removed(self, playlist, tracks):
        pass
    
    def tracks_moved(self, playlist, tracks, new_position):
        pass
    
    def playlist_renamed(self, playlist):
        pass
    
    def playlist_state_changed(self, playlist):
        pass
    
    def playlist_update_in_progress(self, playlist, done):
        pass
    
    def playlist_metadata_updated(self, playlist):
        pass
    
    def track_created_changed(self, playlist, position, user, when):
        pass
    
    def track_seen_changed(self, playlist, position, seen):
        pass
    
    def description_changed(self, playlist, desc):
        pass
    
    def image_changed(self, playlist, image):
        pass
    
    def track_message_changed(self, playlist, position, message):
        pass
    
    def subscribers_changed(self, playlist):
        pass



class PlaylistIterator:
    __playlist = None
    __pos = None
    
    def __init__(self, playlist):
        self.__playlist = playlist
        self.__pos = 0
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.__pos < self.__playlist.num_tracks():
            track = self.__playlist.track(self.__pos)
            self.__pos += 1
            return track
        else:
            raise StopIteration



class Playlist:
    _session = None
    _playlist = None
    _callbacks = None
    
    
    def __init__(self, session, playlist):
        self._session = session
        self._playlist = playlist
        self._callbacks = {}
    
    
    @synchronized
    def is_loaded(self):
        return _playlist.is_loaded(self._playlist)
    
    
    @synchronized
    def add_callbacks(self, callbacks):
        cb_id = id(callbacks)
        
        if cb_id in self._callbacks:
            raise DuplicateCallbackError()
        
        else:
            proxy = ProxyPlaylistCallbacks(
                self._session, self, callbacks
            )
            
            struct = proxy.get_callback_struct()
            ptr = ctypes.pointer(struct)
            
            self._callbacks[cb_id] = {
                "struct": struct,
                "ptr": ptr,
                "callbacks": callbacks,
            }
            
            _playlist.add_callbacks(
                self._playlist, ptr, None
            )
    
    
    @synchronized
    def remove_callbacks(self, callbacks):
        cb_id = id(callbacks)
        
        if cb_id not in self._callbacks:
            raise UnknownCallbackError()
        
        else:
            ptr = self._callbacks[cb_id]["ptr"]
            _playlist.remove_callbacks(
                self._playlist, ptr, None
            )
            del self._callbacks[cb_id]
    
    
    def remove_all_callbacks(self):
        for item in self._callbacks:
            self.remove_callbacks(item["callbacks"])
    
    
    @synchronized
    def num_tracks(self):
        return _playlist.num_tracks(self._playlist)
    
    
    @synchronized
    def track(self, index):
        return track.Track(
            self._session,_playlist.track(self._playlist, index)
        )
    
    
    @synchronized
    def name(self):
        return _playlist.name(self._playlist)
    
    
    @synchronized
    def is_in_ram(self):
        return _playlist.is_in_ram(self._session, self._playlist)
    
    
    @synchronized
    def set_in_ram(self, in_ram):
        _playlist.set_in_ram(self._session, self._playlist, in_ram)
    
    
    def __iter__(self):
        return PlaylistIterator(self)
    
    
    def __del__(self):
        self.remove_all_callbacks()
    
    
    def get_struct(self):
        return self._playlist
