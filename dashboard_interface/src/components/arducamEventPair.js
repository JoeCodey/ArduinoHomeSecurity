import {
    Component,
    useState,useEffect
} from "react";

import MotionEvent from './motionEvent.js'
import CircularProgress from '@material-ui/core/CircularProgress';

export const useImage = (src) => {
    const [hasLoaded, setHasLoaded] = useState(false);
    const [hasError, setHasError] = useState(false);
    const [hasStartedInitialFetch, setHasStartedInitialFetch] = useState(false);

    useEffect(() => {
        setHasStartedInitialFetch(true);
        setHasLoaded(false);
        setHasError(false);

        // Here's where the magic happens.
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
     const {
        timeStart,
        timeEnd,
        location,
        arducamImage
    } = props

    const d = new Date ; 
    const imageURL =  "http://localhost:8888/getImage?id=" + props.imgId
    
    let {hasLoaded, hasError} = useImage(imageURL) ;

    // const fetchImage = async() => {
    //      const res = await fetch('http://localhost:8888/capture')
    //      return res.blob()
    //     }

    // useEffect(() => {
    //     const getImage = async () => { 
    //     const img_arduCam = await fetchImage()
    //     setState(img_arduCam) 
    //     }
    //     getImage() 
    // },[])   

   


    return ( 
        <>
          
           <MotionEvent metaData= {props.metaData} />
           
            
            {!hasLoaded && <CircularProgress />}
            {hasLoaded && <img height="100%" style={{maxWidth: '500px', width: '100%'}} src={imageURL} />}
           
    

        </>




    );





}

export default ArducamEventPair;