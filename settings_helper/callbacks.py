
from frozenclass import FrozenClass
from .exceptions import *

__all__=['SettingsCallbacks']

@FrozenClass
class SettingsCallbacks( object ):
    '''
    This is a list of callbacks usedby both the SettingsTool() and SettingsHelper() classes.
    '''
    def __init__(self):
        pass

    def _save_before_open(self,filename):
        '''
        Hook: Call when saveing, before the filename is opened.
        '''
        pass

    def _save_after_close(self,filename):
        '''
        Hook: Call when saving, after the filename is written and closed.
        '''
        pass

    def _load_before_open( self, filename ):
        '''
        Hook: Called when loading, before opening the filename
        '''
        pass

    def _load_after_close( self, filename ):
        '''
        Hook: Called when loading, after closing the filename
        '''
        pass

    def _unknown_setting( self, section, name, value ):
        '''
        While loading an uknown setting has been found.

        This can happen if the saved settings come from a different
        version of the application and the settings names have changed.

        The default action is to raise an exception.

        To handle the issue yourself, just do so, then return from the function.
        '''
        if name == None:
            e = SettingUnknown( "unknown setting: [%s] section" % name )
        else:
            e = SettingUnknown( "unknown setting: [%s] %s=%s" % (section,name,value))
        e.section = section
        e.name = name
        e.value = value
        raise(e)
