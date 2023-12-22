import urllib.parse

def YouTubeSearch(query):
	query=urllib.parse.quote_plus(query)
	return f"amzns://apps/android?p=com.amazon.firetv.youtube#Intent;S.intentToFwd=youtube://search?query={query}&isVoice=false&launch=searchinapps;end"

def YouTubeVideo(id):
	return f"amzns://apps/android?p=com.amazon.firetv.youtube#Intent;S.intentToFwd=youtube://youtube.com/watch?v={id};end"

def KodiUri(uri):
	uri=urllib.parse.quote_plus(uri)
	print(uri)
	# ActivateWindow(10025,&quot;plugin://plugin.video.youtube/channel/UCu9ytDtJg8xYtFX8f5UqyeA/playlist/PLAJpD5fqQPsKeWG2hsvxPRhf8nhrNevxK/&quot;,return)
	return f"amzns://apps/android?p=org.xbmc.kodi#Intent;S.intentToFwd={uri};end"