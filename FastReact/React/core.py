import aiofiles
import asyncio
import os
from fastapi.responses import Response
from fastapi import status as HTTP_STATUS
import rjsmin

def get_static_directory()->str:
    return os.path.join(os.path.dirname(__file__), 'src')

async def read_file(file_name):
    async with aiofiles.open(file_name, mode='r') as f:
        return await f.read()

async def js(resp: Response):
    resp.headers['content-type'] = 'text/plain'
    # resp.headers['cache-control'] = "public, s-maxage=600, max-age=60"
    content = []
    files = os.listdir(get_static_directory())
    content.append(read_file(os.path.join(get_static_directory(), 'library.js')))
    for file in files:
        if file[-3:].lower() == '.js' and file != 'renderer.js' and file != 'library.js':
            content.append(read_file(os.path.join(get_static_directory(), file)))
    content.append(read_file(os.path.join(get_static_directory(), 'renderer.js')))
    javascript =  "".join(await asyncio.gather(*content))
    return javascript
    return rjsmin.jsmin(javascript)

async def index():
    content = ""
    async with aiofiles.open(os.path.join(get_static_directory(), 'index.html'), mode='r') as handler:
        content = await handler.read()
    available_js = ""
    available_js += f'\t<script type="text/babel" src="/apps.js"></script>\r\n'
    # files = os.listdir(get_static_directory())
    # for file in files:
    #     if file[-3:].lower() == '.js':
    #         available_js += f'\t<script type="text/babel" src="/react_static/{file}"></script>\r\n'
    return content.replace("%REACT_SCRIPT%", available_js[:-2])
    
    