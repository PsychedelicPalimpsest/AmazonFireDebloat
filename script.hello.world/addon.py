import xbmcaddon
import xbmcgui
import sys
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
URL = sys.argv[0]

# Set a string variable to use 
line1 = "Hello World! " + URL

# Launch a dialog box in kodi showing the string variable 'line1' as the contents
xbmcgui.Dialog().ok(addonname, line1)
