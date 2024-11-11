import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';

interface Message {
  sender: string;
  text: string;
}

const Chatbox = () => {

  const [loadingSession, setLoadingSession] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const [input, setInput] = useState('');       // To hold user input
  const [messages, setMessages] = useState<Message[]>([]); // To hold the conversation history

  useEffect(() => {   // Load session id

    const getFrechSessionId = async () => {
      const response = await apiService.freshSessionId();
      const frechResponse = response.data.session_id;
      if (frechResponse) {
        localStorage.setItem('session-id', frechResponse);
        setSessionId(frechResponse);
        //Console.log(`Got new session id from backend: ${frechResponse}`);
      } else {
        setError('Session-id could not be loaded!');
      }
      setLoadingSession(false);
    };

    const getLocalSessionId = async (maybeSessionId: string) => {
      //Console.log(`Session id found in localStorage: ${maybeSessionId}`);
      const response = await apiService.checkSessionId(maybeSessionId);
      if (response.data.found) {
        //Console.log('Same session id found in database');
        setSessionId(maybeSessionId);
        setLoadingSession(false);
      } else {
        //Console.log('Session id not found in database');
        getFrechSessionId();
      }
    };

    const storedSessionId = localStorage.getItem('session-id');
    if (storedSessionId === null) {
      getFrechSessionId();
    } else {
      getLocalSessionId(storedSessionId);
    }

  }, []);

  // Function to send the user's query to the backend
  const sendMessage = async () => {
    if (input.trim() === '') {return;}
    
    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);
    
    const responseMessage = { sender: 'bot', text: '' };

    // Send the input to the FastAPI backend
    try {
      //Console.log(sessionId);
      if (sessionId === null) {throw new Error('sessionId was null!');}

      const response = await apiService.sendQuery(input, sessionId);
    
      responseMessage.text = JSON.stringify(response.data);
    } catch {
      //Console.log(e);
      responseMessage.text = 'Error: Something went wrong';
    }
  
    setMessages([...messages, userMessage, responseMessage]);
    
    setInput('');  // Clear the input field
  };

  return (
    <div className="chatbox">
      { !error && !loadingSession && (<>
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="input-section">
          <input
            type="text"
            value={input}
            onChange={(e) => { setInput(e.target.value); }}
            onKeyDown={async (e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask me something..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </>)}
      { error && <div>
        {error}
      </div>}
      { loadingSession && <div>
        Loading...
      </div>}
    </div>
  );
};

export default Chatbox;
