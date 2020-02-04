import React, {Component} from 'react';

class InformationBlock extends React.Component {
    constructor(props){
        super(props);
       

    }

    gridBlockSetUp(){
        // Returns JSX setting up initial grid properties
        if (this.props.dataType == "video"){
            return(
            <video width="320" height="240" controls>
                <source src='videos/output.mp4' type="video/mp4"></source>
            </video>
            )
        }else{
            return (<p style={{fontSize:10}}> {this.props.dataType} </p> ) ;
        }
    
    }
    
    render(){
        return (
            <div class="grid-item">
                {this.gridBlockSetUp()}
                
            </div>
        )   ;
    }
}



class GridInformation extends React.Component {

    constructor(props){
        super(props) ;
        this.state = {
            numBlocks: 10 
        } ;

    }

    render(){

        const grid = [] ;

        for (let blk = 0; blk < this.state.numBlocks; blk++) {
           grid.push(<div><InformationBlock dataType = "video" /> </div>);
           grid.push(<div><InformationBlock dataType = "text" /> </div>);
        }

        return (

            <div class = "grid-wrapper">
                {grid}
            </div>

        ) ;
    }

}


export default GridInformation ;
