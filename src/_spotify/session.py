import ctypes
import _spotify

#Import handy globals
from _spotify import LibSpotifyInterface, callback, bool_type


#Structure definitions
class callbacks(ctypes.Structure):
    pass

class config(ctypes.Structure):
    pass

class offline_sync_status(ctypes.Structure):
    pass


#Callbacks
cb_logged_in = callback(None, ctypes.c_void_p, ctypes.c_int)
cb_logged_out = callback(None, ctypes.c_void_p)
cb_metadata_updated = callback(None, ctypes.c_void_p)
cb_connection_error = callback(None, ctypes.c_void_p, ctypes.c_int)
cb_message_to_user = callback(None, ctypes.c_void_p, ctypes.c_char_p)
cb_notify_main_thread = callback(None, ctypes.c_void_p)

cb_music_delivery = callback(
    ctypes.c_int,
    ctypes.c_void_p, ctypes.POINTER(_spotify.audioformat),
    ctypes.c_void_p, ctypes.c_int
)

cb_play_token_lost = callback(None, ctypes.c_void_p)
cb_log_message = callback(None, ctypes.c_void_p, ctypes.c_char_p)
cb_end_of_track = callback(None, ctypes.c_void_p)
cb_streaming_error = callback(None, ctypes.c_void_p, ctypes.c_int)
cb_userinfo_updated = callback(None, ctypes.c_void_p)
cb_start_playback = callback(None, ctypes.c_void_p)
cb_stop_playback = callback(None, ctypes.c_void_p)

cb_get_audio_buffer_stats = callback(
    None, ctypes.c_void_p, ctypes.POINTER(_spotify.audio_buffer_stats)
)

cb_offline_status_updated = callback(None, ctypes.c_void_p)


#Completion of structure defs
callbacks._fields_ = [
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
    ("streaming_error", cb_streaming_error),
    ("userinfo_updated", cb_userinfo_updated),
    ("start_playback", cb_start_playback),
    ("stop_playback", cb_stop_playback),
    ("get_audio_buffer_stats", cb_get_audio_buffer_stats),
    ("offline_status_updated", cb_offline_status_updated)
]

config._fields_ = [
    ("api_version", ctypes.c_int),
    ("cache_location", ctypes.c_char_p),
    ("settings_location", ctypes.c_char_p),
    ("application_key", ctypes.POINTER(ctypes.c_byte)),
    ("application_key_size", ctypes.c_uint),
    ("user_agent", ctypes.c_char_p),
    ("callbacks", ctypes.POINTER(callbacks)),
    ("userdata", ctypes.c_void_p),
    ("compress_playlists", bool_type),
    ("dont_save_metadata_for_playlists", bool_type),
    ("initially_unload_playlists", bool_type),
]

offline_sync_status._fields_ = [
    ("queued_tracks", ctypes.c_int),
    ("done_tracks", ctypes.c_int),
    ("copied_tracks", ctypes.c_int),
    ("willnotcopy_tracks", ctypes.c_int),
    ("error_tracks", ctypes.c_int),
    ("syncing", bool_type)
]



#Low level function interface
class SessionInterface(LibSpotifyInterface):
    def __init__(self):
        LibSpotifyInterface.__init__(self)
        
        self._register_func(
            'create',
            'sp_session_create',
            ctypes.c_int,
            ctypes.POINTER(config), ctypes.POINTER(ctypes.c_void_p)
        )
        
        self._register_func(
            'release',
            'sp_session_release',
            None,
            ctypes.c_void_p
        )
        
        self._register_func(
            'login',
            "sp_session_login",
            None,
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, bool_type
        )
        
        self._register_func(
            'relogin',
            "sp_session_relogin",
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'remembered_user',
            'sp_session_remembered_user',
            ctypes.c_int,
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
        )
        
        self._register_func(
            'forget_me',
            'sp_session_forget_me',
            None,
            ctypes.c_void_p
        )
        
        self._register_func(
            'user',
            'sp_session_user',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'logout',
            "sp_session_logout",
            None,
            ctypes.c_void_p
        )
        
        self._register_func(
            'connectionstate',
            'sp_session_connectionstate',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'userdata',
            'sp_session_userdata',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'set_cache_size',
            'sp_session_set_cache_size',
            None,
            ctypes.c_void_p, ctypes.c_size_t
        )
        
        self._register_func(
            'process_events',
            'sp_session_process_events',
            None,
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)
        )
        
        self._register_func(
            'player_load',
            'sp_session_player_load',
            ctypes.c_int,
            ctypes.c_void_p, ctypes.c_void_p
        )
        
        self._register_func(
            'player_seek',
            'sp_session_player_seek',
            None,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'player_play',
            'sp_session_player_play',
            None,
            ctypes.c_void_p, bool_type
        )
        
        self._register_func(
            'player_unload',
            'sp_session_player_unload',
            None,
            ctypes.c_void_p
        )
        
        self._register_func(
            'player_prefetch',
            'sp_session_player_prefetch',
            ctypes.c_int,
            ctypes.c_void_p, ctypes.c_void_p
        )
        
        self._register_func(
            'playlistcontainer',
            'sp_session_playlistcontainer',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'inbox_create',
            'sp_session_inbox_create',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'starred_create',
            'sp_session_starred_create',
            ctypes.c_void_p,
            ctypes.c_void_p
        )
        
        self._register_func(
            'starred_for_user_create',
            'sp_session_starred_for_user_create',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_char_p
        )
        
        self._register_func(
            'publishedcontainer_for_user_create',
            'sp_session_publishedcontainer_for_user_create',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_char_p
        )
        
        self._register_func(
            'preferred_bitrate',
            'sp_session_preferred_bitrate',
            None,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'preferred_offline_bitrate',
            'sp_session_preferred_offline_bitrate',
            None,
            ctypes.c_void_p, ctypes.c_int, bool_type
        )
        
        self._register_func(
            'num_friends',
            'sp_session_num_friends',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'friend',
            'sp_session_friend',
            ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'set_connection_type',
            'sp_session_set_connection_type',
            None,
            ctypes.c_void_p, ctypes.c_int
        )
        
        self._register_func(
            'set_connection_rules',
            'sp_session_set_connection_rules',
            None,
            ctypes.c_void_p, ctypes.c_int
        )
        
        #Mmmm, shouldn't these ones be sp_session_offline*
        self._register_func(
            'offline_tracks_to_sync',
            'sp_offline_tracks_to_sync',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'offline_num_playlists',
            'sp_offline_num_playlists',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'offline_sync_get_status',
            'sp_offline_sync_get_status',
            bool_type,
            ctypes.c_void_p, ctypes.POINTER(offline_sync_status)
        )
        
        self._register_func(
            'offline_time_left',
            'sp_offline_time_left',
            ctypes.c_int,
            ctypes.c_void_p
        )
        
        self._register_func(
            'user_country',
            'sp_session_user_country',
            ctypes.c_int,
            ctypes.c_void_p
        )
