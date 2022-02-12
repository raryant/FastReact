from FastReact import FastReactAPP
import uvicorn

app = FastReactAPP()
# @app.on_event
@app.component('Test-Component')
def testComponent():
    pass

def main():
    uvicorn.run(app, port=8027)

if __name__ == '__main__': main()