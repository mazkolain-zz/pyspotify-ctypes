from _spotify import user as _user

from spotify.utils.decorators import synchronized



class User:
    __user_struct = None
    
    
    @synchronized
    def __init__(self, user_struct):
        self.__user_struct = user_struct
        
        #Ref counting
        _user.add_ref(self.__user_struct)
    
    
    @synchronized
    def canonical_name(self):
        return _user.canonical_name(self.__user_struct)
    
    
    @synchronized
    def display_name(self):
        return _user.display_name(self.__user_struct)
    
    
    @synchronized
    def full_name(self):
        return _user.full_name(self.__user_struct)
    
    
    @synchronized
    def is_loaded(self):
        return _user.is_loaded(self.__user_struct)
    
    
    @synchronized
    def picture(self):
        return _user.picture(self.__user_struct)
    
    
    @synchronized
    def relation_type(self, session):
        return _user.relation_type(session.get_struct(), self.__user_struct)
    
    
    def get_struct(self):
        return self.__user_struct
    
    
    @synchronized
    def __del__(self):
        _user.release(self.__user_struct)
