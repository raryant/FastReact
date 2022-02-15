"use strict"
function FastReact(){}
FastReact.LoadComponent = (component) => React.lazy(()=>{
    return axios.get(component).then(e=>{
        const BlobURL = URL.createObjectURL(new Blob([Babel.transform(e.data, {presets: ['react']}).code],  {type : 'text/javascript'}));
        console.log('Component Path:',BlobURL)
        return import(BlobURL);
    }).catch((e) => console.log('Error in importing', e))
});
FastReact.Import = (component) =>{
    return axios.get(component).then(e=>{
        const BlobURL = URL.createObjectURL(new Blob([Babel.transform(e.data, {presets: ['react']}).code],  {type : 'text/javascript'}));
        console.log('Component Path:',BlobURL)
        return import(BlobURL);
    }).catch((e) => console.log('Error in importing', e))
};
