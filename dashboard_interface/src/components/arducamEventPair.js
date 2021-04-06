import {
    Component,
    useState
} from "react";

import MotionEvent from './motionEvent.js'

const ArducamEventPair = (props) => {

    const {
        timeStart,
        timeEnd,
        location,
        arducamImage
    } = props


    return ( 
        <>
          
           <MotionEvent metaData= {props.metaData} />
            
            
           <img width="100%" height="100%" src='testImageDashboard.jpg' type="img/jpg">
               
           </img>
    

        </>




    );





}

export default ArducamEventPair;