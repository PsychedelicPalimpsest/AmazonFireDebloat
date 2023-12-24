from .ktNodes import *
import uuid

from .youtube import YouTubeSubscriptionChannel, YouTubeRecomendationChannel
baseMenus = {
    "find": ["KT_NAV_MENU_FIND", "[reftype=mb/screen,refid=BROWSE]", "browse_all"],
    "free": ["KT_NAV_MENU_FREE", "[reftype=mb/screen,refid=FREE]", "free_us_tfs"],
    "home": ["KT_NAV_MENU_HOME", "[reftype=mb/screen,refid=HOME_DEFAULT]", "hm_jar_home"],
    "live": ["KT_NAV_MENU_LIVE", "[reftype=mb/screen,refid=LIVE_DEFAULT]", "hm_live_jarvis_tfs"],
    "my_stuff": ["KT_NAV_MENU_LIBRARY", "[reftype=mb/screen,refid=LIBRARY]", "library_all_c"]
}

class ToolBarChannel(MediaChannel):
	TTL = 1
	def __init__(self, *_):
		MediaChannel.__init__(self, "Toolbar", "[reftype=spc,refid=htoolbar]", elements=[
				MediaRefItem("Launcher Settings", "Click here to get to the menu to clear the launcher settings",
					"amzns://apps/android?p=com.amazon.tv.launcher#Intent;action=android.settings.APPLICATION_DETAILS_SETTINGS;end",
					"[reftype=mb/item,refid=launchersettings]",
					"https://github.com/HeronErin/AmazonFireDebloat/blob/main/test_imgs/title_ad_rot.jpg?raw=true" )

			])

customRows = {
	"@recentApps": lambda _, **__: RecentApps("Recently used apps: ", f"[reftype=spc,refid=recentlyused]"),
	"@toolbar" : ToolBarChannel,
	"@youtubeSubs": YouTubeSubscriptionChannel,
	"@youtubeRecomendations": YouTubeRecomendationChannel
}


def full_control(config):
	print("a")
	defaultCount = 0
	priority = 20400
	past = []

	jarvis = JarvisRoot([])
	

	for menu in config.jsonData.get("root", []):
		mid = uuid.uuid4().hex

		kt = f"KT_NAV_MENU_{mid}"
		ref = f"[reftype=mb/screen,refid={mid}]"
		csId = mid

		if "element_base" in menu and not menu in past:
			if menu["element_base"] in baseMenus:
				kt, ref, csId = baseMenus[menu["element_base"]]
			else:
				print(f"Warning: {menu['element_base']} not in {', '.join(baseMenus.keys())}")
		elements = []
		for element in menu.get("elements", []):
			if type(element) is str:
				if element in customRows:
					elements.append(customRows[element](config))
				else:
					print(f"Warning: {element} not valid row!")
			elif type(element) is dict:
				assert "type" in element, f"Must include type in elements of ref menu: {element}"
				if element["type"] in customRows:
					elements.append(customRows[element["type"]](config, **element))
				else:
					print(f"Warning: {element} not valid row!")

		menu = RefMenu(title=menu.get("name", ""), priority=priority, navKey=kt, ref=ref, csId=csId, elements=elements)
		jarvis.elements.append(menu)
		past.append(menu)
		priority-=200
	return jarvis
