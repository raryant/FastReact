const themes = {
  DarkTheme,
  LightTheme,
}
function getTheme(theme) {
  return themes[theme]
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
FastReact.ThemeProvider = (props) => {
  // eslint-disable-next-line react/prop-types
  const { children } = props

  // Read current theme from localStorage or maybe from an api
  const currentTheme = localStorage.getItem('appTheme') || 'LightTheme'

  // State to hold the selected theme name
  const [themeName, _setThemeName] = React.useState(currentTheme)
  const [windowTitle, _setWindowTitle] = React.useState('FastReact')
  const [appTitle, _setAppTitle] = React.useState('FastReact')
  const [drawerStatus, _setDrawer] = React.useState(false)

  // Retrieve the theme object by theme name
  const theme = getTheme(themeName)
  document.title = windowTitle
  // Wrap _setThemeName to store new theme names in localStorage
  const setThemeName = (name) => {
    localStorage.setItem('appTheme', name)
    _setThemeName(name)
  }
  const setWindowTitle = (title) =>{
      document.title = title
      _setWindowTitle(title)
  }
  const setAppTitle = (title) =>{
      _setAppTitle(title)
  }
  const contextValue = {
    currentTheme: themeName,
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
      <MaterialUI.ThemeProvider theme={theme}>{children}</MaterialUI.ThemeProvider>
    </FastReact.ThemeContext.Provider>
  )
}
