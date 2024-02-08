// websocket_button.js

import React, { useState } from 'react';

const WebsocketButton = ({ socket }) => {
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

export default WebsocketButton;
