import React from 'react';
import logo from './logo.svg';
import GridInformation from './components/informationGrid.js' ;
import {useState, useEffect } from 'react' ;
import './App.css';
import './components/informationGrid.css' ;
import { ContactlessOutlined } from '@material-ui/icons';
import {io} from 'socket.io-client';
import { ConnectionState } from './components/ConnectionState';
import { ConnectionManager } from './components/ConnectionManager';

// Generate initial starting states for grid in the form of  { id  : {dataType: "type" , data: ""}}
const startingState = Array(8).fill(null).reduce((objects, _, index) => ({...objects, [index]: {dataType: index % 2 === 0 ? "text" : "video", data: " "}}), {})

//Nginx server proxy configured as '/api' for communication with backend and databse
const flaskBackendAddress = '/api'
const webSocketBackendAddress = "/socket.io";
console.log(process.env.NODE_ENV) 
const socket = io(webSocketBackendAddress,
  {transports: ['websocket']});

function App() {
  // Global for the type of data that will be shown in each dashboard block 
  const [blockdata, setBlockData] = useState([] ) ; 
  //const [isConnected, setIsConnected] = useState(socket.connected);
  // My "FooEvent" below as per socket-io documentation 
  
  // Fetch all blocks data (used initially) from server 
  const fetchBlocks = async () => {
    const res = await fetch(`${flaskBackendAddress}/blockdata`) 
    const data = await res.json() 
    return data ;   
  }
  
  //fetch latest data from Flask backend 
  const fetchnewData = async () => {
    const res = await fetch(`${flaskBackendAddress}/newblockdata`) 
    const data = await res.json() 
    return data ;   
  }
  const testWebSocket = async () => {
    console.log("executing...testblocks")
    const res = await fetch(`${flaskBackendAddress}/testWebSocket`) 
  }
  // Fetch indiv block data from server 
  // TODO: Currently not used (also not implemented on backend)
  const fetchBlock = async (id) => {
    const res = await fetch(`${flaskBackendAddress}/blockdata/${id}`) 
    const data = await res.json() 
    return data ;   
  }

  useEffect(() => {
    console.log("UseEffect()...")
    // Get data of events for each "Block" displayd in the dashboard 
    const getBlocks = async () => {
      const blocksFromServer = await fetchnewData() ; 
      {console.log("testBlockData -> " , blocksFromServer)}
      socket.emit("testEvent","*** this is my message ***")
      setBlockData(blocksFromServer);
  }
    getBlocks();
    

    // Listens for requests from the server to update dashboard with newdata (triggered when event data is changed/deleted)
    socket.on('newdata', (data) => {
      console.log('Received data from Flask:', data);
      getBlocks();
    });
    
    //http request which asks for a WebSocket respone; useful for debugging WebSocket. 
    //testWebSocket() ;
    
    return () => {
    
    };

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

//******* FUTURE feats *************/
    //Not Implemented: Initial Code to control WebSocket status with UI elements
    // function onConnect() {
    //   setIsConnected(true);
    // }
    
    // function onDisconnect() {
    //   setIsConnected(false);
    // }

    // socket.on('connect', onConnect);
    // socket.on('disconnect', onDisconnect);

    //  {/* <ConnectionState isConnected={ isConnected }/>
    //   <ConnectionManager />  */}

    // return () => {
    //   ** more UNIMPLENETED code for client control of websocket with UI */
    //   socket.off('connect', onConnect);
    //   socket.off('disconnect', onDisconnect);
      
    // };
  
    // }, [])
    //******************/
 