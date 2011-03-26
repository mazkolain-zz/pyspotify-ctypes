import ctypes

#Import low level session api
from _spotify import session as _session

#Libspotify instance available globally
from _spotify import libspotify

import spotify
from spotify import user

import threading



#classes
class Session:
    api_version = 7
    _manager = None
    _main_lock = None
    
    #Instance variable to avoid them getting garbage collected
    _callbacks = None
    
    
    def __init__(self, manager, cache_location="", settings_location="", app_key=None, user_agent=None):
        self._manager = manager
        self._main_lock = threading.Lock()
        
        #prepare callbacks
        self._callbacks = _session.callbacks(
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
            ctypes.pointer(self._callbacks),
            ctypes.c_void_p(),
            1,
            0,
            1,
        )
        
        self._session = ctypes.c_void_p()
        err = _session.create(ctypes.byref(config), ctypes.byref(self._session))
        self._handle_sp_error(err)
    
    
    def __del__(self):
        _session.release(self._session)
    
    
    def _handle_sp_error(self, errorcode):
        if errorcode != 0:
            msg = libspotify.sp_error_message(errorcode)
            raise spotify.LibSpotifyError(msg)
    
    
    def login(self, username, password):
        with self._main_lock:
            self._handle_sp_error(
               _session.login(self._session, username, password)
            )
    
    def user(self):
        return user.User(
            libspotify, _session.user(self._session)
        )
    
    
    def logout(self):
        self._handle_sp_error(
            _session.logout(self._session)
        )
    
    def connectionstate(self):
        return _session.connectionstate(self._session)
    
    def userdata(self):
        return _session.userdata(self._session)
    
    def set_cache_size(self, size):
        _session.set_cache_size(size)
    
    def process_events(self):
        with self._main_lock:
            next_timeout = ctypes.c_int(0)
            _session.process_events(self._session, ctypes.byref(next_timeout))
    
    def player_load(self, track):
        pass
    
    def player_seek(self, offset):
        pass
    
    def player_play(self, play):
        pass
    
    def player_unload(self):
        pass
    
    def playlistcontainer(self):
        pass
    
    #Callback proxies
    def _logged_in(self, session, error):
        self._manager.logged_in(self, error)
    
    def _logged_out(self, session):
        self._manager.logged_out(self)
    
    def _metadata_updated(self, session):
        self._manager.metadata_updated(self)
    
    def _connection_error(self, session, error):
        self._manager.connection_error(self, error)
    
    def _message_to_user(self, session, message):
        self._manager.message_to_user(self, message)
    
    def _notify_main_thread(self, session):
        self.process_events()
    
    def _music_delivery(self, session, format, frames, num_frames):
        self._manager.music_delivery(self, format, frames, num_frames)
    
    def _play_token_lost(self, session):
        self._manager.play_token_lost(self)
    
    def _log_message(self, session, data):
        self._manager.log_message(self, data)
    
    def _end_of_track(self, session, error):
        self._manager.end_of_track(self, error)
    
    def _streaming_error(self, session, error):
        self._manager.streaming_error(self, error)
    
    def _userinfo_updated(self, session):
        self._manager.userinfo_updated(self)
    
    def _start_playback(self, session):
        self._manager.start_playback(self)
    
    def _stop_playback(self, session):
        self._manager.stop_playback(self)
    
    def _get_audio_buffer_stats(self, session, stats):
        self._manager.get_audio_buffer_stats(self, stats)
