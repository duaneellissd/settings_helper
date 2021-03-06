# Save & Recall Settings

Settings helper for python apps, save, recall, and reset-to-default application settings.

In various application you often have 'settings' that need
to be saved or recalled from a file, these classes helps do that.

There are two important classes:

* SettingsHelper()
* SettingsTool()

## To install from git hub:

   bash$ pip install git+https://github.com/duaneellissd/settings_helper.git
   
   # or, download a zip file
   
   bash$ pip install settings_helper.zip

## class SettingsHelper()

The intent is that each major class in your app has 
a "setting helper" object, constructed like this:

    <!-- language: python -->
    class Foo(object);
        def __init__( self, ... ):
             self.settings = SettingsHelper( sectionname, default_values )

The settings can then be saved or read from a INI file, via
the SettingsTool() class, which uses the ConfigParser class.

*Note* the "sectionname" must be unique across the entire application.

*Example*: a camera vision system might have settings like this:

   <!-- language: python -->
   self.camera = SettingsHelper( "cam0", default_camera_values )

   print("Camera section: %s" % self.camera._section )
   # Where "_section" might be: "cam0", and "cam1"
   print("Camera id: %d" % self.camera.id )
   print("Camera  h: %d" % self.camera.height )
   print("Camera  w: %d" % self.camera.width )

Other examples might include:

* Font selection
* Unit of measure (ie: Imperial Metric)
* Printer Settings (ie: Landscape, gray, color)
* Username & Email Address

Only simple settings are supported, and must be one of:

* None
* str
* bool
* int
* str
* float
* NOT currently SUPPORTED compound types, ie: lists, tuples, dicts.

Note the value "None" uses a magic string '__NONE__' in the INI file

## class SettingsTool()

The class SettingsTool() is used to read or save the settings to a file
it manages (via a module global variable) to track all settings through
out the application so that the can easily be saved or recalled.

In addition, sometimes users screw up settings and you need 
the ability to reset all settings to their "factory defaults"

*Note*: Multiple settings files can be supported, see the source for details.

*For example*:

   tool = SettingsTool()
   tool.register( someclass.settings )
   tool.register( otherclass.settings )
   ... and more settings ...
   tool.save_to_ini( "somefilename.ini" )

Then later:

   tool.load_from_ini( "somefilename.ini")

Both the tool, and the helpers contain some hooks or callbacks
as defined by class SettingsCallbacks() that can be used to
add more functionality.


DO NOT DO THIS:

   # Step 1
   defaults = { 'id' : 123, 'height' : 480, 'width': 640 }
   self.settings = SettingsHelper( 'camera', defaults )

   # Step 2 - Do do this to set defaults
   # they are already set for you.
   self.settings.id = 123

   # Todo note: how does one document the SETTINGS member names?

FUTURE:

* Today this uses a ConfigFile to save the data.
* It could in the future use a json file
* Or possibly a pickle file (this would support compound types)

