import React from 'react';
import logo from './logo.svg';
import GridInformation from './components/informationGrid.js' ;

import './App.css';
import './components/informationGrid.css' ;


function App() {
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
        <GridInformation />
      </div>
    </div>
  );
}

export default App;
 