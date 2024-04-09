import sys
import platform
import asyncio
import json
from collections.abc import Callable

_url: str = None
_data: str = None
_callback: Callable[[dict], None] = None
_requests = None


def init():
    global _requests
    if sys.platform == "emscripten":
        platform.window.eval("""
window.Fetch = {}
window.Fetch.POST = function * POST (url, data)
{
    var request = new Request(url, {headers: {'Accept': 'application/json','Content-Type': 'application/json'}, method: 'POST', body: data});
    var content = 'undefined';
    fetch(request).then(resp => resp.text()).then((resp) => {content = resp;});
    while(content == 'undefined'){yield;}
    yield content;
}
        """)
    else:
        import requests
        _requests = requests


def post(url: str, data: dict, callback: Callable[[dict], None]):
    global _url, _data, _callback
    _url = url
    _data = json.dumps(data)
    _callback = callback


async def flush():
    global _url, _data, _callback, _requests
    if not _url:
        return
    result: dict = None
    if _requests:
        result = _requests.post(
            _url, _data, headers={"Accept": "application/json", "Content-Type": "application/json"}
        ).json()
    else:
        await asyncio.sleep(0)
        content = await platform.jsiter(platform.window.Fetch.POST(_url, _data))
        result = json.loads(content)

    if _callback:
        _callback(result)
