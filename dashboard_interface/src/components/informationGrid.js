import React, {Component} from 'react';
import {useState} from 'react' ;
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
                {/* <p style={{fontSize:10}}> {this.props.blockId}</p> */}
            </div>
        )   ;
    }
} 




const IndivBlock = (props) => {
        

    
        function condRenderDatatype(props){
                // Returns JSX setting up initial grid properties
                if (props.dataType == "video"){
                    return(
                    <video width="100%" height="100%" controls style={{backgroundSize: "100%"}}>
                        <source src='videos/output.mp4' type="video/mp4"></source>
                    </video>
                    )
                }else if(props.blockSize == "focus"){
                    return (<p style={{fontSize:20}}> {props.dataType} </p> ) ;
                }else if(props.dataType == "text"){
                    return (<div style={{}}>
                            <p style={{fontSize:13}}> MotionDetected?:  </p> 
                            <p style={{fontSize:13}}> Date:  </p> 
                            <p style={{fontSize:13}}> Loc:  </p> 
                            </div>
                        ) ;
                }
                
    }



    return (
            <>
                {condRenderDatatype(props)}
                <p style={{fontSize:10}}> {props.blockId}</p>
            </>
        )   ;
    

}


 
const GridInformation  = () => {

    const [dataTypes, setDataType] = useState([
        {dataType: 'text',
         metaData: {motionDetected: true, Date: new Date, location: "Entrance"} },
        {dataType: 'video'},
        {dataType: 'text',
        metaData: {motionDetected: true, Date: new Date, location: "Entrance"} },
        {dataType: 'video'},
        {dataType: 'text',
        metaData: {motionDetected: true, Date: new Date, location: "Entrance"}},
        {dataType: 'video'},
        {dataType: 'text',
        metaData: {motionDetected: true, Date: new Date, location: "Entrance"} },
        {dataType: 'video'}
    ]) ;

    
    // setSizeBlock(){
    //     if(this.props.elementSize == "focus"){
    //         style=
    //     }
    // }

    // render(

        // for (let blk = 1; blk < this.state.numBlocks; blk++) {
        //     if (blk == 5) {
        //         grid.push(<div class={"gridId "+"id-"+blk}><IndivBlock blockSize="focus" blockId = {blk} dataType = "focus"/></div>)
        //     }else{
        //     grid.push(<div class={"gridId "+"id-"+blk}><IndivBlock blockId = {blk} dataType = {blk%2 == 0 ? "text":"video"} /> </div>);
        //     }  
        // }

    let id_num = 0 ; 
        return (

            <div class = "grid-wrapper" style={{placeItems: 'center' / 'center'}}>  
                {dataTypes.map( (dataTypeInBlock, index) => (
                        <div class={"gridId "+"id-"+index}>
                        <IndivBlock dataType= {dataTypeInBlock.dataType} blockId= {index}  /> 
                        </div>
                    
                    )
                )
                }
     
                <style>{".id-1{grid-area: 2 / 2 / span 2 / span 2;}"}</style>
            </div>

        ) ;
    }


export default GridInformation ;
