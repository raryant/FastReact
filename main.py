from FastReact import FastReactAPP, Component, Response
import uvicorn
import os
app = FastReactAPP()
# print("Set Image: ", app.set_header_image(os.path.join(os.path.dirname(__file__), 'logo.png')))
# print("Image Path: ", app.UIRouter.drawer_header_image_path)
# @app.on_event
@app.component('test1')
class TestComponent(Component):
    icon = "face"
    # def drawer_button(self):
    #     return """<span className="material-icons">info</span>"""
    
@app.component('test2')
class TestComponent2(Component):
    icon = "info"
    @Component.get('/testing', tags=["API-COMPONENT-2"], response_class=Response.PlainTextResponse)
    async def testing(name: str):
        print("Hellow", name)
        return f"Hellow World! I <3 {name}"

def main():
    uvicorn.run(app,host='0.0.0.0', port=8027)

if __name__ == '__main__': main()