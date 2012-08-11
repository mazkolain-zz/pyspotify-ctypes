'''
Created on 11/08/2012

@author: mazkolain
'''
import spotify
import spotify.albumbrowse



class LoadAlbumCallback(spotify.albumbrowse.AlbumbrowseCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def albumbrowse_complete(self, artistbrowse):
        self.__checker.check_conditions()



def load_albumbrowse(session, album, timeout=5, ondelay=None):
    #Check a valid number on timeout
    if timeout <= 1:
        raise ValueError('Timeout value must be higher than one second.')
    
    checker = spotify.BulkConditionChecker()
    cb = LoadAlbumCallback(checker)
    albumbrowse = spotify.albumbrowse.Albumbrowse(session, album, cb)
    
    def is_loaded():
        return albumbrowse.is_loaded()
    
    #If it's already loaded
    if is_loaded():
        return albumbrowse
    
    #Otherwise we'll have to wait
    else:
        
        #Add the wait condition
        checker.add_condition(is_loaded)
        
        #Let's see what happens within a second...
        if checker.try_complete_wait(1):
            return albumbrowse
        
        #We need to wait more time
        else:
            
            #Notify outside code about the delay
            if ondelay is not None:
                ondelay()
            
            #Now try again with the rest of the timeout
            checker.complete_wait(timeout - 1)
            
            return albumbrowse
