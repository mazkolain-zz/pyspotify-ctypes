import ctypes

#Import handy globals
from _spotify import libspotify, callback, bool_type


#Structure definitions
class callbacks(ctypes.Structure):
    pass


#Callbacks
cb_playlist_added = callback(
    None,
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p
)

cb_playlist_removed = callback(
    None,
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p
)

cb_playlist_moved = callback(
    None,
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_int, ctypes.c_int,
    ctypes.c_void_p
)

cb_container_loaded = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Completion of structure defs
callbacks._fields_ = [
    ("playlist_added", cb_playlist_added),
    ("playlist_removed", cb_playlist_removed),
    ("playlist_moved", cb_playlist_moved),
    ("container_loaded", cb_container_loaded),
]


add_callbacks = libspotify.sp_playlistcontainer_add_callbacks
add_callbacks.argtypes = [ctypes.c_void_p, ctypes.POINTER(callbacks), ctypes.c_void_p]

remove_callbacks = libspotify.sp_playlistcontainer_remove_callbacks
remove_callbacks.argtypes = [ctypes.c_void_p, ctypes.POINTER(callbacks), ctypes.c_void_p]

num_playlists = libspotify.sp_playlistcontainer_num_playlists
num_playlists.argtypes = [ctypes.c_void_p]
num_playlists.restype = ctypes.c_int

playlist = libspotify.sp_playlistcontainer_playlist
playlist.argtypes = [ctypes.c_void_p, ctypes.c_int]
playlist.restype = ctypes.c_void_p

playlist_type = libspotify.sp_playlistcontainer_playlist_type
playlist_type.argtypes = [ctypes.c_void_p, ctypes.c_int]
playlist_type.restype = ctypes.c_int

playlist_folder_name = libspotify.sp_playlistcontainer_playlist_folder_name
playlist_folder_name.argtypes = [
    ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
]
playlist_folder_name.restype = ctypes.c_int

playlist_folder_id = libspotify.sp_playlistcontainer_playlist_folder_id
playlist_folder_id.argtypes = [ctypes.c_void_p, ctypes.c_int]
playlist_folder_id.restype = ctypes.c_uint64

add_new_playlist = libspotify.sp_playlistcontainer_add_new_playlist
add_new_playlist.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
add_new_playlist.restype = ctypes.c_void_p

add_playlist = libspotify.sp_playlistcontainer_add_playlist
add_playlist.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
add_playlist.restype = ctypes.c_void_p

remove_playlist = libspotify.sp_playlistcontainer_remove_playlist
remove_playlist.argtypes = [ctypes.c_void_p, ctypes.c_int]
remove_playlist.restype = ctypes.c_int

move_playlist = libspotify.sp_playlistcontainer_move_playlist
move_playlist.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, bool_type]
move_playlist.restype = ctypes.c_int

add_folder = libspotify.sp_playlistcontainer_add_folder
add_folder.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
add_folder.restype = ctypes.c_int

owner = libspotify.sp_playlistcontainer_owner
owner.argtypes = [ctypes.c_void_p]
owner.restype = ctypes.c_void_p

add_ref = libspotify.sp_playlistcontainer_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_playlistcontainer_release
release.argtypes = [ctypes.c_void_p]
