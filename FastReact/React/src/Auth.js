FastReact.AuthContext = React.createContext({
    userData: {},
    setUserData: null,
    login: null,
    logout: null,
    getUserData: null,
    getUserLevel: null,
    updateLastSeen: null,
})
FastReact.AuthProvider = (props) =>{
    const createUserData = (data) =>{
        return ({        
            uid: data.uid || 0,
            name: data.name || null,
            username: data.username || null,
            user_level: data.user_level || 0,
            email: data.email || 0,
            token: data.token || null,
            last_seen: data.last_seen || 0,
            theme: data.theme || 'normal',
            first_visit: data.first_visit || true,
        })
    }
    const dummy = true
    const {children} = props
    let localUserData = localStorage.getItem('userData') || createUserData({})
    try{
        localUserData = JSON.parse(localUserData)
    }catch(err){
        console.error(err)
        localUserData = createUserData({})
        localStorage.setItem('userData', JSON.stringify(localUserData))
    }   
    const [userData, _setUserData] = React.useState(localUserData)
    // const createUserData = createUserData    
    
    const getUserData = () =>{
        return userData
    }
    const getUserLevel = () => {
        return userData.user_level
    }
    const login = (username, password) => {
        if(dummy){
            if(username === 'admin' && password === 'admin'){
                const _userData = createUserData({
                    uid: 1, 
                    name: "Rachmat Riyanto",
                    username: "admin",
                    user_level: 3, 
                    email: "raryant@outlook.com",
                    token: "ini_token",
                    last_seen: new Date().getTime(),
                    theme: "dark"
                })
                _setUserData(_userData)
                localStorage.setItem('userData', JSON.stringify(_userData))
                return {ret: true, userData: _userData}
            }
            return {ret: false, userData: null}
        }
    }
    const logout = () => {
        localStorage.setItem('userData', JSON.stringify(createUserData({})))
        _setUserData(createUserData({}))
        return true
    }
    const updateLastSeen = () =>{ 
        const _userData = userData;
        _userData.last_seen = new Date().getTime()       
        _setUserData(_userData)
        localStorage.setItem('userData', JSON.stringify(_userData))
    }
    const contextValue = {
        userData: userData,
        setUserData: createUserData,
        login: login,
        logout: logout,
        getUserData: getUserData,
        getUserLevel: getUserLevel,
        updateLastSeen: updateLastSeen
    }
    // if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    //     window.auth = contextValue
    // }
      
    return (
        <FastReact.AuthContext.Provider value={contextValue}>
            {children}
        </FastReact.AuthContext.Provider>
    )
}
