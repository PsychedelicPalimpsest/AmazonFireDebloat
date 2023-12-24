import os, requests, time, uuid
from youtube_dl import YoutubeDL
from youtube_dl.extractor import (
    YoutubeIE,
    YoutubePlaylistIE,
    YoutubeTabIE,
)
from youtube_dl.utils import YoutubeDLCookieJar

from .ktNodes import MediaRefItem, MediaChannel
from .intents import *

class RefreshingChannel(MediaChannel):
    def __init__(self, *args, **kwargs):
        MediaChannel.__init__(self, *args, **kwargs)
        self.lastHandle = None
    def handle(self, resp, _id):
        if self.lastHandle is not None:
            if time.time()-self.lastHandle < self.TTL*60:
                MediaChannel.handle(self, resp, _id)
        self.refresh()
        self.lastHandle = time.time()
        MediaChannel.handle(self, resp, _id)
class YouTubeSubscriptionChannel(RefreshingChannel):
    def __init__(self, config):
        self.TTL = 10
        self.config=config
        if not hasattr(config, "youTubeHandler"):
            config.youTubeHandler = YouTubeHandler(config)
        RefreshingChannel.__init__(self, 
            text="Your youtube subscriptions", 
            ref=f"[reftype=bc,refid=youtubesub]")
    def refresh(self):
        self.elements=self.config.youTubeHandler.getElements("https://www.youtube.com/feed/subscriptions")


class YouTubeRecomendationChannel(RefreshingChannel):
    def __init__(self, config):
        self.TTL = 5
        self.config=config
        if not hasattr(config, "youTubeHandler"):
            config.youTubeHandler = YouTubeHandler(config)
        RefreshingChannel.__init__(self, 
            text="Your youtube recommendendations", 
            ref=f"[reftype=bc,refid=youtuberec]")
    def refresh(self):
        self.elements=self.config.youTubeHandler.getElements("https://www.youtube.com/feed/recommended")



class YouTubeHandler:
    def __init__(self, config):

        if "youtube_cookie_file" in config.jsonData:
            self.ydl = YoutubeDL({"cookiefile": config.jsonData['youtube_cookie_file']})
            self.ie = YoutubeTabIE(self.ydl)
            
            def tmp():
                # Handles closing cookies and stuff
                with self.ydl: pass

            config.onExit.append(tmp)


        else:
            print("ERROR: You can not use youtube rows without storing youtube cookies! Please create a \"youtube_cookie_file\" entry in your config of a dump of your youtube account cookies.")
            exit(-1)
    def getElements(self, url):
        elements = []
        sub = self.ie.extract(url)
        assert "entries" in sub, "YouTube sent a malformed response"
        for i, video in enumerate(sub["entries"]):
            if i > 20:
                break
            assert video["_type"] == "url", f"Youtube sent object: {video}"
            mref = MediaRefItem(
                  video.get("title"),
                 f"From: {video.get('uploader')}\n{video.get('description')}",
                  YouTubeVideo(video.get('id')), 
                  f'[reftype=mb/item,refid=youtube{video.get("id")}]', 
                  image=f"https://img.youtube.com/vi/{video.get('id')}/mqdefault.jpg")
            mref.TTL=600 # Youtube videos shouldn't change that much
            elements.append(mref)  
        print(elements)
        return elements



# y = YouTubeHandler(
# print(y.getSubscription())