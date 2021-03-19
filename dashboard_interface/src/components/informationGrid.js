import React, {Component} from 'react';
import {useState} from 'react' ;
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';

const IndivBlock = (props) => {

    const [dataType, setDataType] = useState({dataType: "text"})

    function updateState (newState) { setDataType({newState})} 

    function condRenderDatatype(props){
                // Returns JSX setting up initial grid properties
                if (props.dataType == "video"){
                    return(
                    <div class={"gridId "+"id-"+props.blockId} style={{placeItems: 'center' / 'center'}}>
                    <video width="100%" height="100%" controls style={{backgroundSize: "100%"}}>
                        <source src='videos/output.mp4' type="video/mp4"></source>
                    </video>
                    </div>
                    )
                }else if(props.blockSize == "focus"){
                    return (<p style={{fontSize:20}}> {props.dataType} </p> ) ;
                }else if(props.dataType == "text"){
                    return (<div class={"gridId "+"id-"+props.blockId} style={{placeItems: 'start' / 'start'}}>
                            
                            
                                    <ErrorOutlineIcon /> <p style={{fontSize:13}}> MotionDetected:  </p> 
                                
                        
                                    <p style={{fontSize:13}}> Date:  </p> 
                          
                                    <p style={{fontSize:13}}> Loc:  </p> 
                               
                         
                    
                            </div>
                        ) ;
                }
                
    }

    return (
            <>
                {condRenderDatatype(props)}
                
            </>
        )   ;
}

// Generate initial starting states for grid in the form of  { id  : {dataType: "type" , data: ""}}
const startingState = Array(8).fill(null).reduce((objects, _, index) => ({...objects, [index]: {dataType: index % 2 == 0 ? "text" : "video", data: " "}}), {})


const GridInformation  = ({dataTypes}) => {

    // const [dataTypes, setDataType] = useState(startingState) ;

    // function handleChange(obj, index ){ // new obj state 

    //     setObjects([...dataTypes], obj) ; 
    // }
     
    let id_num = 0 ; 
        return (

            <div class = "grid-wrapper" >  
                {dataTypes.map( (dataTypeInBlock, index) => (
                        
                        <IndivBlock dataType= {dataTypeInBlock.dataType} blockId= {index}  /> 
                        
                    )
                )
                }
     
                <style>{".id-1{grid-area: 2 / 2 / span 2 / span 2;}"}</style>
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




