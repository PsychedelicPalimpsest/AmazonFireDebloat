import xbmcaddon
import xbmcgui
import xbmc
import sys
import base64
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
URL = sys.argv[0]

# This can run pretty much anything. 


if "/_B64_/" in URL:
	b = URL.split("/_B64_/")[-1].encode("utf-8")
	to_run = base64.urlsafe_b64decode(b).decode("utf-8")
	xbmc.log(msg=f'{addonname}: Running builtin from user: {to_run}', level=xbmc.LOGWARNING);
	xbmc.executebuitin(to_run)
