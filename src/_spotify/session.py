from ctypes import *

#structure definitions
class sp_audioformat(Structure):
    pass

class sp_session_callbacks(Structure):
    pass

class sp_session_config(Structure):
    pass


#Callbacks
cb_logged_in = WINFUNCTYPE(None, c_void_p, c_int)
cb_logged_out = WINFUNCTYPE(None, c_void_p)
cb_metadata_updated = WINFUNCTYPE(None, c_void_p)
cb_connection_error = WINFUNCTYPE(None, c_int)
cb_message_to_user = WINFUNCTYPE(None, c_char_p)
cb_notify_main_thread = WINFUNCTYPE(None, c_void_p)
cb_music_delivery = WINFUNCTYPE(c_int, POINTER(sp_audioformat), c_void_p, c_int)
cb_play_token_lost = WINFUNCTYPE(None, c_void_p)
cb_log_message = WINFUNCTYPE(None, c_void_p, c_char_p)
cb_end_of_track = WINFUNCTYPE(None, c_void_p)

#Above callback proxies
def cb_proxy_logged_in():
    pass

def cb_proxy_logged_out():
    pass


#completion of types
sp_audioformat._fields = [
    ("sample_type", c_int),
    ("sample_rate", c_int),
    ("channels", c_int),
]

sp_session_callbacks._fields_ = [
    ("logged_in", cb_logged_in),
    ("logged_out", cb_logged_out),
    ("metadata_updated", cb_metadata_updated),
    ("connection_error", cb_connection_error),
    ("message_to_user", cb_message_to_user),
    ("notify_main_thread", cb_notify_main_thread),
    ("music_delivery", cb_music_delivery),
    ("play_token_lost", cb_play_token_lost),
    ("log_message", cb_log_message),
    ("end_of_track", cb_end_of_track),
]

sp_session_config._fields_ = [
    ("api_version", c_int),
    ("cache_location", c_char_p),
    ("settings_location", c_char_p),
    ("application_key", c_void_p),
    ("application_key_size", c_uint),
    ("user_agent", c_char_p),
    ("callbacks", sp_session_callbacks),
    ("userdata", c_void_p),
]





class LibSpotifyError(Exception):
    def __init__(self, msg):
        self.msg = msg


#classes
class Session:
    api_version = 3
    
    def __init__(self, manager, cache_location=None, settings_location=None, app_key=None, user_agent=None):
        #load the spotify lib
        self.libspotify = WinDLL("libspotify")
        
        #prepare callbacks
        callbacks = sp_session_callbacks(
            cb_logged_in(manager.logged_in),
            cb_logged_out(manager.logged_out),
            cb_metadata_updated(manager.metadata_updated),
            cb_connection_error(manager.connection_error),
            cb_message_to_user(manager.message_to_user),
            cb_notify_main_thread(manager.notify_main_thread),
            cb_music_delivery(manager.music_delivery),
            cb_play_token_lost(manager.play_token_lost),
            cb_log_message(manager.log_message),
            cb_end_of_track(manager.end_of_track),
        )
        
        #initialize app config
        config = sp_session_config(
            self.api_version,
            cache_location,
            settings_location,
            app_key,
            sizeof(app_key),
            user_agent,
            callbacks,
            None
        )
        
        sess_p = c_void_p
        self._libspotify.sp_session_init(config, sess_p)
        self._session = sess_p
    
    
    def _handle_sp_error(self, errorcode):
        if errorcode != 0:
            msg = self._libspotify.sp_error_message(errorcode)
            raise LibSpotifyError(msg)
    
    
    def login(self, username, password):
        self._handle_sp_error(
            self._libspotify.sp_session_login(self._session, username, password)
        )
    
    
    def user(self):
        pass
    
    
    def logout(self):
        self._handle_sp_error(
            self._libspotify.sp_session_logout(self._session)
        )
    
    def connectionstate(self):
        pass
    
    def userdata(self):
        pass
    
    def process_events(self):
        pass
    
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
