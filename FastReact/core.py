
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
        @self.exception_handler(StarletteHTTPException)
        def redirect_to_root(req, exc):
            return RedirectResponse('/')
        self.UIRouter = ReactCore.UIRouter(path=ui_path, theme_path=theme_path)
        self.ThemeRouter = ReactTheme.ThemeRouter(path=theme_path)
        self.include_router(self.UIRouter)
        self.include_router(self.ThemeRouter)
        self.router.on_event("startup")(self.__register_component__)

    def component(self, component_name: str = "Fast React Component"):
        def component_wrapper(component):
            component.__dict__['name'] = component_name
            self.__component_list__.append(component)
            def wrapper(*args, **kwargs):
                return component(*args, **kwargs)
            return wrapper
        return component_wrapper
    
    def __register_component__(self):
        print("available component: ", self.__component_list__)
    
        