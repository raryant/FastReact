
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
from pydantic import BaseModel, Json
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

class ComponentGroup:
    header = {}
    name = "Fast-React-Component-Group"
    description = "Fast-React-Component-Group"
    icon = "apps"
    children = {}
    display_empty = False
    def __init__(self) -> None:
        self.children = {}
    def __str__(self) -> str:
        return f"{self.name} Group\r\n"
    def __repr__(self) -> str:
        return f'\r\n{str(self)}Available Component: {repr(self.children)}\r\n\r\n'
    def __call__(self)-> Any:
        return self.name
    def set_component_group_name(self, name: str):
        self.name = name
    def add_children_component(self, component_name: str,  component: Any):
        self.children[component_name] = component
    def get_children_json(self):
        # {content: 'Dashboard', name: 'Dashboard', icon: <span className="material-icons">menu</span>, path: "/", level: [0,1,2,3]},
        child = []
        for childKey in self.children.keys():
            child_component: Component
            child_component = self.children.get(childKey)
            child.append({
                "name": child_component.name,
                "icon": child_component.icon,
                "path": child_component.path,
                "level": child_component.level,
            })
        return child
        
    def get_drawer_object(self)->dict:
        return {
         "menu": self.name,
         "desc": self.description,
         "icon": self.icon,
         "subMenu": self.get_children_json(),
         "display_empty": self.display_empty
        }
class Component:
    media_type = "text/javascript"
    header = {}
    name = "Fast-React-Component"
    path: str = None
    icon = "double_arrow"
    api = {}
    level = [0,1,2,3]
    group = None
    def __init__(self)->None:
        if self.path == None: self.path = self.name
    def set_component_name(self, name: str):
        self.name = name
    def set_component_path(self, path: str):
        self.path = path
    def set_group_name(self, group: Any):
        self.group = group
    def drawer_button(self):
        return f'<span className="material-icons">{self.icon}</span>'
    async def load_component(self):  
        content = "const ComponentApp = () => { return(<div>"
        content += "Hello World!\r\n"
        content += self.drawer_button()
        content += "</div>)}; export default ComponentApp"
        return Response(content=content, headers=self.header, media_type=self.media_type)
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f'Component Object {str(self)}'
    @classmethod
    def get(self,path: str,*,response_model: Optional[Type[Any]] = None,status_code: Optional[int] = None,tags: Optional[List[str]] = None,dependencies: Optional[Sequence[params.Depends]] = None,summary: Optional[str] = None,description: Optional[str] = None,response_description: str = "Successful Response",responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,deprecated: Optional[bool] = None,operation_id: Optional[str] = None,response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,response_model_by_alias: bool = True,response_model_exclude_unset: bool = False,response_model_exclude_defaults: bool = False,response_model_exclude_none: bool = False,include_in_schema: bool = True,response_class: Type[Response] = Default(JSONResponse),name: Optional[str] = None,callbacks: Optional[List[BaseRoute]] = None,openapi_extra: Optional[Dict[str, Any]] = None,):
        kwargs = locals()
        kwargs.pop('self', None)
        args = ()
        def decorator(func):
            self.api[path] = {
                "args": args,
                "kwargs": kwargs,
                "func": func, 
                "method": "get"
            } 
            return func
        return decorator

    @classmethod
    def post(self,path: str,*,response_model: Optional[Type[Any]] = None,status_code: Optional[int] = None,tags: Optional[List[str]] = None,dependencies: Optional[Sequence[params.Depends]] = None,summary: Optional[str] = None,description: Optional[str] = None,response_description: str = "Successful Response",responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,deprecated: Optional[bool] = None,operation_id: Optional[str] = None,response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,response_model_by_alias: bool = True,response_model_exclude_unset: bool = False,response_model_exclude_defaults: bool = False,response_model_exclude_none: bool = False,include_in_schema: bool = True,response_class: Type[Response] = Default(JSONResponse),name: Optional[str] = None,callbacks: Optional[List[BaseRoute]] = None,openapi_extra: Optional[Dict[str, Any]] = None,):
        kwargs = locals()
        kwargs.pop('self', None)
        args = ()
        def decorator(func):
            self.api[path] = {
                "args": args,
                "kwargs": kwargs,
                "func": func, 
                "method": "post"
            } 
            return func
        return decorator