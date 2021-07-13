import React from 'react';
import logo from './logo.svg';
import GridInformation from './components/informationGrid.js' ;
import {useState, useEffect } from 'react' ;
import './App.css';
import './components/informationGrid.css' ;
import { ContactlessOutlined } from '@material-ui/icons';

// Generate initial starting states for grid in the form of  { id  : {dataType: "type" , data: ""}}
const startingState = Array(8).fill(null).reduce((objects, _, index) => ({...objects, [index]: {dataType: index % 2 === 0 ? "text" : "video", data: " "}}), {})
const flaskBackendAddress = 'http://localhost:8888'
function App() {
  // Global for the type of data that will be shown in each dashboard block 
  const [blockdata, setBlockData] = useState([] ) ; 

  // Fetch all blocks data (used initially) from server 
  const fetchBlocks = async () => {
    const res = await fetch(`${flaskBackendAddress}/blockdata`) 
    const data = await res.json() 

    return data ;   
  }
  
  //fetch latest data from Flask backend 
  //TODO: Dockerize backend and frontentend for portability 
  const fetchnewData = async () => {
    const res = await fetch(`${flaskBackendAddress}/newblockdata`) 
    const data = await res.json() 
    return data ;   
  }

  // Fetch indiv block data from server 
  // TODO: Currently not used (also not implemented on backend)
  const fetchBlock = async (id) => {
    const res = await fetch(`${flaskBackendAddress}blockdata/${id}`) 
    const data = await res.json() 
    return data ;   
  }

  
  useEffect(() => {
    // Get initial data 
    // (Currently this sample static data to test frontent rendernig)
    const getBlocks = async () => {
      const blocksFromServer = await fetchBlocks() ; 
      {console.log("testBlockData -> " , blocksFromServer)}
      setBlockData(blocksFromServer)
  }
    getBlocks()
    // Get new event data for every block from backend 
    //TODO: replace SetInterval Polling implementation 
    // with realtime Web Socket Connection 
    const timer = setInterval(async () => {
        const data = await fetchnewData()
        {console.log("newBlockData -> " , data)}
        setBlockData(data)
    },3000)
  }, [])

  return (

    <div className="App">
      <header className="App-header">

        <h1>Active Information Dashboard
        </h1>
      </header>

      <div className="Grid-Layouts">
    
        <GridInformation dataTypes={blockdata}/>
      </div>
    </div> 
  );
}

export default App;
 