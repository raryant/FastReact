
from starlette.responses import HTMLResponse, JSONResponse, Response, PlainTextResponse, FileResponse
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from .React import core as ReactCore, constructor as ReactConstructor
from fastapi.staticfiles import StaticFiles
import base64

class APP(FastAPI):
    __component_list__ = []
    __favicon__ = ""
    def setup(self):
        @self.exception_handler(StarletteHTTPException)
        def redirect_to_root(req, exc):
            return RedirectResponse('/')
        self.__favicon__ = ReactCore.os.path.join(ReactCore.get_static_directory(), 'favicon.ico')
        print(self.__favicon__)
        self.router.on_event("startup")(self.__register_component__)
    def component(self, component_name: str = "Fast React Component"):
        def component_wrapper(component):
            component.__dict__['name'] = component_name
            self.__component_list__.append(component)
            def wrapper(*args, **kwargs):
                return component(*args, **kwargs)
            return wrapper
        return component_wrapper
    def setFavicon(self, path: str):
        self.__favicon__ = path
    def __register_component__(self):
        print("available component: ", self.__component_list__)
        self.get('/', include_in_schema=False, response_class=HTMLResponse)(ReactCore.index)
        self.get('/apps.js', include_in_schema=False, response_class=PlainTextResponse)(ReactCore.js)
        self.get('/favicon.ico', include_in_schema=False)(lambda : FileResponse(self.__favicon__))
        # self.mount("/react_static", StaticFiles(directory=ReactCore.get_static_directory()), name="react_static")
        super().setup()
    
        