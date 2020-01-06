import http
import urllib3
from core.utils import check_is_none

http = urllib3.PoolManager()
chunk_size = 65536

def check_size(url):
    r = http.request('GET', url, preload_content=False)
    content_bytes = r.headers.get("Content-Length")
    r.release_conn()
    return content_bytes

def parse_inputs(model, thread):
    inputs = []
    for input in thread.models[model]['input_files']:
        id = check_is_none(input, 'id')
        name = check_is_none(input, 'name')
        available_resources = check_is_none(check_is_none(input, 'value'), 'resources')
        for r in available_resources:
            if check_is_none(r, "selected"):
                download_url = check_is_none(r, 'url')
        inputs.append({'id': id, 'name': name, 'download_url': download_url})
    return inputs
