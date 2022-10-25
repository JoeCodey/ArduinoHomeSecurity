import {
    Component,
    useState,useEffect
} from "react";

import MotionEvent from './motionEvent.js'
import CircularProgress from '@material-ui/core/CircularProgress';

// 127.0.0.1 addresses docker container from the outside (e.g. the browser)
const flaskBackendAddress = '/api'
var incrementer = 0 

// Custom Hook for loading image from backend 
export const useImage = (src) => {
    const [hasLoaded, setHasLoaded] = useState(false);
    const [hasError, setHasError] = useState(false);
    const [hasStartedInitialFetch, setHasStartedInitialFetch] = useState(false);

    useEffect(() => {
        setHasStartedInitialFetch(true);
        setHasLoaded(false);
        setHasError(false);

        
        const image = new Image();
        image.src = src;

        const handleError = () => {
            setHasError(true);
        };

        const handleLoad = () => {
            setHasLoaded(true);
            setHasError(false);
        };

        image.onerror = handleError;
        image.onload = handleLoad;

        return () => {
            image.removeEventListener("error", handleError);
            image.removeEventListener("load", handleLoad);
        };
    }, [src]);

    return { hasLoaded, hasError, hasStartedInitialFetch };
};

const ArducamEventPair = (props) => {
     

    const imageURL =  `${flaskBackendAddress}/getImage?id=${props.imgId}`
    console.log("prop arducampair -> ",props)
    console.log("imageURL -> ",imageURL)
    console.log("arducamId-> ",incrementer)
    incrementer += 1 
    
    let {hasLoaded, hasError} = useImage(imageURL) ;



    return ( 
        <>      
           <MotionEvent metaData= {props.metaData} />
            {!hasLoaded && <CircularProgress />}
            {hasLoaded && <img height="100%" style={{maxWidth: '500px', width: '100%'}} src={imageURL} />}

        </>

    );
}

export default ArducamEventPair;