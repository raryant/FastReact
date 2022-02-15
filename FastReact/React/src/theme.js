// const themes = (await axios.get('/theme/available_theme')).data
async function getTheme(theme) {
    return MaterialUI.createTheme((await axios.get(`%THEME_PATH%/get/${theme}`)).data)
}

// eslint-disable-next-line no-unused-vars
FastReact.ThemeContext = React.createContext(
  {
    currentTheme: 'normal',
    setTheme: null,
    windowTitle: 'FastReact',
    appTitle: 'FastReact',
    setWindowTitle: null,
    setAppTitle: null,
    drawerStatus: false,
    setDrawer: null,
  },
)
FastReact.AvailableTheme = []
FastReact.ThemeProvider = (props) => {
  // eslint-disable-next-line react/prop-types
  const { children } = props

  // Read current theme from localStorage or maybe from an api
  const currentTheme = localStorage.getItem('appTheme') || 'Dark'

  // State to hold the selected theme name
  const [Theme, _setTheme] = React.useState(MaterialUI.createTheme({}))
  const [windowTitle, _setWindowTitle] = React.useState('FastReact')
  const [appTitle, _setAppTitle] = React.useState('FastReact')
  const [drawerStatus, _setDrawer] = React.useState(false)

  React.useEffect(()=>{
    getTheme(currentTheme).then(e=>{
        _setTheme(e)
      })  
    axios.get(`%THEME_PATH%/available_theme`).then(e=>{
      FastReact.AvailableTheme = e.data
    })
  },[])
  document.title = windowTitle
  // Wrap _setThemeName to store new theme names in localStorage
  const setThemeName = (name) => {
    localStorage.setItem('appTheme', name)
    getTheme(currentTheme).then(e=>{
      _setTheme(e)
    })
  }
  const setWindowTitle = (title) =>{
      document.title = title
      _setWindowTitle(title)
  }
  const setAppTitle = (title) =>{
      _setAppTitle(title)
  }
  const contextValue = {
    currentTheme: Theme,
    setTheme: setThemeName,
    windowTitle: windowTitle,
    appTitle: appTitle,
    setWindowTitle: setWindowTitle,
    setAppTitle: setAppTitle,
    drawerStatus: drawerStatus,
    setDrawer: _setDrawer,
  }

  return (
    <FastReact.ThemeContext.Provider value={contextValue}>
      <MaterialUI.ThemeProvider theme={Theme}>{children}</MaterialUI.ThemeProvider>
    </FastReact.ThemeContext.Provider>
  )
}
