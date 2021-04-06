import React, { Component } from "react";
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';

const MotionEvent = (props) => {

    const {
        timeStart,
        timeEnd,
        location
    } = props.metaData


    return (<>
                            
                            
         <p style={{fontSize:13 , position: "relative" , top: '2px'}}> <ErrorOutlineIcon /> MotionDetected:  </p> 

        <p style={{fontSize:13, marginBottom:0}}>
            TimeStart / TimeEnd 
        </p>
        <p style={{fontSize:13, margin:0 , paddingTop:0}}>
            {props.metaData.timeStart} / {props.metaData.timeEnd}
        </p>


        
        {/* {console.log("Time props -> " + props.metaData.timeEnd)} */}

        <p style={{fontSize:13}}> Loc:  {props.metaData.location}</p> 

        {/* <style>{".id-"+props.blockId+"{place-items: start start}"}</style> */}
        
    
</>
) ;
}

export default MotionEvent ; 