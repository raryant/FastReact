
from fastapi.responses import Response
from fastapi import APIRouter
class ComponentGroup:
    def __init__(self) -> None:
        pass

class Component:
    media_type = "text/javascript"
    header = {}
    name = "Fast-React-Component"
    icon = "article"
    api = {}
    def __init__(self)->None:
        pass
    def set_component_name(self, name: str):
        self.name = name
    def drawer_button(self):
        return f'<span className="material-icons">{self.icon}</span>'
    async def load_component(self):        
        print(self, " Called!")
        print(self.test_list)
        self.test_list[0](self)
        content = "const ComponentApp = () => { return(<div>"
        content += "Hello World!\r\n"
        content += self.drawer_button()
        content += "</div>)}; export default ComponentApp"
        return Response(content=content, headers=self.header, media_type=self.media_type)
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return str(self)
    @classmethod
    def get(self, path: str, *args, **kwargs):
        def decorator(func):
            self.api[path] = {
                "args": args,
                "kwargs": kwargs,
                "func": func, 
                "method": "get"
            } 
            return func
        return decorator
    # @classmethod
    # def testing(self):
    #     print("Hello")
    #     def wrap(fun):
    #         print("world!")
    #         print(fun(self))
    #         self.test_list.append(fun)
    #         return fun
    #     def __repr__()->str:
    #         return "Component"
    #     return wrap