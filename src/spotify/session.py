import ctypes

#Import low level api
from _spotify import session as _session

#Import general classes from the high level module
import spotify

#Also import this one's siblings
from spotify import user, playlistcontainer, playlist, handle_sp_error

#Decorators
from spotify.utils.decorators import synchronized



class ProxySessionCallbacks:
    __session = None
    __callbacks = None
    __manager = None
    __struct = None
    
    
    def __init__(self, session, callbacks, manager):
        self.__session = session
        self.__callbacks = callbacks
        self.__manager = manager
        self.__struct = _session.callbacks(
            _session.cb_logged_in(self._logged_in),
            _session.cb_logged_out(self._logged_out),
            _session.cb_metadata_updated(self._metadata_updated),
            _session.cb_connection_error(self._connection_error),
            _session.cb_message_to_user(self._message_to_user),
            _session.cb_notify_main_thread(self._notify_main_thread),
            _session.cb_music_delivery(self._music_delivery),
            _session.cb_play_token_lost(self._play_token_lost),
            _session.cb_log_message(self._log_message),
            _session.cb_end_of_track(self._end_of_track),
            _session.cb_streaming_error(self._streaming_error),
            _session.cb_userinfo_updated(self._userinfo_updated),
            _session.cb_start_playback(self._start_playback),
            _session.cb_stop_playback(self._stop_playback),
            _session.cb_get_audio_buffer_stats(self._get_audio_buffer_stats),
        )
    
    @synchronized
    def _logged_in(self, session, error):
        self.__callbacks.logged_in(self.__session, error)
        self.__manager.logged_in(self.__session, error)
    
    
    @synchronized
    def _logged_out(self, session):
        self.__callbacks.logged_out(self.__session)
        self.__manager.logged_out(self.__session)
    
    
    @synchronized
    def _metadata_updated(self, session):
        self.__callbacks.metadata_updated(self.__session)
        self.__manager.metadata_updated(self.__session)
    
    
    @synchronized
    def _connection_error(self, session, error):
        self.__callbacks.connection_error(self.__session, error)
        self.__manager.connection_error(self.__session, error)
    
    
    @synchronized
    def _message_to_user(self, session, message):
        self.__callbacks.message_to_user(self.__session, message)
        self.__manager.message_to_user(self.__session, message)
    
    
    def _notify_main_thread(self, session):
        #Not synchronized, also nonblocking:
        self.__callbacks.notify_main_thread(self.__session)
        self.__manager.notify_main_thread(self.__session)
    
    
    def _music_delivery(self, session, format, frames, num_frames):
        if synchronized.get_lock().acquire(False):
            res = self.__callbacks.music_delivery(self.__session, format, frames, num_frames)
            synchronized.get_lock().release()
            return res
        else:
            return 0
    
    
    @synchronized
    def _play_token_lost(self, session):
        self.__callbacks.play_token_lost(self.__session)
        self.__manager.play_token_lost(self.__session)
    
    
    @synchronized
    def _log_message(self, session, data):
        self.__callbacks.log_message(self.__session, data)
        self.__manager.log_message(self.__session, data)
    
    
    @synchronized
    def _end_of_track(self, session, error):
        self.__callbacks.end_of_track(self.__session, error)
        self.__manager.end_of_track(self.__session, error)
    
    
    @synchronized
    def _streaming_error(self, session, error):
        self.__callbacks.streaming_error(self.__session, error)
        self.__manager.streaming_error(self.__session, error)
    
    
    @synchronized
    def _userinfo_updated(self, session):
        self.__callbacks.userinfo_updated(self.__session)
        self.__manager.userinfo_updated(self.__session)
    
    
    @synchronized
    def _start_playback(self, session):
        self.__callbacks.start_playback(self.__session)
        self.__manager.start_playback(self.__session)
    
    
    @synchronized
    def _stop_playback(self, session):
        self.__callbacks.stop_playback(self.__session)
        self.__manager.stop_playback(self.__session)
    
    
    @synchronized
    def _get_audio_buffer_stats(self, session, stats):
        self.__manager.get_audio_buffer_stats(self.__session, stats)

    
    def get_callback_struct(self):
        return self.__struct



class SessionCallbacks:
    def logged_in(self, session, error):
        pass
    
    def logged_out(self, session):
        pass
    
    def metadata_updated(self, session):
        pass
    
    def connection_error(self, session, error):
        pass
    
    def message_to_user(self, session, message):
        pass
    
    def notify_main_thread(self, session):
        pass
    
    def music_delivery(self, format, frames, num_frames):
        pass
    
    def play_token_lost(self, session):
        pass
    
    def log_message(self, session, message):
        pass
    
    def end_of_track(self, session, error):
        pass
    
    def userinfo_updated(self, session):
        pass
    
    def start_playback(self, session):
        pass
    
    def stop_playback(self, session):
        pass
    
    def get_audio_buffer_stats(self, session, stats):
        pass



#classes
class Session:
    api_version = 7
    
    __session = None
    
    __proxy_callbacks = None
    __callback_manager = None
    
    _user_callbacks = None
    _metadata_callbacks = None
    
    #Playlistcontainer instance
    _playlistcontainer = None
    
    
    def __init__(self, callbacks, cache_location="", settings_location="", app_key=None, user_agent=None):
        #Callback managers
        self._user_callbacks = spotify.CallbackQueueManager()
        self._metadata_callbacks = spotify.CallbackQueueManager()
        
        #prepare callbacks
        self.__callback_manager = spotify.CallbackManager()
        self.__callbacks = ProxySessionCallbacks(
            self, callbacks, self.__callback_manager
        )
        
        #app key conversion
        appkey_type = ctypes.c_byte * len(app_key)
        appkey_c = appkey_type.from_buffer(bytearray(app_key))
        
        #initialize app config
        config = _session.config(
            self.api_version,
            cache_location,
            settings_location,
            appkey_c,
            ctypes.sizeof(appkey_c),
            user_agent,
            ctypes.pointer(self.__callbacks.get_callback_struct()),
            ctypes.c_void_p(),
            1,
            0,
            1,
        )
        
        self.__session = ctypes.c_void_p()
        err = _session.create(ctypes.byref(config), ctypes.byref(self.__session))
        spotify.handle_sp_error(err)
    
    
    def add_callbacks(self, callbacks):
        self.__callback_manager.add_callbacks(callbacks)
    
    
    def remove_callbacks(self, callbacks):
        self.__callback_manager.remove_callbacks(callbacks)
    
    
    @synchronized
    def login(self, username, password):
        _session.login(self.__session, username, password)
    
    
    @synchronized
    def user(self, onload=None):
        user_obj = user.User(self.__session, _session.user(self.__session))
            
        if onload != None:
            self._user_callbacks.add_callback(
                user_obj.is_loaded, onload, user_obj
            )
                
        return user_obj
    
    
    @synchronized
    def logout(self):
        _session.logout(self.__session)
    
    
    @synchronized
    def connectionstate(self):
        return _session.connectionstate(self.__session)
    
    
    @synchronized
    def userdata(self):
        return _session.userdata(self.__session)
    
    
    @synchronized
    def set_cache_size(self, size):
        _session.set_cache_size(size)
    
    
    @synchronized
    def process_events(self):
        next_timeout = ctypes.c_int(0)
        _session.process_events(self.__session, ctypes.byref(next_timeout))
        return next_timeout.value / 1000
        
    
    @synchronized
    def player_load(self, track):
        handle_sp_error(
            _session.player_load(self.__session, track.get_struct())
        )
    
    
    @synchronized
    def player_seek(self, offset):
        _session.player_seek(self.__session, offset)
    
    
    @synchronized
    def player_play(self, play):
        _session.player_play(self.__session, play)
    
    
    @synchronized
    def player_unload(self):
        _session.player_unload(self.__session)
    
    
    @synchronized
    def player_prefetch(self, track):
        handle_sp_error(
            _session.player_prefetch(self.__session, track.get_struct())
        )
    
    
    @synchronized
    def playlistcontainer(self):
        if self._playlistcontainer is None:
            self._playlistcontainer = playlistcontainer.PlaylistContainer(
                _session.playlistcontainer(self.__session),
            )
        
        return self._playlistcontainer
    
    
    @synchronized
    def inbox_create(self):
        return playlist.Playlist(_session.inbox_create(self.__session))
    
    
    @synchronized
    def starred_create(self):
        return playlist.Playlist(_session.starred_create(self.__session))
    
    
    @synchronized
    def starred_for_user_create(self, canonical_username):
        return playlist.Playlist(
            _session.starred_for_user_create(
                self.__session, canonical_username
            )
        )
    
    
    @synchronized
    def publishedcontainer_for_user_create(self, canonical_username):
        return playlistcontainer.PlaylistContainer(
            _session.publishedcontainer_for_user_create(
                self.__session, canonical_username
            )
        )
    
    
    @synchronized
    def preferred_bitrate(self, bitrate):
        _session.preferred_bitrate(self.__session, bitrate)
    
    
    @synchronized
    def num_friends(self):
        return _session.num_friends(self.__session)
    
    
    @synchronized
    def friend(self, index):
        return user.User(
            _session.friend(self.__session, index)
        )
    
    
    @synchronized
    def get_struct(self):
        return self.__session
    
    
    @synchronized
    def __del__(self):
        _session.release(self.__session)
