FastReact.App = (props) =>{
    const [Component, SetComponent] = React.useState('Default')
    const navigate = ReactRouterDOM.useNavigate()
    const location = ReactRouterDOM.useLocation()
    React.useEffect(async()=>{
        console.log("location_changed!", location.pathname)
        // console.log(location)
        if(location.pathname !== '/'){
            // SetComponent(<FastReact.Importir filename={`./_components${location.pathname}`}/>)
            // const ComponentApp = React.lazy(()=>import(`/_components${location.pathname}`))
            const ComponentApp = FastReact.LoadComponent(`/_components${location.pathname}`)
            SetComponent(<ComponentApp/>)
        }
    }, [location])
    window._location = location
    window._navigate = navigate
    // console.log(props)
    return Component
}

ReactDOM.render(
    <FastReact.ThemeProvider>
        <MaterialUI.CssBaseline />
        <FastReact.AuthProvider>
            <ReactRouterDOM.BrowserRouter>
                <FastReact.Header>
                    <React.Suspense fallback={<div>Loading...</div>}>
                        <FastReact.App/>
                    </React.Suspense>
                    {/* <ReactRouterDOM.Routes>
                        <ReactRouterDOM.Route path="/:component" element={<FastReact.App/>}/>
                    </ReactRouterDOM.Routes> */}
                </FastReact.Header>
            </ReactRouterDOM.BrowserRouter>
        </FastReact.AuthProvider>
    </FastReact.ThemeProvider>,
document.querySelector('#root'),
);