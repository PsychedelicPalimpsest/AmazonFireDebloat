import urllib.parse

def YouTubeSearch(query):
	query=urllib.parse.quote_plus(query)
	return f"amzns://apps/android?p=com.amazon.firetv.youtube#Intent;S.intentToFwd=youtube://search?query={query}&isVoice=false&launch=searchinapps;end"

def YouTubeVideo(id):
	return f"amzns://apps/android?p=com.amazon.firetv.youtube#Intent;S.intentToFwd=youtube://youtube.com/watch?v={id};end"
import base64
def KodiUri(uri):
	uri=base64.urlsafe_b64encode('ActivateWindow(10025,"plugin://plugin.video.watchnixtoons2/?action=actionEpisodesMenu&url=https%3a%2f%2fwww.wcofun.tv%2fanime%2fattack-on-titan",return)'.encode("utf-8")).decode("utf-8")
	uri = f"plugin://script.redirect.fav/_B64_/{uri}#Intent;component=org.xbmc.kodi/.Splash;end"
	uri=urllib.parse.quote_plus(uri)
	print(uri)
	# ActivateWindow(10025,&quot;plugin://plugin.video.youtube/channel/UCu9ytDtJg8xYtFX8f5UqyeA/playlist/PLAJpD5fqQPsKeWG2hsvxPRhf8nhrNevxK/&quot;,return)
	return f"amzns://apps/android?p=org.xbmc.kodi#Intent;S.intentToFwd={uri};end"




