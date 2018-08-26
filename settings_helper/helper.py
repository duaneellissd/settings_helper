
import copy
from .callbacks import *
from .tool import global_settings
from frozenclass import FrozenClass

__all__=['SettingsHelper']

MAGIC_NONE_STRING='__NONE__'

@FrozenClass
class SettingsHelper( SettingsCallbacks ):
    def __init__(self, section, default_values, auto_register = True ):
        '''
        section - is the section name save to in the config file.
        default_values - must be a dict of name value pairs

        The section name must be unique across the application.
        '''
        SettingsCallbacks.__init__(self)
        
        # remember the prefix for later
        self._section = section

        # Remember these settings for later.
        if auto_register:
            global global_settings
            global_settings.register( self )
        else:
            # The user must regiser them with the SettingsTool()
            # on their own, it's not done automatically
            pass

        # Set our defaults, we'll use the keys later.
        self._default_values = copy.deepcopy( default_values )
        
        for name,value in self._default_values.items():
            setattr( self, name,value )

    def _load_before_open(self, filename):
        '''
        This is an override method for the owner.
        It is called before the config file is opened.
        '''
        pass
    
    def _load_after_close(self, filename):
        '''
        This is an override method for the owner.
        It is called after the config file is closed.
        '''
        pass

    def _factory_default(self):
        '''
        Restore these settings to their factory defaults
        '''
        for name, value in self._default_values.items():
            setattr( self,name,value)
    
    def _to_dict(self):
        '''
        called during save(), converts settings to a dict
        that dict is then saved via a ConfigFile (.ini file)
        '''
        result = dict()
        for name, value in self._default_values.items():
            # get current value
            value = getattr( self, name )
            # translate magic values
            if value == None:
                value = MAGIC_NONE_STRING
            # We can only save strings to the config file
            assert( isinstance( value, (str, int, float, bool)))
            result[name] = str(value)
        return result
    
    def _from_dict(self,d):
        '''
        called during load(), the file has been read and the [section] name 
        matches, this dict contains values for this class, this puts
        the values away.
        '''
        for name, new_value in d.items():
            # if the name is unknown..
            if not hasattr( self, name ):
                # let app override handling of this.
                self._unknown_setting( self._section, name, new_value )
                continue
            # Translate magic values
            if new_value.strip() == MAGIC_NONE_STRING:
                value = None
            else:
                    # Get the old value
                    old_value = getattr( self, name )
                    # And convert the file content (which could be a string)
                    # into the runtime content (which might be an integer)
                    new_value = old_value.__class__(new_value)
            setattr( self, name, new_value )
