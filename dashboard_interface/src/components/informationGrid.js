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
                    if(props.metaData.cameraData === 'yes'){
                        return (
                            <ArducamEventPair metaData = {props.metaData} imgId= {props.blockId} /> 
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
//    const startingState = Array(8).fill(null).reduce((objects, _, index) => ({...objects, [index]: {dataType: index % 2 == 0 ? "text" : "video", data: " "}}), {})
//     const [gridCharac, setDataType] = useState([dataTypes]) ;

    // function handleChange(obj, index ){ // new obj state 

    //     setObjects([...dataTypes], obj) ; 
    // }
    // if (!gridCharac) {gridCharac = startingState } 

    // useEffect(() => {
    //     effect
    //     return () => {
    //         cleanup
    //     }
    // }, [input])
    

    let id_num = 0 ; 
    let lengthDatatypes = Object.keys(dataTypes).length -1; 
        return (
            <div class = "grid-wrapper" >  
               
                {
                dataTypes.map( (dataTypeInBlock, index) => (
                        
                       
                         <IndivBlock dataType= {dataTypeInBlock.dataType} blockId= {index} metaData = {dataTypeInBlock}   /> 
                        
                        
                         
                         

                    ))
                }
     
                <style>{".id-"+lengthDatatypes+"{grid-area: 2 / 2 / span 2 / span 2;}"}</style> 
            </div>

        ) ;
    }
export default GridInformation ;
    /*
     ** Class information has been deprecated for functional component IndivBlock
     ------------------------------------------------------------------------------
    class InformationBlock extends React.Component {
        constructor(props){
            super(props);
        

        }

        gridBlockSetUp(){
            // Returns JSX setting up initial grid properties
            if (this.props.dataType == "video"){
                return(
                <video width="320" height="220" controls>
                    <source src='videos/output.mp4' type="video/mp4"></source>
                </video>
                )
            }else if(this.props.blockSize == "focus"){
                return (<p style={{fontSize:20}}> {this.props.dataType} </p> ) ;
            }else{
                return (<p style={{fontSize:10}}> {this.props.dataType} </p> ) ;
            }
        
        }
        
        render(){
            return (
                <div class="grid-item" >
                    
                    {this.gridBlockSetUp()}
                    {/* <p style={{fontSize:10}}> {this.props.blockId}</p> }
                </div>
            )   ;
        }
    }
**/




