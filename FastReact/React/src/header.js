
const Content = [
    {
    menu: 'Home',
    desc: 'Home Menu',
    subMenu: [

      ],
    }
  ];
function DrawerItems(){
    const { appTitle, setAppTitle } = React.useContext(FastReact.ThemeContext)
    const { getUserLevel } = React.useContext(FastReact.AuthContext)
    const updateSelected = (eLink, pageName) => {
        // history.go(eLink);
        setAppTitle(pageName)
    }
    const classes = {}
    React.useEffect(()=>{
      let title = appTitle
      Content.map(({menu, subMenu})=>{
        const sm = subMenu.map(({name, path, level})=>{
          if(window.location.pathname === path){
            title = menu + ' > ' + name            
            if(!level.some((x)=>x===getUserLevel())){
              history.push('/login')
            }
          }
        })
      })
      setAppTitle(title)
    })
    return(
    <MaterialUI.List>
    {Content.map(({menu, desc, subMenu }) => (
      <React.Fragment key={menu}>
        <div style={{display: !subMenu.some(({level})=>level.some((x)=>x===getUserLevel())) ? 'none' : ''}}>
        <MaterialUI.Tooltip title={desc ? desc : menu} arrow placement="right">
        <MaterialUI.ListItem className={classes.categoryHeader}>
          <MaterialUI.ListItemText>
            {menu}
          </MaterialUI.ListItemText>
        </MaterialUI.ListItem>
        </MaterialUI.Tooltip>
        {subMenu.map(({ name: subMenuName, icon, path, level, desc: childDesc}) => (
            <MaterialUI.Tooltip title={childDesc ? childDesc : subMenuName} arrow placement="right" key={subMenuName}>
            <MaterialUI.MenuItem button="true" style={{display: !level.some((level)=>level===getUserLevel()) ? 'None': ''}} selected={window.location.pathname === path} key={subMenuName} onClick={() => updateSelected(path, menu + " > " + subMenuName)}>
                <div style={{width: '24px', height: '24px', marginRight: '1em', marginLeft: '-0.3em'}}>{icon}</div>
                <MaterialUI.ListItemText>
                    {subMenuName}
                </MaterialUI.ListItemText>
            </MaterialUI.MenuItem>
            </MaterialUI.Tooltip>
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
            {/* <FastReactEngine.DrawerImage/> */}
            {/* <div id='drawerImage' style={{width: '100%', height: '100%', backgroundSize: '100% 100%', backgroundRepeat: 'no-repeat', backgroundPosition: 'center'}} alt="Header Logo" /> */}
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
