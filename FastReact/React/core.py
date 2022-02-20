import aiofiles
import asyncio
import os
from fastapi.responses import Response, PlainTextResponse, HTMLResponse, StreamingResponse, FileResponse
from fastapi import status as HTTP_STATUS, APIRouter
import rjsmin
from FastReact.helper import read_file
import logging

class UIRouter(APIRouter):
    favicon_path = os.path.join(os.path.dirname(__file__), 'default', 'favicon.ico')
    drawer_header_image_path = os.path.join(os.path.dirname(__file__), 'default', 'drawerHeader.jpg')
    drawer_header_endpoint = ""
    def __init__(self, path: str = '', theme_path: str = '', asset_path: str = 'assets', drawer_header_endpoint: str = None,*args, **kwargs):
        self.__theme_path__ = theme_path
        self.__assets_path__ = asset_path
        self.drawer_header_endpoint = drawer_header_endpoint if isinstance(drawer_header_endpoint, str) else f'/{self.__assets_path__}/drawer_header.js'
        super().__init__(prefix=path, *args, **kwargs)
        self.logger = logging.getLogger('uvicorn')
        @self.get(f'/{self.__assets_path__}/apps.js', include_in_schema=False)
        async def js(resp: Response):
            resp.media_type = "application/javascript"
            resp.headers['content-type'] = 'text/babel'
            # resp.headers['cache-control'] = "public, s-maxage=600, max-age=60"
            content = []
            files = os.listdir(self.get_src_directory())
            content.append(read_file(os.path.join(self.get_src_directory(), 'library.js')))
            for file in files:
                if file[-3:].lower() == '.js' and file != 'renderer.js' and file != 'library.js':
                    content.append(read_file(os.path.join(self.get_src_directory(), file)))
            content.append(read_file(os.path.join(self.get_src_directory(), 'renderer.js')))
            javascript =  "".join(await asyncio.gather(*content))
            javascript = javascript.replace('%THEME_PATH%', self.__theme_path__)
            javascript = javascript.replace('%ASSETS_PATH%', f'/{self.__assets_path__}')
            javascript = javascript.replace('%DRAWER_HEADER_ENDPOINT%', self.drawer_header_endpoint)
            return Response(javascript, media_type="text/javascript")
            return rjsmin.jsmin(javascript)
        @self.get('/', include_in_schema=False, response_class=HTMLResponse)
        async def index():
            content = ""
            async with aiofiles.open(os.path.join(self.get_src_directory(), 'index.html'), mode='r') as handler:
                content = await handler.read()
            available_js = ""
            available_js += f'\t<script data-plugins="transform-modules-umd" data-presets="es2015,stage-3,react" data-type="module" type="text/babel" src="/{self.__assets_path__}/apps.js"></script>\r\n'
            return content.replace("%REACT_SCRIPT%", available_js[:-2])
        @self.get('/favicon.ico', include_in_schema=False)
        def favicon(resp: Response):
            resp.headers['cache-control'] = "public, s-maxage=600, max-age=60"
            resp.media_type = "image/vnd.microsoft.icon"
            return FileResponse(path=self.get_favicon_path())

        @self.get(f'/{self.__assets_path__}/HeaderLogo.png', include_in_schema=False)
        def drawerImage(resp: Response):
            resp.headers['cache-control'] = "public, s-maxage=600, max-age=60"
            return FileResponse(path=self.get_drawer_header_image_path(), media_type='image/png')
            
        @self.get(self.drawer_header_endpoint, include_in_schema=False)
        def drawerHeader(resp: Response):
            resp.headers['cache-control'] = "public, s-maxage=600, max-age=60"
            resp.media_type = "application/javascript"
            ret = "const DrawerHeaderImage = () =>{ return (<div id='drawerImage' style={{width: '100%', height: '100%', backgroundSize: '100% 100%', backgroundRepeat: 'no-repeat', backgroundPosition: 'center' ,backgroundImage: 'url(\""+self.__assets_path__+"/HeaderLogo.png\")'}} alt='Header Logo' />)};export default DrawerHeaderImage"
            # ret = rjsmin.jsmin(ret)
            return PlainTextResponse(content=ret, media_type="text/javascript")
        self.index_handler = index
        self.apps_js_handler = js
        self.drawer_image_header_handler = drawerHeader

    def get_favicon_path(self):
        path = os.path.join(self.favicon_path)
        if not os.path.isfile(path):
            self.logger.error(f'favicon not available! returning default favicon')
            path = os.path.join(os.path.dirname(__file__), 'default', 'favicon.ico')
        return path

    def set_favicon_path(self, path: str)->bool:
        if not os.path.isfile(path):
            self.logger.error(f'{path} not exists')
            return False
        self.favicon_path = path
        return True
    
    def get_drawer_header_image_path(self):
        path = os.path.join(self.drawer_header_image_path)
        if not os.path.isfile(path):
            self.logger.error(f'favicon not available! returning default favicon')
            path = os.path.join(os.path.dirname(__file__), 'default', 'favicon.ico')
        return path

    def set_drawer_header_image_path(self, path: str):
        if not os.path.isfile(path):
            self.logger.error(f'{path} not exists')
            return False
        self.drawer_header_image_path = path
        return True


    def get_src_directory(self)->str:
        return os.path.join(os.path.dirname(__file__), 'src')
    
    
    