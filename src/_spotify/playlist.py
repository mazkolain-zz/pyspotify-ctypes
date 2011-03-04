import ctypes

#Import handy globals
from _spotify import libspotify, callback


#Structure definitions
class callbacks(ctypes.Structure):
    pass


#Callbacks
cb_tracks_added = callback(
    None,
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

cb_tracks_removed = callback(
    None,
    ctypes.c_void_p, ctypes.POINTER(ctypes.c_int),
    ctypes.c_int, ctypes.c_void_p
)

cb_tracks_moved = callback(
    None,
    ctypes.c_void_p, ctypes.POINTER(ctypes.c_int),
    ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

cb_playlist_renamed = callback(None, ctypes.c_void_p, ctypes.c_void_p)
cb_playlist_state_changed = callback(None, ctypes.c_void_p, ctypes.c_void_p)

cb_playlist_update_in_progress = callback(
    None, ctypes.c_void_p, ctypes.c_bool, ctypes.c_void_p
)

cb_playlist_metadata_updated = callback(None, ctypes.c_void_p, ctypes.c_void_p)

cb_track_created_changed = callback(
    None,
    ctypes.c_void_p, ctypes.c_int,
    ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p
)

cb_track_seen_changed = callback(
    None, ctypes.c_void_p, ctypes.c_int, ctypes.c_bool, ctypes.c_void_p
)

cb_description_changed = callback(
    None, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p
)

cb_image_changed = callback(
    None, ctypes.c_void_p, ctypes.POINTER(ctypes.c_byte), ctypes.c_void_p
)

cb_track_message_changed = callback(
    None, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p
)

cb_subscribers_changed = callback(None, ctypes.c_void_p, ctypes.c_void_p)


#Completion of structure defs
callbacks._fields_ = [
   ("tracks_added", cb_tracks_added),
   ("tracks_removed", cb_tracks_removed),
   ("tracks_moved", cb_tracks_moved),
   ("playlist_renamed", cb_playlist_renamed),
   ("playlist_state_changed", cb_playlist_state_changed),
   ("playlist_update_in_progress", cb_playlist_update_in_progress),
   ("playlist_metadata_updated", cb_playlist_metadata_updated),
   ("track_created_changed", cb_track_created_changed),
   ("track_seen_changed", cb_track_seen_changed),
   ("description_changed", cb_description_changed),
   ("image_changed", cb_image_changed),
   ("track_message_changed", cb_track_message_changed),
   ("subscribers_changed", cb_subscribers_changed),
]


#Function prototypes
is_loaded = libspotify.sp_playlist_is_loaded
is_loaded.argtypes = [ctypes.c_void_p]
is_loaded.restype = ctypes.c_bool

add_callbacks = libspotify.sp_playlist_add_callbacks
add_callbacks.argtypes = [
    ctypes.c_void_p, ctypes.POINTER(callbacks), ctypes.c_void_p
]

remove_callbacks = libspotify.sp_playlist_remove_callbacks
remove_callbacks.argtypes = [
    ctypes.c_void_p, ctypes.POINTER(callbacks), ctypes.c_void_p
]

num_tracks = libspotify.sp_playlist_num_tracks
num_tracks.argtypes = [ctypes.c_void_p]
num_tracks.restype = ctypes.c_int

track = libspotify.sp_playlist_track
track.argtypes = [ctypes.c_void_p, ctypes.c_int]
track.restype = ctypes.c_void_p

track_create_time = libspotify.sp_playlist_track_create_time
track_create_time.argtypes = [ctypes.c_void_p, ctypes.c_int]
track_create_time.restype = ctypes.c_int

track_creator = libspotify.sp_playlist_track_creator
track_creator.argtypes = [ctypes.c_void_p, ctypes.c_int]
track_creator.restype = ctypes.c_void_p

track_seen = libspotify.sp_playlist_track_seen 
track_seen.argtypes = [ctypes.c_void_p, ctypes.c_int]
track_seen.restype = ctypes.c_bool

track_set_seen = libspotify.sp_playlist_track_set_seen
track_set_seen.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_bool]
track_set_seen.restype = ctypes.c_int

track_message = libspotify.sp_playlist_track_message
track_message.argtypes = [ctypes.c_void_p, ctypes.c_int]
track_message.restype = ctypes.c_char_p

name = libspotify.sp_playlist_name
name.argtypes = [ctypes.c_void_p]
name.restype = ctypes.c_char_p

rename = libspotify.sp_playlist_rename
rename.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
rename.restype = ctypes.c_int

owner = libspotify.sp_playlist_owner
owner.argtypes = [ctypes.c_void_p]
owner.restype = ctypes.c_void_p

is_collaborative = libspotify.sp_playlist_is_collaborative
is_collaborative.argtypes = [ctypes.c_void_p]
is_collaborative.restype = ctypes.c_bool

set_collaborative = libspotify.sp_playlist_set_collaborative
set_collaborative.argtypes = [ctypes.c_void_p, ctypes.c_bool]

set_autolink_tracks = libspotify.sp_playlist_set_autolink_tracks
set_autolink_tracks.argtypes = [ctypes.c_void_p, ctypes.c_bool]

get_description = libspotify.sp_playlist_get_description
get_description.argtypes = [ctypes.c_void_p]
get_description.restype = ctypes.c_char_p

get_image = libspotify.sp_playlist_get_image
get_image.argtypes = [ctypes.c_void_p, ctypes.c_byte * 20]
get_image.restype = ctypes.c_bool

has_pending_changes = libspotify.sp_playlist_has_pending_changes
has_pending_changes.argtypes = [ctypes.c_void_p]
has_pending_changes.restype = ctypes.c_bool

add_tracks = libspotify.sp_playlist_add_tracks
add_tracks.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
add_tracks.restype = ctypes.c_int

remove_tracks = libspotify.sp_playlist_remove_tracks
remove_tracks.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
remove_tracks.restype = ctypes.c_int

reorder_tracks = libspotify.sp_playlist_reorder_tracks
reorder_tracks.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]
reorder_tracks.restype = ctypes.c_int

num_subscribers = libspotify.sp_playlist_num_subscribers
num_subscribers.argtypes = [ctypes.c_void_p]
num_subscribers.restype = ctypes.c_uint

subscribers = libspotify.sp_playlist_subscribers
subscribers.argtypes = [ctypes.c_void_p]
subscribers.restype = ctypes.c_void_p

subscribers_free = libspotify.sp_playlist_subscribers_free
subscribers_free.argtypes = [ctypes.c_void_p]

update_subscribers = libspotify.sp_playlist_update_subscribers
update_subscribers.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

is_in_ram = libspotify.sp_playlist_is_in_ram
is_in_ram.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
is_in_ram.restype = ctypes.c_bool

set_in_ram = libspotify.sp_playlist_set_in_ram
set_in_ram.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool]

create = libspotify.sp_playlist_create
create.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
create.restype = ctypes.c_void_p

add_ref = libspotify.sp_playlist_add_ref
add_ref.argtypes = [ctypes.c_void_p]

release = libspotify.sp_playlist_release
release.argtypes = [ctypes.c_void_p]
