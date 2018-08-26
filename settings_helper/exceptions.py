__all__ = [ 'SettingUnknown', 'SettingsError' ]

class SettingUnknown( Exception ):
    ''' 
    Raised when an unknown setting occurs, see self.section, self.name, self.value for details
    '''
    pass

class SettingsError( Exception ):
    '''
    Something has gone horribly wrong (programer mistake!) and we cannot continue.
    '''
    pass

