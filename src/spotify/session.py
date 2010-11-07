import ctypes

#Import low level session api
from _spotify import session as _session

#Libspotify instance available globally
from _spotify import libspotify

import spotify
from spotify import user



#classes
class Session:
    api_version = 6
    
    def __init__(self, manager, cache_location=None, settings_location=None, app_key=None, user_agent=None):
        #prepare callbacks
        callbacks = _session.callbacks(
            _session.cb_logged_in(manager.logged_in),
            _session.cb_logged_out(manager.logged_out),
            _session.cb_metadata_updated(manager.metadata_updated),
            _session.cb_connection_error(manager.connection_error),
            _session.cb_message_to_user(manager.message_to_user),
            _session.cb_notify_main_thread(manager.notify_main_thread),
            _session.cb_music_delivery(manager.music_delivery),
            _session.cb_play_token_lost(manager.play_token_lost),
            _session.cb_log_message(manager.log_message),
            _session.cb_end_of_track(manager.end_of_track),
        )
        
        #initialize app config
        config = _session.config(
            self.api_version,
            cache_location,
            settings_location,
            app_key,
            ctypes.sizeof(app_key),
            user_agent,
            callbacks,
            None
        )
        
        sess_p = ctypes.c_void_p
        _session.create(config, sess_p)
        self._session = sess_p
    
    
    def __del__(self):
        _session.release(self._session)
    
    
    def _handle_sp_error(self, errorcode):
        if errorcode != 0:
            msg = libspotify.sp_error_message(errorcode)
            raise spotify.LibSpotifyError(msg)
    
    
    def login(self, username, password):
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
    
    def process_events(self):
        next_timeout = 0
        _session.process_events(self._session, next_timeout)
        return next_timeout
    
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
