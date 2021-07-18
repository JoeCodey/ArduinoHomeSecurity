import React, {Component} from 'react';
import {useState} from 'react' ;
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import MotionEvent from './motionEvent.js'
import ArducamEventPair from './arducamEventPair.js' 

const IndivBlock = (props) => {

    

    const [dataType, setDataType] = useState({dataType: "text"})

    function updateState (newState) { setDataType({newState})} 

    function condRenderDatatype(props){
                // Returns JSX setting up initial grid properties
                if (props.dataType === "test_video"){
                    return( 
                        <video width="100%" height="100%" controls style={{backgroundSize: "100%"}}>
                            <source src='videos/output.mp4' type="video/mp4"></source>
                        </video>
                    )
                }else if(props.blockSize === "focus"){
                    return (<p style={{fontSize:20}}> {props.dataType} </p> ) ;
                }else if(props.dataType === "text"){
                    if(props.metaData.cameradata === 'yes'){
                        return (
                            <ArducamEventPair metaData = {props.metaData} imgId= {props.metaData.event_id} /> 
                        );
                    }
                    return (
                            <MotionEvent metaData= {props.metaData}   />
                        ) ;
                }else if(props.dataType === "image"){
                    return (
                        <img width="100%" height="100%" src='testImageDashboard.jpg' type="img/jpg"></img>
                    )
                }
                
    }

    return (
        <div class={"gridId "+"id-"+props.blockId}>
                {condRenderDatatype(props)}
                <p style={{fontSize:10}}> {props.blockId}</p>
        </div>
        )   ;
}

// Generate initial starting states for grid in the form of  { id  : {dataType: "type" , data: ""}}

const GridInformation  = ({dataTypes}) => {
    
    let id_num = 0 ; 
    let lengthDatatypes = Object.keys(dataTypes).length -1; 
        return (
            <div class = "grid-wrapper" >  
                {
                dataTypes.map( (dataTypeInBlock, index) => (
                        // object produced by Cassandra db is only lower-case ... yet JS object indexing is case sensite .dataType != .datatype
                         <IndivBlock dataType= {dataTypeInBlock.datatype} blockId= {index} metaData = {dataTypeInBlock}   /> 
                    ))
                }
                <style>{".id-"+lengthDatatypes+"{grid-area: 2 / 2 / span 2 / span 2;}"}</style> 
            </div>
        ) ;
    }
export default GridInformation ;
 