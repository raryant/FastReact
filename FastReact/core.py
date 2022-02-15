
from typing import Any, Optional
from urllib.request import Request
from starlette.responses import HTMLResponse, JSONResponse, Response, PlainTextResponse, FileResponse
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from .React import core as ReactCore, constructor as ReactConstructor, theme as ReactTheme
from fastapi.staticfiles import StaticFiles
import base64

class FastReactAPP(FastAPI):
    __component_list__ = []
    def __init__(self, ui_path: str = '', theme_path: str = '/theme', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UIRouter = ReactCore.UIRouter(path=ui_path, theme_path=theme_path)
        self.ThemeRouter = ReactTheme.ThemeRouter(path=theme_path)
        self.include_router(self.UIRouter)
        self.include_router(self.ThemeRouter)
        self.router.on_event("startup")(self.__register_component__)
        @self.exception_handler(StarletteHTTPException)
        async def exception_handler(request: Request, exception: StarletteHTTPException):
            if exception.status_code == 404:
                print('404 Triggered')
                return Response(content=await self.UIRouter.index_handler())
            return RedirectResponse('/')
    def set_favicon(self, path: str)->bool: return self.UIRouter.set_favicon_path(path)
    def set_header_image(self, path: str)->bool: return self.UIRouter.set_drawer_header_image_path(path)

    def component(self, component_name: str = "Fast-React-Component"):
        def component_wrapper(component_class: ReactConstructor.Component):
            component: ReactConstructor.Component
            component = component_class()
            for api_path in component.api.keys():
                api = component.api[api_path]
                print(api)
                if api['method'] == "get":
                    print("Register Get Method!")
                    self.get(api_path, *api['args'], **api['kwargs'])(api['func'])
            component.set_component_name(component_name)
            self.__component_list__.append(component)
            self.router.get(f'/_components/{component_name}')(component.load_component)
            # @self.get(f'/_components/{component_name}')
            # async def call():
            #     return await component()
            return component
        return component_wrapper
    
    def __register_component__(self):
        print("available component: ", self.__component_list__)
        component: ReactConstructor.Component
        for component in self.__component_list__:
            # self.get(f'/_components/{component.component_name}')(await component())
            print(component)
    
        