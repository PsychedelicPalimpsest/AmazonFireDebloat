import time
class AbstractKTNode:
    # Can take any args and kwargs
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    # Must return dict with no args or kwargs
    def serialize(self) -> dict:
        raise NotImplementedError
    def jserialize(self) -> dict: # Jarvis serializable element
        raise NotImplementedError
    def getRID(self) -> str: 
        raise NotImplementedError
    def getRef(self) -> str:
        raise NotImplementedError

    def needsThreading(self):
        return False

    def handle(self, resp, _id):
        resp["response"].append(self.serialize())
def idToDict(id_):
    id_ = id_[1:-1]
    return {b.split('=')[0]:b.split('=')[1] for b in id_.split(",")}

def dictToId(dic):
    return "["+",".join((k+"="+v for k, v in dic.items()))+ "]"
class MediaRefItem(AbstractKTNode):
    TTL = 10
    def __init__(self, text, desc, uri, ref, image=None):
        self.text=text
        self.desc=desc
        self.uri=uri
        self.image = image or "https://raw.githubusercontent.com/HeronErin/AmazonFireDebloat/main/test_imgs/title_ad_rot.jpg"
        self.ref = ref


        self.idDict = idToDict(ref)
    def getRID(self):
        return self.idDict.get("refid")
    def getRef(self):
        return self.ref

    def serialize(self):
        return {"type": "com.amazon.mediabrowse.referenceitem@3",
            "text": self.text,
            "ref": self.ref,
            "ttl": self.TTL,
            "csIdSource": None,
            "csId": None,
            "image": self.image,
            "qualifiedImage": None,
            "widescreenImage": None,
            "backgroundImage": None,
            "titleImage": None,
            "treatments": None,
            "headerText": " ",
            "description": self.desc,
            "descriptionHeader": None,
            "attributes": None,
            "contentRating": None,
            "enforcementRating": None,
            "itemRef": None,
            "referencedType": "external",
            "triggers": {
                "select": {
                    "activity": {
                        "uri": self.uri
                    }
                }
            },
            "previewVideoUrl": None,
            "previewVideoId": None,
            "previewVideoProvider": None,
            "displayAspectRatio": None,
            "badges": None,
            "adaptivePreviewVideoUrl": None,
            "metaData": None,
            "tags": None}


class MediaChannel(AbstractKTNode):
    TTL = 10
    def __init__(self, text, ref, elements = None,csId=None):
        self.text=text
        self.ref=ref
        self.csId = csId
        self.elements = elements or []

        self.idDict = idToDict(ref)
    def getRID(self):
        return self.idDict.get("refid")
    def getRef(self):
        return self.ref
    def serialize(self):
        return {
            "type": "com.amazon.mediabrowse.channel@2",
            "text": self.text,
            "ref": self.ref,
            "ttl": self.TTL,
            "refs": [element.getRef() for element in self.elements],
            "csId": "NAVIGATION:find-page:evergreenRow-v3",
            "smartlistActions": {
                "isAddSupported": False,
                "isRemoveSupported": False,
                "isNavigateToDetailPageSupported": False
            },
            "csChannel": {
                "refMarker": "NAVIGATION:find-page:evergreenRow-v3",
                "topicId": "NAVIGATION:find-page:evergreenRow-v3",
                "adsInserted": "0",
                "contentSource": "TFS",
                "feedId": "1703190681:7906538106279227351",
                "region": "US-OH",
                "templateId": "find-page",
                "engagementId": "NAVIGATION:find-page:evergreenRow-v3",
                "providerType": "NAVIGATION"
            },
            "csItems": None,
            "subtitle": None,
            "images": None,
            "itemHeight": None,
            "isGrid": None,
            "aspectRatioOverride": None,
            "refreshContext": None,
            "refreshPolicies": None,
            "ttk": None,
            "metaData": None,
            "tags": None
        }

    def handle(self, resp, _id):
        resp["response"].append(self.serialize())
        for e in self.elements:
            resp["additional"].append(e.serialize())

class RecentApps(MediaChannel):
    TTL=2000
    def __init__(self, text, ref):
        self.text=text
        self.ref=ref

        self.idDict = idToDict(ref)
    def serialize(self):
        return {
            "type": "com.amazon.mediabrowse.localdatasourcechannel@1",
            "text": self.text,
            "ref": self.ref,
            "ttl": self.TTL,
            "refs": [],
            "csId": "library_recents",
            "smartlistActions": {
                "isAddSupported": False,
                "isRemoveSupported": False,
                "isNavigateToDetailPageSupported": False
            },
            "csChannel": {
               "symphonyPageId": "library-app-reengagement",
                "isPinned": "true",
                "symphonySlotId": "center-0",
                "templateId": "recent-apps",
                "providerType": "SYMPHONY",
                "symphonyComponentName": "Channel",
                "refMarker": "library_recents",
                "subFeedType": "OVERRULED",
                "topicId": "SYMPHONY:recent-apps:library_recents",
                "adsInserted": "0",
                "contentSource": "TFS",
                "feedId": "1703190652:4882371426136571308",
                "symphonyCreativeId": "b01e4da7-2b4e-40de-900a-70ad150681bd",
                "region": "US-OH",
                "engagementId": "library_recents",
            },
            "csItems": None,
            "subtitle": None,
            "images": None,
            "categoryId": "cards",
            "itemHeight": None,
            "filters": {
                "subCategoryId": "library @@ recents"
            },
            "isGrid": None,
            "aspectRatioOverride": None,
            "refreshContext": None,
            "refreshPolicies": None,
            "ttk": None,
            "metaData": None,
            "tags": None
        }
    def handle(self, resp, _id):
        resp["response"].append(self.serialize())

class RefMenu(AbstractKTNode):
    TTL = 10
    def __init__(self, title:str, priority:int, navKey:str, ref:str,csId:str, iconUnicode=None, navMarkers = None, visibility = None, elements = None):
        self.title = title
        self.priority=priority
        self.navKey=navKey
        self.ref=ref
        self.csId=csId
        self.iconUnicode=iconUnicode
        self.navMarkers=navMarkers
        self.visibility=visibility or "TAB_ICON"
        self.elements = elements or []

        self.idDict = idToDict(ref)
    def getRID(self):
        return self.idDict.get("refid")
    def getRef(self):
        return self.ref
    def jserialize(self):
        return {
            "type": "com.amazon.mediabrowse.screenrefmenuelement@2",
            "title": self.title,
            "priority": self.priority,
            "navKey": self.navKey,
            "screenRef": self.ref,
            "iconUnicode": self.iconUnicode,
            "navMarkers": self.navMarkers,
            "visibility": self.visibility
        }
    def serialize(self):
        return {
            "type": "com.amazon.mediabrowse.navmenuscreen@1",
            "text": self.title,
            "ref": self.ref,
            "ttl": self.TTL,
            "csId": self.csId,
            "strips": [element.getRef() for element in self.elements],
            "bannerAdvertisement": None,
            "featuredRotatorRef": None,
            "pills": None,
            "metaData": {}, # Might need to be dict
            "tags": None,
            "weblabTreatmentsTriggered": {
                "FTV_CORSERV_EVRGRN_PRELD_758968": "C"
            }
        }


class JarvisRoot(AbstractKTNode):
    TTL = 10
    def __init__(self, elements):
        self.elements = elements
    def serialize(self): 
        return {
        "type": "com.amazon.mediabrowse.browsemenu@2",
        "text": "menu",
        "ref": "[reftype=browse/menu,refid=jarvis_root]",
        "ttl": self.TTL,
        "elements": [element.jserialize() for element in self.elements],
        "weblabTreatmentsTriggered": {},
        "metaData": None,
        "tags": None
    }
    def getRID(self):
        return "jarvis_root"
    def getRef(self):
        return "[reftype=browse/menu,refid=jarvis_root]"

