import urllib.parse

def YouTubeSearch(query):
	query=urllib.parse.quote_plus(query)
	return f"amzns://apps/android?p=com.amazon.firetv.youtube#Intent;S.intentToFwd=youtube://search?query={query}&isVoice=false&launch=searchinapps;end"

def YouTubeVideo(id):
	return f"amzns://apps/android?p=com.amazon.firetv.youtube#Intent;S.intentToFwd=youtube://youtube.com/watch?v={id};end"