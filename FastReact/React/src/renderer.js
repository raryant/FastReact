ReactDOM.render(
    <FastReact.ThemeProvider>
        <MaterialUI.CssBaseline />
        <FastReact.AuthProvider>
            <FastReact.Header>
                
            </FastReact.Header>
        </FastReact.AuthProvider>
    </FastReact.ThemeProvider>,
document.querySelector('#root'),
);