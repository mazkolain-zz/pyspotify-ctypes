import ctypes
import _spotify

#Import handy globals
from _spotify import libspotify, callback


#Structure definitions
class callbacks(ctypes.Structure):
    pass

class config(ctypes.Structure):
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
    ("compress_playlists", ctypes.c_bool),
    ("dont_save_metadata_for_playlists", ctypes.c_bool),
    ("initially_unload_playlists", ctypes.c_bool),
]


#Function declarations
create = _spotify.libspotify.sp_session_create
create.argtypes = [ctypes.POINTER(config), ctypes.POINTER(ctypes.c_void_p)]
create.restype = ctypes.c_int

release = libspotify.sp_session_release
release.argtypes = [ctypes.c_void_p]

login = libspotify.sp_session_login
login.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

user = libspotify.sp_session_user
user.argtypes = [ctypes.c_void_p]
user.restype = ctypes.c_void_p

logout = libspotify.sp_session_logout
logout.argtypes = [ctypes.c_void_p]

connectionstate = libspotify.sp_session_connectionstate
connectionstate.argtypes = [ctypes.c_void_p]
connectionstate.restype = ctypes.c_int

userdata = libspotify.sp_session_userdata
userdata.argtypes = [ctypes.c_void_p]
userdata.restype = ctypes.c_void_p

set_cache_size = libspotify.sp_session_set_cache_size
set_cache_size.argtypes = [ctypes.c_void_p, ctypes.c_size_t]

process_events = libspotify.sp_session_process_events
process_events.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]

player_load = libspotify.sp_session_player_load
player_load.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
player_load.restype = ctypes.c_int

player_seek = libspotify.sp_session_player_seek
player_seek.argtypes = [ctypes.c_void_p, ctypes.c_int]

player_play = libspotify.sp_session_player_play
player_play.argtypes = [ctypes.c_void_p, ctypes.c_bool]

player_unload = libspotify.sp_session_player_unload
player_unload.argtypes = [ctypes.c_void_p]

player_prefetch = libspotify.sp_session_player_prefetch
player_prefetch.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
player_prefetch.restype = ctypes.c_int

playlistcontainer = libspotify.sp_session_playlistcontainer
playlistcontainer.argtypes = [ctypes.c_void_p]
playlistcontainer.restype = ctypes.c_void_p

inbox_create = libspotify.sp_session_inbox_create
inbox_create.argtypes = [ctypes.c_void_p]
inbox_create.restype = ctypes.c_void_p

starred_create = libspotify.sp_session_starred_create
starred_create.argtypes = [ctypes.c_void_p]
starred_create.restype = ctypes.c_void_p

starred_for_user_create = libspotify.sp_session_starred_for_user_create
starred_for_user_create.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
starred_for_user_create.restype = ctypes.c_void_p

publishedcontainer_for_user_create = libspotify.sp_session_publishedcontainer_for_user_create
publishedcontainer_for_user_create.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
publishedcontainer_for_user_create.restype = ctypes.c_void_p

#Gone since 0.6?
#publishedcontainer_for_user_release = libspotify.sp_session_publishedcontainer_for_user_release
#publishedcontainer_for_user_release.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

preferred_bitrate = libspotify.sp_session_preferred_bitrate
preferred_bitrate.argtypes = [ctypes.c_void_p, ctypes.c_int]

num_friends = libspotify.sp_session_num_friends
num_friends.argtypes = [ctypes.c_void_p]
num_friends.restype = ctypes.c_int

friend = libspotify.sp_session_friend
friend.argtypes = [ctypes.c_void_p, ctypes.c_int]
friend.restype = ctypes.c_void_p
