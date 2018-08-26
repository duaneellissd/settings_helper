from unittest import TestCase
import os
import settings_helper

TEST1_INI_FILENAME = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), 'test_data1.ini')
TEST2_INI_FILENAME = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), 'test_data2.ini')

class MyHelper( settings_helper.SettingsHelper ):
    def __init__( self, name, thedict, autoregister=True):
        settings_helper.SettingsHelper.__init__(self, name, thedict, autoregister  )

const_settings = {
    'test1' : { 'pi' : 3.14159, 'b' : 'b', 'a' : ord('a') },
    'test2' : { 'pi2' : 2 * 3.14159, 'a' : ord('a'), 'b' : 'b' }
}
        
        
class MyTestClass1( object ):
    def __init__(self):
        # we should find this
        self.settings = MyHelper( "test1", const_settings['test1']  )
        # this should not be found
        self.settings2 = MyHelper( "NOT_HERE", { 'X' : ord('X'), 'y' : 'y', 'z' : 42.4242 }, False )

class MyTestClass2(object):
    def __init__(self):
        self.settings = MyHelper( "test2", const_settings['test2']  )
        
def copy_settings():
    return copy.deepcopy( const_settings )

def compare_dicts_keys( a, b ):
    if len(a) != len(b):
        return "different lengths"
    for k in a.keys():
        if k not in b:
            return "missing key: %s" % k
    return None

def compare_dict_values( a, b ):
    r = compare_dict_keys(a,b)
    if r != None:
        return r
    for k in a.keys():
        if a[k] != b[k]:
            return "a[%s]=%s, b[%s]=%s" % (k,a[k],k,b[k])
    return None
    
class test_settings( TestCase ):
    def test_010_save_recall( self ):
        dut1 = MyTestClass1()
        dut2 = MyTestClass2()
        self.assertEqual( 2, len( settings_helper.global_settings.all_settings ) )
        settings_helper.global_settings.save_to_ini( TEST1_INI_FILENAME )

        dut1.settings.a = 1
        dut1.settings.b = 'bees and honey'
        dut1.settings.pi = 99.999

        dut2.settings.a = 3
        dut2.settings.b = 'bees sting'
        dut2.settings.pi2 = 99.999 / 3.0

        # Save this as modified
        settings_helper.global_settings.save_to_ini( TEST2_INI_FILENAME )

        # Set factory defaults
        settings_helper.global_settings.factory_defaults()

        def verify_defaults():
            # Verify we have factory defaults
            for thing, values in const_settings.items():
                if thing == 'test1':
                    d = dut1
                else:
                    d = dut2
                    for k,v in values.items():
                        self.assertEqual( getattr( d.settings, k ), v )

        verify_defaults()
                        
        # load settings from 1
        settings_helper.global_settings.load_from_ini( TEST2_INI_FILENAME )
        self.assertEqual( dut1.settings.a , 1 )
        self.assertEqual( dut1.settings.b , 'bees and honey')
        self.assertEqual( dut1.settings.pi ,99.999)

        self.assertEqual( dut2.settings.a , 3)
        self.assertEqual( dut2.settings.b , 'bees sting')
        self.assertEqual( dut2.settings.pi2 , 99.999 / 3.0)

        # Load factory defaults
        settings_helper.global_settings.load_from_ini( TEST1_INI_FILENAME )

        verify_defaults()

        
