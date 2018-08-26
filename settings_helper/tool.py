
from frozenclass import FrozenClass
from .callbacks import *
from .exceptions import *

__all__=['SettingsTool', 'global_settings' ]

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


@FrozenClass
class SettingsTool(SettingsCallbacks):
    '''
    This tool class can save & load settings to/from an 'ini' file.
    '''
    def __init__(self):
        SettingsCallbacks.__init__(self)
        self.all_settings = dict()

    def register( self, settings ):
        '''
        Add this item to the list of settings managed by this tool instance.
        '''
        if settings._section in self.all_settings:
            SettingsError( "duplicate settings key: %s" % settings._section )
        self.all_settings[ settings._section ] = settings

    def factory_defaults( self ):
        '''
        Restore all settings to their default value
        '''
        for name,klass in self.all_settings.items():
            klass._factory_default()
        
    def save_to_ini( self, filename ):
        '''
        Save settings to an INI file via ConfigParser()
        '''

        # Prep
        self._save_before_open(filename)

        for name, klass in self.all_settings.items():
            klass._save_before_open( filename )

        # create config
        config = ConfigParser()

        # Go fetch data
        for name, klass in self.all_settings.items():
            config[ name ] = klass._to_dict()

        # Save to file
        with open( filename,'w' ) as configfile:
            config.write( configfile )

        # Fini
        for name, klass in self.all_settings.items():
            klass._save_after_close( filename )

        self._save_after_close(filename)
    
    def load_from_ini( self, filename ):
        '''
        Load settings from an INI file via ConfigParser()
        '''

        self._load_before_open(filename)

        # Setup
        for prefix, settings in self.all_settings.items():
            settings._load_before_open(filename)

        # open and read
        config = ConfigParser()
        config.read( filename )

        # put away
        for section in config.sections():
            sklass = self.all_settings.get( section, None )
            if sklass is None:
                self._unknown_setting( section, None, None )
                continue
            sklass._from_dict( config[section] )

        # "close()" does not really happen
        # so we fake it.
        pass

        # Tell clients
        for prefix, settings in self.all_settings.items():
            settings._load_after_close(filename)

        self._load_after_close( filename )

        

'''
Global that holds all known settings in the application'
'''
global_settings = SettingsTool()
