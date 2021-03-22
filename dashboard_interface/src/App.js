import React from 'react';
import logo from './logo.svg';
import GridInformation from './components/informationGrid.js' ;
import {useState, useEffect } from 'react' ;
import './App.css';
import './components/informationGrid.css' ;





function App() {
  // Global for the type of data that will be shown in each dashboard block 
  const [blockdata, setBlockData] = useState([] ) ; 

  // Fetch all blocks data (used initially) from server 
  const fetchBlocks = async () => {
    const res = await fetch('http://localhost:8888/blockdata') 
    const data = await res.json() 
    return data ;   
  }

  // Fetch indiv block data from server 
  const fetchBlock = async (id) => {
    const res = await fetch(`http://localhost:8888/blockdata/${id}`) 
    const data = await res.json() 
    return res ;   
  }

  useEffect(() => {
    const getBlocks = async () => {
      const blocksFromServer = await fetchBlocks() ; 
      console.log("dataReceived -> ")
      console.log(blocksFromServer)
      setBlockData(blocksFromServer)
    }
    getBlocks()
  }, [])


  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" />
        <p>
          Active information .io ! <code>src/App.js</code> 
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
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
 