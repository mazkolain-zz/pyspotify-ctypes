from _spotify import user as _user

from spotify.utils.decorators import synchronized, extract_args

from spotify.utils.finalize import track_for_finalization



@extract_args
@synchronized
def _finalize_user(user_interface, user_struct):
    user_interface.release(user_struct)
    print "user __del__ called"



class User:
    __user_struct = None
    __user_interface = None
    
    
    @synchronized
    def __init__(self, user_struct):
        self.__user_struct = user_struct
        self.__user_interface = _user.UserInterface()
        
        #Ref counting
        self.__user_interface.add_ref(self.__user_struct)
        
        #register finalizers
        args = (self.__user_interface, self.__user_struct)
        track_for_finalization(self, args, _finalize_user)
    
    
    @synchronized
    def canonical_name(self):
        return self.__user_interface.canonical_name(self.__user_struct)
    
    
    @synchronized
    def display_name(self):
        return self.__user_interface.display_name(self.__user_struct)
    
    
    @synchronized
    def is_loaded(self):
        return self.__user_interface.is_loaded(self.__user_struct)
        self.__user_interface.release(self.__user_struct)
    
    
    def get_struct(self):
        return self.__user_struct
