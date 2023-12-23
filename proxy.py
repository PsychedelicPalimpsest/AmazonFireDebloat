from mitmproxy import http
from src import handleKT


def request(flow: http.HTTPFlow) -> None:
    if "aviary.amazon.com" == flow.request.headers.get("host"):

        flow.response = http.Response.make(
            502,  # Status code: Bad Gateway
            b"No aviary for you!!!",
            {"Content-Type": "text/plain"}  
        )
    if "ktpx.amazon.com/mb/data" in flow.request.url:
        handleKT.handleRequest(flow)
    elif "ktpx.amazon.com" == flow.request.headers.get("host"):
        flow.response = http.Response.make(
            502,  # Status code: Bad Gateway
            b"Kt server unsupported",
            {"Content-Type": "text/plain"}  
        )
