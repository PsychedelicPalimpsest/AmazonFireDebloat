from mitmproxy import http
from src import handleKT, handleConfig
import os

import asyncio

from mitmproxy.tools import main
from mitmproxy.tools.dump import DumpMaster

class AmazonAddon:
    config : handleConfig.Config
    def request(self, flow: http.HTTPFlow) -> None:
        print("Request:", flow.request.url)
        if "aviary.amazon.com" == flow.request.headers.get("host"):

            flow.response = http.Response.make(
                502,  # Status code: Bad Gateway
                b"No aviary for you!!!",
                {"Content-Type": "text/plain"}  
            )
        if "ktpx.amazon.com/mb/data" in flow.request.url:
            handleKT.handleRequest(flow, self.config)
        elif "ktpx.amazon.com" == flow.request.headers.get("host"):
            flow.response = http.Response.make(
                502,  # Status code: Bad Gateway
                b"Kt server unsupported",
                {"Content-Type": "text/plain"}  
            )
dir_path = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(dir_path, "active.cfg.json")


if not os.path.exists(config_dir):
    print("Error: can't find active config file. Please create an 'active.cfg.json' file.")
    exit(-1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    addon = AmazonAddon()

    addon.config = handleConfig.Config(open(config_dir, 'r'))

    async def asyncMain():
        options = main.options.Options(listen_host='0.0.0.0', listen_port=8080)
        m = DumpMaster(options=options)
        m.addons.add(addon)
        await m.run()
    # loop.run_until_complete(asyncMain())