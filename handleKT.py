import json
from ktNodes import *
from mitmproxy import http


def generateDefaultJarvis():
    return JarvisRoot([
        RefMenu(title="Find", priority=20400, navKey="KT_NAV_MENU_FIND", ref="[reftype=mb/screen,refid=BROWSE]", csId="browse_all"),
        RefMenu(title="Free", priority=20300, navKey="KT_NAV_MENU_FREE", ref="[reftype=mb/screen,refid=FREE]", csId="free_us_tfs"),
        RefMenu(title="Home for hacker", priority=20000, navKey="KT_NAV_MENU_HOME", ref="[reftype=mb/screen,refid=HOME_DEFAULT]", navMarkers=["DEFAULT_HIGHLIGHT_SCREEN"], csId="hm_jar_home",
            elements=[
                MediaChannel("Hacker news", "[reftype=bc,refid=WATCHLIST]", [
                    MediaRefItem("We fucking did it", "Some description text", "https://www.youtube.com/watch?v=zo-LEmtSIY4", "[reftype=mb/item,refid=exvid]")
                    ])
            ]),
        RefMenu(title="Live", priority=19500, navKey="KT_NAV_MENU_LIVE", ref="[reftype=mb/screen,refid=LIVE_DEFAULT]", navMarkers=["GUIDE_BUTTON_INGRESS"], csId="hm_live_jarvis_tfs"),
        RefMenu(title="My Stuff", priority=19400, navKey="KT_NAV_MENU_LIBRARY", ref="[reftype=mb/screen,refid=LIBRARY]", csId="library_all_c")
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




