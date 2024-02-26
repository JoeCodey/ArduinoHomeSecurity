// websocket_button.js

import React, { useState } from 'react';

const flaskBackendAddress = '/api'

export const WebsocketButton = ({ socket }) => {
  const [isClicked, setIsClicked] = useState(false);

  const handleButtonClick = () => {
    setIsClicked(true);

    // Emit a custom event using the WebSocket instance from props
    socket.emit('test_event', "***emit 'testEvent' from button ");

    setTimeout(() => {
        setIsClicked(false);
      }, 1000);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', marginRight: '10px' }}>
      {/* Added marginRight to move the button slightly away from the h1 tag */}
      <button
        style={{
          backgroundColor: isClicked ? 'green' : 'blue',
          color: 'white',
          border: '2px solid black',
          borderRadius: '5px',
          padding: '8px 12px',
        }}
        onClick={handleButtonClick}
      >
        {isClicked ? 'Clicked!' : 'Click me to test WebSocket'}
      </button>
    </div>
  );
};

export const DeleteAllButton = () => {
  const [isClicked, setIsClicked] = useState(false);

  const handleDeleteAll = () => {
    setIsClicked(true);

    fetch('/api/deleteall', {
      method: 'GET',
    })
      .then(response => {
        if (response.ok) {
          console.log('All data deleted successfully');
          // Optionally, you can perform any additional actions upon successful deletion
        } else {
          console.error('Failed to delete all data');
          // Handle non-200 status codes (e.g., show an error message)
        }
      })
      .catch(error => {
        console.error('Error occurred while deleting all data:', error);
        // Handle network or other errors
      })
      .finally(() => {
        // Reset the button state after some time
        setTimeout(() => {
          setIsClicked(false);
        }, 1000);
      });
  };

  return (
    <button
      style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        backgroundColor: isClicked ? 'green' : 'blue',
        color: 'white',
        border: '2px solid black',
        borderRadius: '5px',
        padding: '8px 12px',
        cursor: isClicked ? 'not-allowed' : 'pointer',
      }}
      onClick={handleDeleteAll}
      disabled={isClicked}
    >
      {isClicked ? 'Deleting...' : 'Delete All Data'}
    </button>
  );
};

