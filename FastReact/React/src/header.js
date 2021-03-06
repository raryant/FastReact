
// const Content = [
//     {
//     menu: 'Home',
//     desc: 'Home Menu',
//     subMenu: [
//         {content: 'Dashboard', name: 'Dashboard', icon: <span className="material-icons">menu</span>, path: "/", level: [0,1,2,3]},
//         {content: 'Dashboard', name: 'DashboardX', icon: <span className="material-icons">menu</span>, path: "/test1", level: [0,1,2,3]},
//         {content: 'Dashboard', name: 'DashboardXX', icon: <span className="material-icons">menu</span>, path: "/test2", level: [0,1,2,3]},
//       ],
//     }
//   ];
function DrawerItems(){
    const { appTitle, setAppTitle } = React.useContext(FastReact.ThemeContext)
    const { getUserLevel } = React.useContext(FastReact.AuthContext)
    const navigate = ReactRouterDOM.useNavigate()
    const location = ReactRouterDOM.useLocation()
    const [Content, setContent] = React.useState([])
    const updateSelected = (eLink, pageName) => {
        // history.pushState({},'',eLink);
        navigate(eLink)
        setAppTitle(pageName)
    }
    React.useEffect(()=>{
      axios.get('/_components/drawer_content.json').then(ret=>{
        if(ret.status === 200){
          setContent(ret.data)
        }
      })
    },[])
    const classes = {}
    React.useEffect(()=>{
      let title = appTitle
      Content.map(({menu, subMenu})=>{
        const sm = subMenu.map(({name, path, level})=>{
          if(window.location.pathname === path){
            title = menu + ' > ' + name            
            if(!level.some((x)=>x===getUserLevel())){
              // history.pushState({},'','/login')
              navigate('/login')
            }
          }
        })
      })
      setAppTitle(title)
    })
    return(
    <MaterialUI.List>
    {Content.map(({menu, desc, subMenu, icon, display_empty}) => (
      <React.Fragment key={menu}>
        <div style={{display: subMenu.some(({level})=>level.some((x)=>x===getUserLevel())) || display_empty ? '' : 'none'}}>
        <MaterialUI.Tooltip title={desc ? desc : menu} arrow placement="right">
        <MaterialUI.ListItem className={classes.categoryHeader}>
        <div style={{width: '24px', height: '24px', marginRight: '1em', marginLeft: '-0.3em'}}><span className="material-icons">{icon}</span></div>
          <MaterialUI.ListItemText>
            {menu}
          </MaterialUI.ListItemText>
        </MaterialUI.ListItem>
        </MaterialUI.Tooltip>
        {subMenu.map(({ name: subMenuName, icon, path, level, desc: childDesc}) => (
            <div style={{display: subMenu.some(({level})=>level.some((x)=>x===getUserLevel())) ? '' : 'none'}} key={subMenuName}>
            <MaterialUI.Tooltip title={childDesc ? childDesc : subMenuName} arrow placement="right" key={subMenuName}>
            <MaterialUI.MenuItem button="true" style={{display: !level.some((level)=>level===getUserLevel()) ? 'None': ''}} selected={window.location.pathname === path} key={subMenuName} onClick={() => updateSelected(path, menu + " > " + subMenuName)}>
                <div style={{marginLeft: '1em', display: 'flex'}}>
                <div style={{width: '24px', height: '24px', marginRight: '1em', marginLeft: '-0.3em'}}><span className="material-icons">{icon}</span></div>
                <MaterialUI.ListItemText>
                    {subMenuName}
                </MaterialUI.ListItemText>
                </div>
            </MaterialUI.MenuItem>
            </MaterialUI.Tooltip>
          </div>
        ))}
      <MaterialUI.Divider/>
      </div>
      </React.Fragment>
    ))}
    </MaterialUI.List>
    )}
    
const drawerWidth = 240;

const Main = MaterialUI.styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    height: `99vh`,
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const AppBar = MaterialUI.styled(MaterialUI.AppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DrawerHeader = MaterialUI.styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

FastReact.Header = (props) =>{
  const theme = MaterialUI.useTheme();
  const { appTitle, setAppTitle, drawerStatus, setDrawer} = React.useContext(FastReact.ThemeContext)
  const [DrawerHeaderImageState, setDrawerHeaderImage] = React.useState('')
  React.useEffect(()=>{
    // const HeaderImage = FastReact.LoadComponent('%ASSETS_PATH%/drawerHeader.js')
    const HeaderImage = FastReact.LoadComponent('%DRAWER_HEADER_ENDPOINT%')
    setDrawerHeaderImage(<HeaderImage/>)
  },[])
  const DrawerHeaderImage = () =>{
    return DrawerHeaderImageState
  }
  const handleDrawerOpen = () => {
    setDrawer(true);
  };

  const handleDrawerClose = () => {
    setDrawer(false);
  };

  return (
    <MaterialUI.Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" open={drawerStatus}>
        <MaterialUI.Toolbar>
          <MaterialUI.IconButton
            color="inherit"
            aria-label="close drawer"
            onClick={handleDrawerClose}
            edge="start"
            sx={{ mr: 2, ...(!drawerStatus && { display: 'none' }) }}
          >
            {theme.direction === 'ltr' ? <span className="material-icons">chevron_right</span> : <span className="material-icons">chevron_left</span> }
          </MaterialUI.IconButton>
          <MaterialUI.IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(drawerStatus && { display: 'none' }) }}
          >
            <span className="material-icons">menu</span> 
          </MaterialUI.IconButton>
          <MaterialUI.Typography variant="h6" noWrap component="div">
            {appTitle}
          </MaterialUI.Typography>
        </MaterialUI.Toolbar>
      </AppBar>
      <MaterialUI.Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={drawerStatus}
      >
        <DrawerHeader style={{display: 'flex', alignItems: 'flex-start', justifyContent: 'center', padding: 0}}>
            <React.Suspense fallback=''>
            <DrawerHeaderImage/>
            </React.Suspense>
        </DrawerHeader>
        <MaterialUI.Divider />
        <DrawerItems/>        
      </MaterialUI.Drawer>
      <Main open={drawerStatus}>
        <DrawerHeader />
        {props.children}
      </Main>
    </MaterialUI.Box>
  );
}
