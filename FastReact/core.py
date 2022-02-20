
import logging
from typing import Any, Callable, Optional
from urllib.request import Request
from starlette.responses import HTMLResponse, JSONResponse, Response, PlainTextResponse, FileResponse
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from .React import core as ReactCore, constructor as ReactConstructor, theme as ReactTheme
from fastapi.staticfiles import StaticFiles

from fastapi.responses import Response
from fastapi import APIRouter
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
)

from fastapi import params
from fastapi.datastructures import Default
from fastapi.encoders import DictIntStrAny, SetIntStr
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from fastapi.params import Depends
from starlette.routing import BaseRoute
from starlette.middleware import Middleware


class FastReactAPP(FastAPI):
    __component_list__ = {}
    __component_group_list__ = {}
    logger = logging.getLogger('uvicorn')
    def __init__(self, ui_path: str = '', theme_path: str = '/theme',debug: bool = False,routes: Optional[List[BaseRoute]] = None,title: str = "FastAPI",description: str = "",version: str = "0.1.0",openapi_url: Optional[str] = "/openapi.json",openapi_tags: Optional[List[Dict[str, Any]]] = None,servers: Optional[List[Dict[str, Union[str, Any]]]] = None,dependencies: Optional[Sequence[Depends]] = None,default_response_class: Type[Response] = Default(JSONResponse),docs_url: Optional[str] = "/docs",redoc_url: Optional[str] = "/redoc",swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,middleware: Optional[Sequence[Middleware]] = None,exception_handlers: Optional[Dict[Union[int, Type[Exception]],Callable[[Request, Any], Coroutine[Any, Any, Response]],]] = None,on_startup: Optional[Sequence[Callable[[], Any]]] = None,on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,terms_of_service: Optional[str] = None,contact: Optional[Dict[str, Union[str, Any]]] = None,license_info: Optional[Dict[str, Union[str, Any]]] = None,openapi_prefix: str = "",root_path: str = "",root_path_in_servers: bool = True,responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,callbacks: Optional[List[BaseRoute]] = None,deprecated: Optional[bool] = None,include_in_schema: bool = True,**extra: Any,) -> None:
        kwargs = locals()
        kwargs.pop('self', None)
        super().__init__(**kwargs)
        self.UIRouter = ReactCore.UIRouter(path=ui_path, theme_path=theme_path)
        self.ThemeRouter = ReactTheme.ThemeRouter(path=theme_path)
        self.include_router(self.UIRouter)
        self.include_router(self.ThemeRouter)
        self.component_group('Fast React')(ReactConstructor.ComponentGroup)
        self.router.on_event("startup")(self.__register_component__)
        @self.exception_handler(StarletteHTTPException)
        async def exception_handler(request: Request, exception: StarletteHTTPException):
            if exception.status_code == 404:
                return Response(content=await self.UIRouter.index_handler())
            return RedirectResponse('/')
        @self.get(f'/_components/drawer_content.json')
        async def get_drawer_content():
            content = []
            component_group: ReactConstructor.ComponentGroup
            for component_group_name in self.__component_group_list__.keys():
                component_group = self.__component_group_list__[component_group_name]
                if component_group_name == 'Fast React':
                    if len(component_group.children) > 0:
                        content.append(component_group.get_drawer_object())
                else: content.append(component_group.get_drawer_object())
            return JSONResponse(content=content)
    def set_favicon(self, path: str)->bool: return self.UIRouter.set_favicon_path(path)
    def set_header_image(self, path: str)->bool: return self.UIRouter.set_drawer_header_image_path(path)
    def component_group(self, group_name: str = "Fast-React-Component-Group"):
        def component_group_wrapper(component_group_class):
            component_group: ReactConstructor.ComponentGroup
            component_group = component_group_class()
            component_group.set_component_group_name(group_name)
            self.__component_group_list__[group_name] = component_group
            return group_name
        return component_group_wrapper
            
    def component(self, component_name: str = "Fast-React-Component", api_prefix: str = '/', group: Any = None):
        assert api_prefix[0] == '/', "api_prefix must begin with '/'"
        def component_wrapper(component_class):
            component: ReactConstructor.Component
            component = component_class()
            component.set_component_name(component_name)
            for api_path in component.api.keys():
                api = component.api[api_path]
                if api_prefix != '/': api['kwargs']['path'] = api_prefix + api_path
                if api['method'] == "get":
                    self.logger.debug(f"Register Get Method for {api_path}!")
                    self.get(*api['args'], **api['kwargs'])(api['func'])
                if api['method'] == "post":
                    self.logger.debug(f"Register Post Method for {api_path}!")
                    self.post(*api['args'], **api['kwargs'])(api['func'])
            self.__component_list__[component_name] = component
            if group != None:
                group_name = group() if callable(group) else group
                _group: ReactConstructor.ComponentGroup
                _group = self.__component_group_list__.get(group_name)
                assert _group != None, "Group Not Found!"
                _group.add_children_component(component_name, component)
            self.get(f'/_components/{component.path}', include_in_schema=False)(component.load_component)
            return component
        return component_wrapper
    
    def __register_component__(self):
        pass
        # print("available component Group: ", self.__component_group_list__)
        component: ReactConstructor.Component
    
        