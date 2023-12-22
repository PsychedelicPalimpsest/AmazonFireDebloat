import json
from ktNodes import *
from mitmproxy import http
from intents import *
# print(YouTubeVideo("U94litUpZuc"))
def generateDefaultJarvis():
    return JarvisRoot([
        RefMenu(title="Find", priority=20400, navKey="KT_NAV_MENU_FIND", ref="[reftype=mb/screen,refid=BROWSE]", csId="browse_all"),
        RefMenu(title="Free", priority=20300, navKey="KT_NAV_MENU_FREE", ref="[reftype=mb/screen,refid=FREE]", csId="free_us_tfs",
            elements=[]),
        RefMenu(title="Home for hacker", priority=20000, navKey="KT_NAV_MENU_HOME", ref="[reftype=mb/screen,refid=HOME_DEFAULT]", navMarkers=["DEFAULT_HIGHLIGHT_SCREEN"], csId="hm_jar_home",
            elements=[
            MediaChannel(text="My channel", ref="[reftype=bc,refid=weeewooo]", elements=[
                MediaRefItem(text="Hello world", desc="An example list item", uri=YouTubeVideo("zo-LEmtSIY4"), ref="[reftype=spc,refid=avideo]")
                ])]),
        RefMenu(title="Live", priority=19500, navKey="KT_NAV_MENU_LIVE", ref="[reftype=mb/screen,refid=LIVE_DEFAULT]", navMarkers=["GUIDE_BUTTON_INGRESS"], csId="hm_live_jarvis_tfs",
            elements=[]),
        RefMenu(title="My Stuff", priority=19400, navKey="KT_NAV_MENU_LIBRARY", ref="[reftype=mb/screen,refid=LIBRARY]", csId="library_all_c",
            elements=[], iconUnicode="💩")
        ])
def query(element, id):
    if element.getRID() == id:
        return element

    if hasattr(element, "elements"):
        for e in element.elements:
            if (r:=query(e, id)):
                return r
def queryParent(element, id):
    if hasattr(element, "elements"):
        for e in element.elements:
            if e.getRID() == id:
                return element
            else:
                if (p:=queryParent(e, id)):
                    return p

root = generateDefaultJarvis()
def handleRequest(flow):
    rJson = {
      "type": "com.amazon.mediabrowse.response@1",
      "response": [],
      "additional": []
    }

    request = json.loads(flow.request.text)
    print(request)
    for id in request.get("id", []):
        refid = idToDict(id)["refid"]
        res = query(root, refid)
        print("search", refid, res)
        if res is None:
            print("Unknown: ", id)
            rJson["response"].append(    {
              "type": "com.amazon.mediabrowse.invalid@1",
              "text": "Invalid",
              "ref": id,
              "ttl": 600,
              "metaData": None,
              "tags": None
            })
        else:
            res.handle(rJson, id)

    flow.response = http.Response.make(200,
        json.dumps(rJson),
        {"Content-Type": "application/json"}  
        )




