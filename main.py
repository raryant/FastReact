from FastReact import FastReactAPP, Component, Response, ComponentGroup
import uvicorn
import os
app = FastReactAPP()
# print("Set Image: ", app.set_header_image(os.path.join(os.path.dirname(__file__), 'logo.png')))
# print("Image Path: ", app.UIRouter.drawer_header_image_path)
# @app.on_event

@app.component_group('Andromeda')
class AndromedaGroup(ComponentGroup):
    icon = "article"
@app.component_group('Pegasus')
class PegasusGroup(ComponentGroup):
    display_empty = True

@app.component('test1', group=AndromedaGroup)
class TestComponent(Component):
    icon = "face"
    name = "Test1"
    @Component.post('/testing', tags=["API-COMPONENT-1"], response_class=Response.PlainTextResponse)
    async def testing(name: str):
        print("Hellow", name)
        return f"Hellow World! I <3 {name}"
    # def drawer_button(self):
    #     return """<span className="material-icons">info</span>"""
    
@app.component('test2', group='Andromeda')
class TestComponent2(Component):
    icon = "info"
    name = "Test2"
    @Component.get('/testing', tags=["API-COMPONENT-2"], response_class=Response.PlainTextResponse)
    async def testing(name: str):
        print("Hellow", name)
        return f"Hellow World! I <3 {name}"
app.component('test3')(Component)

def main():
    uvicorn.run(app,host='0.0.0.0', port=8027)

if __name__ == '__main__': main()